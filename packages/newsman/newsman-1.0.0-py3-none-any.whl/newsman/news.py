# -*- coding: utf-8 -*-
from .reader import Reader
from .scraping import Scraper

class News:
    """A sequence of <Page> objects. News objects have attributes at news level
    and can access attributes of contained articles.

    Attributes:

    """

    def __init__(self, config, pipes=None):
        """Object initialization.

        Args:
            config (dict): Configuration parameters.
            pipes (list): List of pipeline components to load for html
                processing.
        """

        # scraper
        self.scraper = Scraper(config)

        # init reader and create pipeline
        reader = Reader(config)
        for name in pipes:
            pipe = reader.create_pipe(name, config)
            reader.add_pipe(pipe, name=name)
        self.reader = reader

    def __call__(self, src):
        """Starts news scraping.

        Args:
            src (str): Source url for news scraping.
        """

        pages = []
        for data in self.scraper(src):
            page = self.reader(data)
            pages.append(page)

        return pages

    def __getitem__(self, idx):
        """Get a `Page` object by key."""
        return self._pages[idx]

    def __iter__(self):
        """Iterate over `Page` objects."""
        for i in range(len(self._pages)):
            yield self._pages[i]

    def __len__(self):
        """Get number of items."""
        return len(self._pages)
