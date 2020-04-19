# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from shutil import which


class CoinSpider(scrapy.Spider):
    name = 'historical_data'
    allowed_domains = ['https://www.investagrams.com/']
    start_urls = [
        'https://www.investagrams.com/'
    ]

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # chrome_path = which("chromedriver")
        # driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver = webdriver.Chrome(options=chrome_options)

        driver.implicitly_wait(60)
        driver.set_window_size(1920, 1080)

        driver.get('https://www.investagrams.com/Login/')
        driver.find_element_by_css_selector('[type=text]').send_keys('json.panganiban@gmail.com')
        driver.find_element_by_css_selector('[type=password]').send_keys('Jilter10')
        driver.find_element_by_css_selector('.investa-login--btn-login').click()

        searchbar = driver.find_element_by_xpath('(//input[@data-ng-model="SearchBar.Request.Keyword"])[2]')
        searchbar.send_keys('DITO')
        searchbar.send_keys(Keys.ENTER)

        self.html = driver.page_source

        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        for data in resp.xpath('//table[@id="HistoricalDataTable"]/tbody/tr'):
            yield {
                'last_price': data.xpath('.//td[1]/text()').get(),
                'change': data.xpath('.//td[2]/text()').get(),
                'percent_change': data.xpath('.//td[3]/text()').get(),
                'open': data.xpath('.//td[4]/text()').get(),
                'low': data.xpath('.//td[5]/text()').get(),
                'high': data.xpath('.//td[6]/text()').get(),
                'volume': data.xpath('.//td[7]/text()').get(),
                'net_foreign': data.xpath('.//td[8]/text()').get(),
            }
