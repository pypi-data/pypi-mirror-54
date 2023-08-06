# -*- coding: utf-8 -*-
import json
from os import path
from sys import prefix

RESOURCES_DIR = path.join(prefix, 'newsman.d')

def load_charmap():
    """Loads internally stored map of html codes."""
    filename = path.join(RESOURCES_DIR, 'htmlcodes.json')
    with open(filename, 'r', encoding='utf-8') as file:
        codes = json.load(file)['codes']

    return codes

def load_stopwords(lang):
    """Loads internally stored list of stopwords."""

    filename = path.join(RESOURCES_DIR, f'stopwords-{lang}.txt')

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            stopwords = file.read().split('\n')
    except FileNotFoundError:
        stopwords = []

    return stopwords

def load_blacklist():
    """Loads internally stored url filters."""

    filename = path.join(RESOURCES_DIR, 'blacklist.txt')

    with open(filename, 'r', encoding='utf-8') as file:
        blacklist = file.read().splitlines()

    return blacklist

def init_config():

    config = {
        'charmap': load_charmap(),
        'rejected_domains': load_blacklist(),
        'accepted_domains': [],
        'scan_limit': None,
        'recursive': True,
        'link_depth': 2,
        'text_len_thr': 300,
        'title_len_thr': 3,
        'hx_len_thr': 30,
        'conn_timeout': 3.5,
        'limit': None,
        'delay': True
    }

    return config
