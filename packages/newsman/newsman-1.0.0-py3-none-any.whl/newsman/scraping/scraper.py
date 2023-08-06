# -*- coding: utf-8 -*-
import re
from time import time, sleep
from datetime import datetime
from .filtering import UrlFilter
from newsman.utils.url import Url
from requests.exceptions import RequestException as request_exception
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests import Session as ReqSession

MAX_DELAY = 10
HTML_CONTENT = 'text/html'
RE_LINKS = re.compile(r'(href|src)="(\S+)"')

# URL filtering
REJECTED_EXTS = ['txt', 'xml', 'json', 'doc', 'docx', 'pdf', 'gif', 'png',
'jpg', 'jpeg', 'png', 'bmp', 'ico', 'svg', 'css', 'js', 'jsp', 'php', 'mp3',
'mp4', 'mov', 'mpeg4', 'flv']

# chrome on windows
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'

def init_session(config):
    """Inits a new Requests.Session."""

    # init session
    session = ReqSession()

    # define retry mechanism
    retry = Retry(total=3, read=3, connect=3, backoff_factor=0.3,
        status_forcelist=(500, 502, 503, 504))

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    # set proxy data
    if config.get('proxies'):
        session.proxies.update(config['proxies'])

    return session

class Scraper:
    """A class for retrieving content from URLs.

    Attributes:
        session: Requests.Session object, if not provided a default one
            will be initialized.
        conn_timeout: Connection timeout. Set to 3.5 seconds by default.
        recursive: Follow page links (recursive download).
        link_depth: Level of recursion (link depth).
        urlfilter: UrlFilter object for download and link validation.
        limit: If specified, sets maximum number of visited sites (integer).
        visited: Set of (unique) web-sites traversed by the object.
        delay: A boolean flag, if True adds a random delay between requests to
            evade IP-blocking.
    Returns:
        news: A News object with content of retrieved pages.
    """

    def __init__(self, config):
        """Object initialization.

        Args:
            config: Dict with configuration parameters.
            session: A Requests.Session object.
        """
        # web session
        self._session = init_session(config)
        # connection
        self.conn_timeout = config['conn_timeout']
        # recursion
        self.recursive = config['recursive']
        self.link_depth = config['link_depth']
        # url filtering
        self.urlfilter = UrlFilter(accepted_exts=None,
            rejected_exts=REJECTED_EXTS,
            accepted_domains=config['accepted_domains'],
            rejected_domains=config['rejected_domains'])
        # max. number of pages scraped
        self.limit = config['limit']
        # request delay
        self.delay = config['delay']
        # globally set visited urls and download metadata
        self.visited = set()

    def __call__(self, url):
        """Starts crawling the given url."""

        # kept  at object-level
        visited = self.visited
        session = self._session
        link_depth = self.link_depth

        # crafted headers
        headers = {'User-Agent': user_agent}

        if self.limit:
            currently_visited = 0

        # init request times
        req_times = []

        curr_links = [url]
        curr_level = 1
        while curr_level <= link_depth:

            next_links = []
            for url in curr_links:

                data = None

                # clean & check
                url_obj = Url(url)

                # skip already visited urls
                if url_obj.loc in visited:
                    continue

                try:
                    t_a = time()
                    resp = session.get(url, timeout=self.conn_timeout, headers=headers)
                    t_b = time()

                    if resp.status_code != 200:
                        raise request_exception()

                except request_exception as err:
                    resp = None

                else:
                    # get retrieval timestamp
                    timestamp = self._timestamp()

                    # update visited set
                    visited.add(url_obj.loc)
                    if self.limit:
                        currently_visited += 1

                    # handle delay time
                    req_times.append(t_b - t_a)
                    if self.delay:
                        self.set_delay(req_times)

                    # content check
                    content_type = resp.headers.get('Content-Type')
                    if content_type and HTML_CONTENT in content_type:

                        data = (url_obj, resp.content, timestamp)

                        # search for links
                        html = resp.text
                        links = self._extract_links(url_obj, html)

                        # update next links
                        next_links += links

                # return site data
                if data:
                    yield data

                if self.limit and currently_visited == self.limit:
                    break

            curr_links = next_links
            curr_level += 1
            del next_links

    def _extract_links(self, url_obj, html):
        """Extracts valid links from url."""

        links = []
        urlfilter = self.urlfilter

        # search for href links / src images
        matches = RE_LINKS.findall(html)
        for match in matches:

            lnk = match[1].split('?')[0]
            lnk = lnk.split('#')[0]

            if not lnk:
                continue

            # workaround for relative links
            if lnk[0:2] == '//':
                lnk = f'{url_obj.scheme}://{lnk[2:]}'
            elif lnk[0] == '/':
                lnk = f'{url_obj.scheme}://{url_obj.domain}{lnk}'

            try:
                url_obj = Url(lnk)
                if urlfilter.validate_domain(url_obj) and urlfilter.validate_content(url_obj):
                    links.append(lnk)
            except ValueError:
                # link not valid
                pass

        return list(set(links))

    def _timestamp(self):
        """Generates a timestamp for retrieval time. """

        return datetime.now()

    def set_delay(self, req_times):
        """Adds a delay for next request.

        Delay is evaluated as 1.1 times the mean response time of last 10
        requests.
        """

        req_times = req_times[-10:]
        mtbr = sum(req_times)/len(req_times)
        sleep(min(1.1*mtbr, MAX_DELAY))

        return
