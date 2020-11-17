import scrapy
from selenium import webdriver
from urllib import parse


class TorrentkittySpider(scrapy.Spider):
    name = 'torrentkitty'
    allowed_domains = ['torrentkitty.tv']
    search_name = "变形金刚"
    search_name = parse.quote(search_name)
    start_urls = ['https://www.torrentkitty.tv/search/{}'.format(search_name)]

    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        self.browser = webdriver.Chrome(executable_path="/Users/winters/software/chromedriver",
                                        chrome_options=option)
        super().__init__()

    def start_requests(self):
        for url in self.start_urls:
            response = scrapy.Request(url, callback=self.parse)
            yield response

    def close(self, spider):
        self.browser.quit()

    def parse(self, response):
        names = response.xpath("//table[@id='archiveResult']//tr//td[@class='name']/text()").extract()
        sizes = response.xpath("//table[@id='archiveResult']//tr//td[@class='size']/text()").extract()
        dates = response.xpath("//table[@id='archiveResult']//tr//td[@class='date']/text()").extract()
        torrents = response.xpath("//table[@id='archiveResult']//tr//td[@class='action']/a[2]/@href").extract()
        for name, size, date, torrent in zip(names, sizes, dates, torrents):
            yield {
                "name": name,
                "size": size,
                "date": date,
                "torrent": torrent
            }
        next_no = response.xpath("//div[@class='pagination']/a[last()]/@href").extract_first()
        if next_no is not None:
            url = 'https://www.torrentkitty.tv/search/{}/{}'.format(self.search_name, next_no)
            yield scrapy.Request(url=url, callback=self.parse)
