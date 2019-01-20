#coding:utf-8
import sys
sys.path.append("..")
from config import TimeConfig as time
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree

class Time(object):
    url = 'http://time.com/'
    def first_requests(self):
        response = Req(self.url, proxy=True).get_select()
        selector = etree.HTML(response.text)
        partA = selector.xpath('//div[@class="column text-align-left visible-desktop visible-mobile last-column"]/div[@class="column-tout  "]')
        partB = selector.xpath('//div[@class="column text-align-left visible-desktop"]/div[@class="column-tout  "]')

        for part in partA:
            item = dict()
            item['title'] = xpath_out(part.xpath('div[@class="column-tout-info "]/div/div/a/text()')).strip()
            item['link'] = "http://time.com" + xpath_out(part.xpath('div[@class="column-tout-info "]/div/div/a/@href'))
            yield item

        for part in partB:
            item = dict()
            item['title'] = xpath_out(part.xpath('div[@class="column-tout-info "]/div/div[1]/a/text()')).strip()
            item['link'] = "http://time.com" + xpath_out(part.xpath('div[@class="column-tout-info "]/div/div[1]/a/@href'))
            yield item


def run():
    sets = Pipeline(time.site_id, time.site_name).structure_set()
    Pipeline(time.site_id, time.site_name).open_spider(sets)

    for item in Time().first_requests():
        Pipeline(time.site_id, time.site_name).process_item(item)
        Pipeline(time.site_id, time.site_name).upload_item(item, sets)

    try:
        Pipeline(time.site_id, time.site_name).close_spider()
    except:
        Logger().setLogger(time.log_path, 4, "Failed to close spider,db_session may failed")

if __name__ == '__main__':
    # time.log_path = "../" + time.log_path
    run()
