[![Latest Version](https://img.shields.io/pypi/v/noizze-crawler.svg)](https://pypi.org/project/noizze-crawler/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)


# NOIZZE Crawler

A web page crawler PyPI Package which returns (title(og, head), image(og, meta), description(og, meta)).

## Dependency
* BeautifulSoup4

## Installation
Run the folowing to install:

```shell
pip install noizze-crawler
```

## Usage

```python
import noizze_crawler as nc
import sys


if __name__ == '__main__':
    url = 'https://dvdprime.com/g2/bbs/board.php?bo_table=comm&wr_id=20525678'

    try:
        (title, desc, image_url, html) = nc.crawler(url)

    except nc.HostNotFound as e:
        print("Host Not Found")
        sys.exit(1)
    except nc.HTTPError as e:
        print("HTTP {}".format(e))
        sys.exit(1)

    print(title, desc, image_url)  # html
```
