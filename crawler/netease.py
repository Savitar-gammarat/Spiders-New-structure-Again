#coding:utf-8
import sys
sys.path.append("..")
from config import NeteaseConfig as ne
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree
import re

class Netease(object):
    url = 'http://news.163.com/rank/'

    def first_requests(self):
        response = Req(self.url).get_select()
        selector = etree.HTML(response.text)
        partA = selector.cssselect('body > div.area.areabg1 > div:nth-child(2) > div > div.tabContents.active > table > tr')
        partA.pop(0)
        for part in partA:
            item = dict()
            item['link'] = part.xpath('td[1]/a/@href')[0]
            item['title'] = part.xpath('td[1]/a/text()')[0]
            item['hot'] = part.xpath('td[2]/text()')[0]
            item['hot'] = round(int(item['hot']) / 10000, 2)
            yield item

        partB = selector.cssselect('body > div.area.areabg1 > div:nth-child(6) > div > div:nth-child(3) > table > tr')
        partB.pop(0)
        for part in partB:
            item = dict()
            item['link'] = part.xpath('td[1]/a/@href')[0]
            item['title'] = part.xpath('td[1]/a/text()')[0]
            item['hot'] = part.xpath('td[2]/text()')[0]
            item['hot'] = round(int(item['hot']) / 10000, 2)
            yield item


def run():
    sets = Pipeline(ne.site_id, ne.site_name).structure_set()
    Pipeline(ne.site_id, ne.site_name).open_spider(sets)

    for item in Netease().first_requests():
        Pipeline(ne.site_id, ne.site_name).process_item(item)
        Pipeline(ne.site_id, ne.site_name).upload_item(item, sets)

    try:
        Pipeline(ne.site_id, ne.site_name).close_spider()
    except:
        Logger().setLogger(ne.log_path, 4, "Failed to close spider,db_session may failed")
        pass


if __name__ == '__main__':
    # ne.log_path = "../" + ne.log_path
    run()
