#coding:utf-8
import sys
sys.path.append("..")
from config import FortuneConfig as fo
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree


class Fortune(object):
    url = 'http://www.fortune.com/'

    def first_requests(self):

        response = Req(self.url, proxy=True).get_select()
        selector = etree.HTML(response.text)
        set = []
        partA = selector.xpath('//div[@class="column text-align-left visible-desktop visible-mobile last-column"]/div[@class="column-tout   "]')
        partB = selector.xpath('//div[@class="column large-headline"]/div[@class="column-tout   "]')
        partC = selector.xpath('//div[@class="column column-feed"]/div[@class="column-tout   "]')

        for part in partA:
            item = dict()
            item['title'] = xpath_out(part.xpath('div[1]/a/text()')).strip()
            item['link'] = "http://www.fortune.com/" + xpath_out(part.xpath('div[1]/a/@href'))
            if not item['link'] in set:
                set.append(item['link'])
                yield item

        for part in partB:
            item = dict()
            item['title'] = xpath_out(part.xpath('div[1]/a/text()')).strip()
            item['link'] = "http://www.fortune.com/" + xpath_out(part.xpath('div[1]/a/@href'))
            if not item['link'] in set:
                set.append(item['link'])
                yield item


        for part in partC:
            item = dict()
            item['title'] = xpath_out(part.xpath('div[1]/a/text()')).strip()
            item['link'] = "http://www.fortune.com/" + xpath_out(part.xpath('div[1]/a/@href'))
            if not item['link'] in set:
                set.append(item['link'])
                yield item


def run():
    sets = Pipeline(fo.site_id, fo.site_name).structure_set()
    Pipeline(fo.site_id, fo.site_name).open_spider(sets)

    for item in Fortune().first_requests():
        Pipeline(fo.site_id, fo.site_name).process_item(item)
        Pipeline(fo.site_id, fo.site_name).upload_item(item, sets)

    try:
        Pipeline(fo.site_id, fo.site_name).close_spider()
    except:
        Logger().setLogger(fo.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # fo.log_path = "../" + fo.log_path
    run()
