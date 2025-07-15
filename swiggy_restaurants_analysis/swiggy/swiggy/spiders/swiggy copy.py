import scrapy
from urllib.parse import urlencode
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','..', 'common_lib')))
import text_parse


class SwiggySpider(scrapy.Spider):
    name = "swiggy_jaipur"
    start_urls=["https://www.swiggy.com/city/{}/order-online"]
    city = "jaipur"
    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        }
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0].format(self.city),callback=self.parse,headers=self.headers)
    
    def parse(self, response):
        script_text = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        pageoffset = text_parse.get_all_values_between_string(t1='{',t2='}',text=script_text,find_word='pageOffset')
        assert pageoffset, "PageOffset not founded"
        nextoffset = pageoffset[0]['nextOffset']
        
        import pdb; pdb.set_trace()