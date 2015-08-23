
from scrapy.spiders import Spider
from cl_jobs.items import ClJobsItem
from scrapy.selector import Selector
from scrapy.http import Request, HtmlResponse
 
class MySpider(Spider):
    name = "cl_gomi"
    allowed_domains = ["harrisonburg.craigslist.org"]
    start_urls = ["http://harrisonburg.craigslist.org/search/ela"]
    #start_urls = ["http://net.tutsplus.com"]

    def parse(self, response):

        print type(response)
        item = ClJobsItem()
        item["title"] = response.url
        item["body"] = response.body
        
        #body = '<html><body><span>good</span></body></html>'
        ext = Selector(response=response).xpath('//html/head/title/text()').extract()
        print type(ext)
        print ext

        filename = "test1.txt"
        with open(filename, 'wb') as f:
            f.write(item["title"] + "\n\n" + item["body"])\

        return item
