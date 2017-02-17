Goal
====

The goal of this project is to provide a full stack of software to allow anyone to search
`docs.typo3.org`_.

The current stack will look like:

- `Scrapy`_ for crawling the docs.

- `Elasticsearch`_ as storage and search server.

- `elasticorn`_ for zero downtime and mapping for `Elasticsearch`_.

Currently nothing is decided about search frontend.

.. _docs.typo3.org: https://docs.typo3.org/
.. _Scrapy: https://scrapy.org/
.. _Elasticsearch: https://www.elastic.co/products/elasticsearch
.. _elasticorn: http://elasticorn.net/
