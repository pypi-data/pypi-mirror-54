# Newsman

A tool for scraping news from web.

There is no AI here, just good old-fashioned if-else rules.

# Usage

Basic usage:

```
import newsman

# start reading
src = 'https://www.bbc.com'
news = newsman.read(src)

# show articles
for article in news:
    print(f'Url: {article.url.url}')
    print(f'Title: {article.title}')
    print(f'Text: {article.text}')
    print(f'Main image: {article.main_image}')
```

Customizing configuration:

```
import newsman

# get configuration
config = newsman.get_config()

# add a proxy for connection
config['proxies'] = proxies

# update accepted/rejected domains
config['accepted_domains'] = ['a-good-site.com', 'the-best-one.org']
config['rejected_domains'] += ['bad.com', 'very.bad.biz']

# override default values for web retrieval
config['link_depth'] = 2            # crawling depth level
config['scan_limit'] = 10           # max. number of scanned sites

# set pipes
pipes = ['byte2html', 'html2text', 'text2title', 'html2image']
news = newsman.News(config, pipes)

src = 'https://www.bbc.com'
pages = news(src)
```

Proxy information is formatted according to [Requests format](https://requests.kennethreitz.org/en/master/user/advanced/#proxies).

# Installation

` pip install newsman `
