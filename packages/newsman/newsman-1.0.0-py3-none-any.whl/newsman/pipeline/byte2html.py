# -*- coding: utf-8 -*-
from .pipe import Pipe
import chardet

class Byte2html(Pipe):

    name = 'byte2html'

    def __init__(self, config):
        """Object initialization.

        Args:
            config: Dict with configuration parameters.
        """
        pass

    def set_annotations(self, page, **kwargs):
        """Extracts raw html from bytes sequence retrieved by web sites.

        Extraction is based on an educated guessing of byte encoding.

        Args:
            page: <Page> object.

        Returns:
            page: <Page> object with article text.
        """

        guessing = chardet.detect(page.raw_bytes)
        if guessing['confidence']>0.6:
            encoding = guessing['encoding']
        else:
            encoding = None

        if encoding:
            html = page.raw_bytes.decode(encoding=encoding, errors='ignore')
            page.html = html

        return page
