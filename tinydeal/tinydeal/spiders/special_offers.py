import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.tinydeal.com.hk/specials.html']
    start_urls = ['http://www.tinydeal.com.hk/specials.html/']

    def parse(self, response):
        pass
