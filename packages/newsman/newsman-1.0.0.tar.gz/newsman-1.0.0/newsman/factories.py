# -*- coding: utf-8 -*-
"""This module provides a way to initialize components for processing
pipeline.

Init functions are stored into a dictionary which can be used by `Pipeline` to
load components on demand.
"""
from .pipeline import Byte2html, Html2text, Html2image, Text2title

def build_factories():
    """Creates default factories for Processor."""

    factories = {
        'byte2html': lambda config: Byte2html(config),
        'html2text': lambda config: Html2text(config),
        'html2image': lambda config: Html2image(config),
        'text2title': lambda config: Text2title(config)
    }

    return factories
