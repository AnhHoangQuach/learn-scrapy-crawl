import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = [
        'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//h3[@class="lister-item-header"]/a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield {
            'title': response.xpath("//h1[@data-testid='hero-title-block__title']/text()").get(),
            'year': response.xpath("(//ul[@data-testid='hero-title-block__metadata']/li/span)[1]/text()").get(),
            'duration': "".join(response.xpath("(//ul[@data-testid='hero-title-block__metadata']/li)[last()]/text()").extract()),
            'genre': response.xpath(
                "//div[@data-testid='genres']/a/span/text()").getall(),
            'rating': response.xpath("//span[@itemprop='ratingValue']/text()").get(),
            'movie_url': response.url
        }
