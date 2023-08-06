# -*- coding: utf-8 -*-
from .pipe import Pipe

class Text2title(Pipe):

    name = 'text2title'

    def __init__(self, config):
        """Object initialization.

        Args:
            config: Dict with configuration parameters.
        """
        pass

    def set_annotations(self, page, **kwargs):
        """Analyses pages for performing keywords and summary annotation.

        Args:
            page: News object.

        Returns:
            page: News object with article text.
        """

        if page.tag_contents:
            page.title = self.extract_title(page.tag_contents)

        return page

    def extract_title(self, tag_contents):
        """Extracts page title."""

        # priority for TITLE TAG
        if 'TAG_TITLE' in tag_contents:
            title = tag_contents['TAG_TITLE'][0]
        elif 'TAG_H1' in tag_contents:
            title = tag_contents['TAG_H1'][0]
        elif 'TAG_H2' in tag_contents:
            title = tag_contents['TAG_H2'][0]
        elif 'TAG_H3' in tag_contents:
            title = tag_contents['TAG_H3'][0]
        else:
            title = ''

        return title
