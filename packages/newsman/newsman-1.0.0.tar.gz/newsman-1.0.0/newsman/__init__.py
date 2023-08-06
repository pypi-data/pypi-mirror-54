# -*- coding: utf-8 -*-
"""This module provides API for newsman package."""
from .utils.config import init_config
from .news import News

__title__ = 'newsman'
__author__ = 'Andrea Capitanelli'
__license__ = 'MIT'
__copyright__ = "Copyright 2019, Newsman"

def read(src, config=None):
    """Reads content from src url and generates a collection of Page objects.

    Default pipeline is used for processing.
    """

    if config is None:
        config = init_config()

    pipes = ['byte2html', 'html2text', 'text2title', 'html2image']
    news = News(config, pipes)

    pages = news(src)

    return pages

def get_config():
    """Provides initial configuration."""
    return init_config()
