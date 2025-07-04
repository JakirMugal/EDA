import scrapy
from urllib.parse import urlencode
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','..', 'common_lib')))
import text_parse


class SwiggySpider(scrapy.Spider):
    name = "swiggy"
    input_zip = "302013"
    headers = {
            '__fetch_req__': 'true',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.swiggy.com',
            'platform': 'dweb',
            'priority': 'u=1, i',
            'referer': 'https://www.swiggy.com/restaurants',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        }
    def start_requests(self):
        url = 'https://www.swiggy.com/dapi/misc/place-autocomplete'
        params = {
            'input': self.input_zip,
            'types': '',
        }
        # Scrapy handles query parameters using the `urlencode` approach manually
        yield scrapy.Request(
            url=f"{url}?{urlencode(params)}",
            method='GET',
            headers=self.headers,
            callback=self.parse,
            dont_filter=True,
            meta={'handle_httpstatus_all': True},
        )


    def parse(self, response):
        data = response.json()['data']
        place_id = data[0]['place_id'] 
        assert place_id, "place_id not founded"
        params = {
                'place_id': 'ChIJzVpAu4CtbTkRYTkN4ZsZYGQ',
            }
        url = "https://www.swiggy.com/dapi/misc/address-recommend"

        yield scrapy.Request(
            url=f"{url}?{urlencode(params)}",
            method='GET',
            headers=self.headers,
            callback=self.parse_address,
            dont_filter=True,
        )
    def parse_address(self,response):
        data=response.json()['data'][0]
        location_json = data['geometry']['location'] 
        import pdb; pdb.set_trace()
        params = {
                'is-seo-homepage-enabled': 'true',
                'page_type': 'DESKTOP_WEB_LISTING',
                **location_json
            }
        url = "https://www.swiggy.com/dapi/restaurants/list/v5"
        yield scrapy.Request(
            url=f"{url}?{urlencode(params)}",
            method='GET',
            headers=self.headers,
            callback=self.parse_restaurant,
            dont_filter=True,
            meta={"params":params},
        )
        
    def parse_restaurant(self,response):
        data=response.json()

        import pdb; pdb.set_trace()
