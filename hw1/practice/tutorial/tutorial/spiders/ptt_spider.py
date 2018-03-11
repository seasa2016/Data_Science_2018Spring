import scrapy 

class PttSpider(scrapy.Spider):
    name = "ptt"
    allowes_domains = ["ptt.cc"]
    start_urls = [
        "https://www.ptt.cc/bbs/LoL/index.html"
    ]
    
    def parse(self,response):
        for sel in response.xpath('//ul/li'):
            title = sel.xpath('a/text()').extract()
            link  = sel.xpath('a/@href').extract()
            desx  = sel.xpath('text()').extract()
            print(title,link,desx)