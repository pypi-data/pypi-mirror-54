# -*- coding: utf-8 -*-
import json

class Page:
    """Class for storing data retrieved by a web site.

    Data can include raw information (e.g. bytes, html) and annotations (e.g.
    keywords, summary).
    Page objects are the items stored in News object. They are open as each
    processing pipe can set its specific attributes to them, in addition to
    default ones.
    """

    def __init__(self, url, raw, timestamp):
        """Object initialization.

        Args:
            url: <Url> object.
        """

        # data and annotations
        self.url = url
        self.raw_bytes = raw
        self.timestamp = timestamp
        self.html = None
        self.tag_contents = None
        self.title = None
        self.text = None
        self.main_image = None
