# -*- coding: utf-8 -*-
import re
from .pipe import Pipe

RE_HEAD = re.compile(r'<head.*?<\/head>', re.MULTILINE|re.DOTALL)
RE_SCRIPTS = re.compile(r'<script.*?<\/script>', re.MULTILINE|re.DOTALL)
RE_NOSCRIPT = re.compile(r'<noscript>.+?<\/noscript>', re.MULTILINE|re.DOTALL)
RE_STYLES = re.compile(r'<style.*?<\/style>', re.MULTILINE|re.DOTALL)
RE_COMMENT = re.compile(r'<!--.*?-->', re.MULTILINE|re.DOTALL)
RE_TITLE = re.compile(r'<title(?: .+?)?>(.+?)<\/title>', re.MULTILINE|re.DOTALL)
RE_P = re.compile(r'<p(?: .+?)?>(.+?)<\/p>', re.MULTILINE|re.DOTALL)
RE_H1 = re.compile(r'<h1.*?>(.+?)<\/h1>', re.MULTILINE|re.DOTALL)
RE_H2 = re.compile(r'<h2.*?>(.+?)<\/h2>', re.MULTILINE|re.DOTALL)
RE_H3 = re.compile(r'<h3.*?>(.+?)<\/h3>', re.MULTILINE|re.DOTALL)
RE_A = re.compile(r'<a .*?>(.+?)<\/a>', re.MULTILINE|re.DOTALL)
RE_SPACES = re.compile(r'\s+', re.MULTILINE|re.DOTALL)
RE_SPAN = re.compile(r'<span.*?>(.+?)<\/span>', re.MULTILINE|re.DOTALL)
RE_IMG = re.compile(r'<img .+?>', re.MULTILINE|re.DOTALL)
RE_GEN = re.compile(r'<.+?>', re.MULTILINE|re.DOTALL)

class Html2text(Pipe):
    """Class for extracting text fragments from raw html.

    Includes simple methods for TAG cleansing and string url-decoding.

    Attributes:
        text_len_thr: Length threshold (characters). Only text fragments
            longer than threshold will be extracted.
        charmap: A dict for decoding html entities. Keys and values are,
            respectively, encoded and utf-8 decoded strings.
    """

    name = 'html2text'

    def __init__(self, config):
        """Object initialization.

        Args:
            config: Dict with configuration parameters.
        """

        self.text_len_thr = config['text_len_thr']
        self.title_len_thr = config['title_len_thr']
        self.hx_len_thr = config['hx_len_thr']
        self.charmap = config['charmap']

    def set_annotations(self, page, **kwargs):
        """ Extracts text fragments from raw html and stores them internally.

        Adds a Dict contents to pages, with text etxracted from different HTML
        tags.

        Args:
            page: <Page> object.

        Returns:
            page: <Page> object with article text.
        """

        html = page.html

        if html:

            # title must be extracted before decluttering because is in HEAD!
            contents_title = self.apply_regex(html, RE_TITLE, self.title_len_thr)
            html = self._declutter(html)

            contents_h1 = self.apply_regex(html, RE_H1, self.hx_len_thr)
            contents_h2 = self.apply_regex(html, RE_H2, self.hx_len_thr)
            contents_h3 = self.apply_regex(html, RE_H3, self.hx_len_thr)

            contents_p = self.apply_regex(html, RE_P, self.text_len_thr)
            html = RE_P.sub('', html)

            contents_span = self.apply_regex(html, RE_SPAN, self.text_len_thr)

            # title data
            contents = {}
            if contents_title:
                contents['TAG_TITLE'] = contents_title
            if contents_h1:
                contents['TAG_H1'] = contents_h1
            if contents_h2:
                contents['TAG_H2'] = contents_h2
            if contents_h3:
                contents['TAG_H3'] = contents_h3

            # text data
            text_p = '\n'.join(contents_p)
            text_span = '\n'.join(contents_span)

            if text_p and text_span:
                text = '\n'.join([text_p, text_span])
            else:
                if text_p:
                    text = text_p
                else:
                    text = text_span

            page.tag_contents = contents
            page.text = text

        return page

    def apply_regex(self, html, reg_exp, len_thr):
        """Extracts text content from given regex, with a length threshold."""

        contents = []
        for match in reg_exp.finditer(html):

            content = match.group(1)
            content = self._decode(content)
            content = self._clean_text(content)

            # remove spaces for threshold comparison
            if len(content.replace(' ', '')) > len_thr:
                contents.append(content)

        return contents

    def _clean_text(self, text):
        """ Removes A and spurious tags. """
        #text = self._extract_from_tag(RE_SPAN, text)
        text = self._extract_from_tag(RE_A, text)
        text = RE_GEN.sub('', text).strip()

        return text

    def _declutter(self, html):
        """ Removes extra-text sections and style tags. """

        html = RE_HEAD.sub('', html)
        html = RE_SCRIPTS.sub('', html)
        html = RE_NOSCRIPT.sub('', html)
        html = RE_STYLES.sub('', html)
        html = RE_COMMENT.sub('', html)
        html = RE_SPACES.sub(' ', html)
        html = RE_IMG.sub(' ', html)
        html = html.replace('<em>', '').replace('</em>', '')
        html = html.replace('<strong>', '').replace('</strong>', '')
        html = html.replace('<br>', '')

        return html

    def _decode(self, text):
        """ Simple HTML-decoding based on replacement. """

        for k, v in self.charmap.items():
            text = text.replace(k, v)

        return text

    def _extract_from_tag(self, regex, html):
        """Extracts text content from inside TAG specified by regex. """
        m = regex.search(html)
        while m:
            html = html[:m.start()] + m.group(1) + html[m.end():]
            m = RE_A.search(html)

        return html
