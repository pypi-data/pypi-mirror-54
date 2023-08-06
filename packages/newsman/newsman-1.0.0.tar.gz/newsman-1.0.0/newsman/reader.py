# -*- coding: utf-8 -*-
from .factories import build_factories
from .processor import Processor
from .page import Page

class Reader(Processor):
    """Concrete class for web reading. """

    def __init__(self, config, factories=None):
        """Object initialization.

        Args:
            config (dict): Configuration parameters.
            factories (dict): Set of functions for component initialization.
        """

        if factories is None:
            factories = build_factories()

        super().__init__(config, factories)

    def make_obj(self, input):
        """Implements concrete creation of <Page> object."""

        page = Page(*input)

        return page
