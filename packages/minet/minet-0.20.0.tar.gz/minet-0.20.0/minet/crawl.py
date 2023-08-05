# =============================================================================
# Minet Crawl
# =============================================================================
#
# Functions related to the crawling utilities of minet.
#
from queue import Queue
from persistqueue import SQLiteQueue
from quenouille import imap_unordered, QueueIterator
from ural import get_domain_name
from collections import namedtuple
from urllib.parse import urljoin
from shutil import rmtree

from minet.scrape import Scraper
from minet.utils import (
    create_pool,
    request,
    extract_response_meta,
    PseudoFStringFormatter
)

from minet.defaults import (
    DEFAULT_GROUP_PARALLELISM,
    DEFAULT_GROUP_BUFFER_SIZE,
    DEFAULT_THROTTLE
)

FORMATTER = PseudoFStringFormatter()

CrawlWorkerResult = namedtuple(
    'CrawlWorkerResult',
    [
        'job',
        'scraped',
        'error',
        'response',
        'meta',
        'next_jobs'
    ]
)


def ensure_list(value):
    if not isinstance(value, list):
        return [value]
    return value


class CrawlJob(object):
    __slots__ = ('url', 'level', 'spider')

    def __init__(self, url, level=0, spider='default'):
        self.url = url
        self.level = level
        self.spider = spider

    def __repr__(self):
        class_name = self.__class__.__name__

        return (
            '<%(class_name)s level=%(level)s url=%(url)s spider=%(spider)s>'
        ) % {
            'class_name': class_name,
            'url': self.url,
            'level': self.level,
            'spider': self.spider
        }


class Spider(object):
    def __init__(self, definition, name='default'):

        # Descriptors
        self.name = name
        self.definition = definition
        self.next_definition = definition.get('next')

        # Settings
        self.max_level = definition.get('max_level', float('inf'))

        # Scrapers
        self.scraper = None
        self.next_scraper = None

        if 'scraper' in definition:
            self.scraper = Scraper(definition['scraper'])

        if self.next_definition is not None and 'scraper' in self.next_definition:
            self.next_scraper = Scraper(self.next_definition['scraper'])

    def get_start_jobs(self):
        start_urls = (
            ensure_list(self.definition.get('start_url', [])) +
            ensure_list(self.definition.get('start_urls', []))
        )

        return [CrawlJob(url, spider=self.name) for url in start_urls]

    def job_from_target(self, target, current_url, next_level):
        if isinstance(target, str):
            return CrawlJob(
                url=urljoin(current_url, target),
                level=next_level,
                spider=self.name
            )

        # TODO: validate target
        return CrawlJob(
            url=urljoin(current_url, target['url']),
            level=next_level,
            spider=target.get('spider', self.name)
        )

    def next_targets_iter(self, job, html):
        next_level = job.level + 1

        # Scraping next results
        if self.next_scraper is not None:
            scraped = self.next_scraper(html)

            if isinstance(scraped, list):
                yield from scraped
            else:
                yield scraped

        # Formatting next url
        elif 'format' in self.next_definition:
            yield FORMATTER.format(
                self.next_definition['format'],
                level=next_level
            )

    def get_next_jobs(self, job, html, current_url):
        if not self.next_definition:
            return

        next_level = job.level + 1

        if next_level > self.max_level:
            return

        next_jobs = []

        for target in self.next_targets_iter(job, html):
            next_jobs.append(self.job_from_target(target, current_url, next_level))

        return next_jobs


class TaskContext(object):
    def __init__(self, queue, queue_iterator):
        self.queue = queue
        self.queue_iterator = queue_iterator

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.queue.task_done()
        self.queue_iterator.task_done()


def crawl(spec, queue_path=None, threads=25, buffer_size=DEFAULT_GROUP_BUFFER_SIZE,
          throttle=DEFAULT_THROTTLE):

    # NOTE: crawling could work depth-first but:
    # buffer_size should be 0 (requires to fix quenouille issue #1)

    using_persistent_queue = queue_path is not None

    # Memory queue
    if not using_persistent_queue:
        queue = Queue()

    # Persistent queue
    else:
        queue = SQLiteQueue(queue_path, multithreading=True, auto_commit=False)

    # Creating spiders
    if 'spiders' in spec:
        spiders = {name: Spider(s, name=name) for name, s in spec['spiders'].items()}
    else:
        spiders = {'default': Spider(spec)}

    def enqueue(jobs):
        for job in jobs:
            assert isinstance(job, CrawlJob)
            queue.put(job)

    # Collecting start jobs - we only add those if queue is not pre-existing
    if queue.qsize() == 0:
        for spider in spiders.values():
            enqueue(spider.get_start_jobs())

    http = create_pool(threads=threads)

    queue_iterator = QueueIterator(queue)
    task_context = TaskContext(queue, queue_iterator)

    def grouper(job):
        return get_domain_name(job.url)

    def worker(job):
        spider = spiders[job.spider]

        err, response = request(http, job.url)

        if err:
            return CrawlWorkerResult(
                job=job,
                scraped=None,
                error=err,
                response=response,
                meta=None,
                next_jobs=None
            )

        meta = extract_response_meta(response)

        # Decoding response data
        data = response.data.decode(meta['encoding'], errors='replace')

        # Scraping items
        scraped = None

        if spider.scraper is not None:
            scraped = spider.scraper(data)

        # Finding next jobs
        next_jobs = spider.get_next_jobs(job, data, response.geturl())

        return CrawlWorkerResult(
            job=job,
            scraped=scraped,
            error=None,
            response=response,
            meta=meta,
            next_jobs=next_jobs
        )

    multithreaded_iterator = imap_unordered(
        queue_iterator,
        worker,
        threads,
        group=grouper,
        group_parallelism=DEFAULT_GROUP_PARALLELISM,
        group_buffer_size=buffer_size,
        group_throttle=throttle
    )

    for result in multithreaded_iterator:

        with task_context:

            # Errored job
            if result.error:
                yield result

                continue

            # Enqueuing next jobs
            # TODO: enqueueing could also be done in worker
            if result.next_jobs is not None:
                enqueue(result.next_jobs)

            yield result

    # Releasing queue (needed by persistqueue)
    if using_persistent_queue:
        del queue
        rmtree(queue_path)
