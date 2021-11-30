import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating', headers={'User-Agent': self.user_agent})

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//h3[@class="lister-item-header"]/a'), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(
            restrict_xpaths='(//a[@class="lister-page-next next-page"])[2]'), process_request='set_user_agent'),
    )

    def set_user_agent(self, request, response):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath("//h1[@data-testid='hero-title-block__title']/text()").get(),
            'year': response.xpath("(//ul[@data-testid='hero-title-block__metadata']/li/span)[1]/text()").get(),
            'duration': "".join(response.xpath("(//ul[@data-testid='hero-title-block__metadata']/li)[last()]/text()").extract()),
            'genre': response.xpath(
                "//div[@data-testid='genres']/a/span/text()").getall(),
            'rating': response.xpath("(//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span)[1]/text()").get(),
            'movie_url': response.url,
        }
