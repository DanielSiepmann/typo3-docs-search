#!/bin/env python

import scrapy


class TYPO3VersionSpider(scrapy.Spider):
    name = 'typo3versionspider'
    # TODO: Define another start url to determien all documentations to crawl
    start_urls = [
        # 'https://docs.typo3.org/typo3cms/TCAReference/',
        # 'https://docs.typo3.org/typo3cms/TyposcriptReference/',
        'https://docs.typo3.org/typo3cms/TyposcriptReference/Setup/Config/Index.html',
    ]

    # Will fetch all possible versions for the current documentation.
    def parse(self, response):
        versions_url = 'https://docs.typo3.org/services/ajaxversions.php?url='
        versions_url = versions_url + response.url

        # yield scrapy.Request(
        #     versions_url,
        #     callback=self.parse_possible_versions
        # )

        yield scrapy.Request(
            response.url,
            callback=self.parse_page
        )

    # Parse possible versions for a single documentation.
    def parse_possible_versions(self, response):
        for version in response.css('a'):
            if version.css('::text').extract_first().find('In one file:') == -1:
                full_url = response.urljoin(
                    version.css('::attr(href)').extract_first()
                )
                yield scrapy.Request(
                    full_url,
                    callback=self.parse_version_main_navigation
                )

    # Parse the current documentation in current version
    def parse_version_main_navigation(self, response):
        for href in response.css('.wy-menu a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_page)

    # Parse a single page with no further navigation
    def parse_page(self, response):
        # Valid for all entries
        doc = response.css('.project').xpath('a/text()').extract_first().strip()
        version = next(
            s for s in response.css('.rst-current-version::text').extract()
            if s.strip()
        ).strip().replace('v: ', '')

        # TODO: Get all "search entries"
        for section in response.css('.section .section'):
            if not section.xpath('h3'):
                continue

            title = section.css('.toc-backref::text').extract_first()
            content = ' '.join(
                section.xpath('*[contains(@class, "container")]').css('::text')
                .extract()).strip()
            url = response.urljoin(
                section.css('.headerlink::attr(href)').extract_first()
            )
            tags = []

            yield {
                'doc': doc,
                'version': version,
                'title': title,
                'content': content,
                'url': url,
                'tags': tags,
            }
