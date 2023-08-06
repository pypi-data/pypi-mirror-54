# -*- coding: utf-8 -*-
import re
from threading import Thread
from .pipe import Pipe
from newsman.utils.url import Url
from newsman.scraping import UrlFilter
import requests

#RE_IMG = re.compile(r'<img (?:.+?) src="(.+?)" (?:.+?)>', re.MULTILINE|re.DOTALL)
RE_IMG = re.compile(r'<img(?:.*?)src="(.+?)"', re.MULTILINE|re.DOTALL)

ACCEPTED_EXTS = ['txt', 'xml', 'json', 'doc', 'docx', 'pdf', 'gif', 'png',
'jpg', 'jpeg', 'png', 'bmp', 'ico', 'svg', 'css', 'js', 'jsp', 'php', 'mp3',
'mp4', 'mov', 'mpeg4', 'flv']

def perform_request(url, results, idx):
    """Performs a HTTP request for getting image size."""
    try:
        resp = requests.get(url, timeout=3.5, stream=True)
        results[idx] = resp.headers['Content-Length']
    except:
        results[idx] = 0

    return

class Html2image(Pipe):
    """Class for extracting the main image for html code.

    Selection is based on ulr filtering and largest size.

    Attributes:
        urlfilter: UrlFilter object for link validation.
    """

    name = 'html2image'

    def __init__(self, config):
        """Object initialization.

        Args:
            config: Dict with configuration parameters.
        """

        self.urlfilter = UrlFilter(accepted_exts=ACCEPTED_EXTS,
            rejected_exts=None, accepted_domains=config['accepted_domains'],
            rejected_domains=config['rejected_domains'])

    def set_annotations(self, page, **kwargs):
        """Extracts image info from html code in asynchronous mode.

        Args:
            page: <Page> object.

        Returns:
            page: <Page> object.
        """

        urlfilter = self.urlfilter

        html = page.html
        if html:

            urls = []
            for match in RE_IMG.finditer(html):

                try:
                    url = Url(match.group(1))
                    #url = self.check_url(match.group(1))
                    if urlfilter.validate_domain(url) and urlfilter.validate_content(url):
                        urls.append(url)
                except ValueError:
                    # invalid url, do nothing
                    pass

            img_sizes = self.get_sizes(urls)
            img_data = [(url.url, img_size) for url, img_size in zip(urls, img_sizes)]

            page.main_image = self.extract_main_image(img_data)

        return page

    def extract_main_image(self, img_data):
        """Finds image with largest size."""

        if img_data:
            main_image = max(img_data, key=lambda item:int(item[1]))[0]
        else:
            main_image = None

        return main_image

    def get_sizes(self, urls):

        num_urls = len(urls)

        # init
        threads = [None] * num_urls
        img_sizes = [None] * num_urls

        for ii in range(len(threads)):
            threads[ii] = Thread(target=perform_request, args=(urls[ii].url, img_sizes, ii))
            threads[ii].start()

        for ii in range(len(threads)):
            threads[ii].join()

        return img_sizes
