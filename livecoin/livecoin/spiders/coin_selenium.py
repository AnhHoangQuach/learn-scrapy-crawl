# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which


class CoinSpiderSelenium(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ['http://www.livecoin.net/en']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        chrome_path = which("chromedriver")
        driver = webdriver.Chrome(
            executable_path=chrome_path, options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get("https://www.livecoin.net/en")

        rur_tab = driver.find_elements_by_class_name("filterPanelItem___2z5Gb")
        rur_tab[4].click()

        self.html = driver.page_source
        driver.close()

    # script = '''
    #     function main(splash, args)
    #         splash.private_mode_enabled = false
    #         url = args.url
    #         assert(splash:go(url))
    #         assert(splash:wait(1))
    #         rur_tab = assert(splash:select_all(".filterPanelItem___2z5Gb"))
    #         rur_tab[5]:mouse_click()
    #         assert(splash:wait(1))
    #         splash:set_viewport_full()
    #         return splash:html()
    #     end

    # '''

    # def start_requests(self):
    #     yield SplashRequest(url="https://www.livecoin.net/en", callback=self.parse, endpoint="execute", args={
    #         'lua_source': self.script
    #     })

    def parse(self, response):
        resp = Selector(text=self.html)
        for currency in resp.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield {
                'currency pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get()
            }
