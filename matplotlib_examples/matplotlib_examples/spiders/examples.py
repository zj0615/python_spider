import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import ExamplesItem

class ExamplesSpider(scrapy.Spider):
    name = 'examples'
    allowed_domains = ['matplotlib.org']
    start_urls = ['https://matplotlib.org/examples/index.html']

    def parse(self, response):
        le = LinkExtractor(restrict_css='div.toctree-wrapper.compound li.toctree-12')
        print(len(le.extract_links(response)))
        links = le.extract_links(self, response)
        for link in links :
            print(link)
            yield scrapy.Request(link.url, callback=self.parse_example)

    def parse_example(self, response):
        href = response.css('a.reference.external::attr(href)').extract_first()
        url = response.urljoin(href)
        print(url)
        example = ExamplesItem()
        example['file_urls'] = [url]
        return example