#coding:utf-8
import sys
sys.path.append("..")
from config import EconomistConfig as ec
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree
from datetime import datetime

class Economic(object):
    url = 'https://www.economist.com/latest/'

    def first_requests(self):
        response = Req(url=self.url, proxy=True).get_select()
        selector = etree.HTML(response.text)
        articles = selector.xpath('//div[@class="teaser-list"]/article')

        for article in articles:
            item = dict()
            item['title'] = xpath_out(article.xpath('a/div[2]/h3/span[2]/text()'))
            item['link'] = "https://www.economist.com" + xpath_out(article.xpath('a/@href'))
            item['datetime'] = xpath_out(article.xpath('a/div[2]/div[@class="teaser__datetime"]/time/@datetime')).encode('utf8').decode('utf8')
            item['datetime'] = str(datetime.strptime(item['datetime'], '%Y-%m-%dT%H:%M:%SZ'))
            yield item

def run():
    sets = Pipeline(ec.site_id, ec.site_name).structure_set()
    Pipeline(ec.site_id, ec.site_name).open_spider(sets)

    for item in Economic().first_requests():
        Pipeline(ec.site_id, ec.site_name).process_item(item)
        Pipeline(ec.site_id, ec.site_name).upload_item(item, sets)

    try:
        Pipeline(ec.site_id, ec.site_name).close_spider()
    except:
        Logger().setLogger(ec.log_path, 4, "Failed to close spider,db_session may failed")

if __name__ == '__main__':
    # ec.log_path = "../" + ec.log_path
    run()
