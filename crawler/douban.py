#coding:utf-8
import sys
sys.path.append("..")
from config import DoubanConfig as do
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree
import re

class Douban(object):
    url_explore = 'https://www.douban.com/explore/'
    url_home = 'https://www.douban.com/'
    hot_pattern = re.compile(r'.*?(\d*)人浏览$',re.S)


    def first_requests(self):
        response = Req(self.url_explore).get_select()
        selector = etree.HTML(response.text)
        gallery = selector.xpath('//*[@id="gallery_main_frame"]/div[@class="item"]')

        for g in gallery:
            item = dict()
            item['link'] = xpath_out(g.xpath('div[@class="bd"]/div/div[@class="title"]/a/@href'))
            item['title'] = xpath_out(g.xpath('div[@class="bd"]/div/div[@class="title"]/a/text()'))
            item['image'] = str(xpath_out(g.xpath('div[@class="bd"]/div[@class="pic"]/a/@style')))[21:-1]
            item['intro'] = xpath_out(g.xpath('div[@class="bd"]/div/p/a/text()'))
            if item['title']:
                    yield item

        home = Req(self.url_home).get_select()
        selector = etree.HTML(home.text)
        side = selector.xpath('//*[@id="anony-sns"]/div/div[2]/div[2]/ul/div/ul/li')
        for s in side:
            item = dict()
            item['link'] = xpath_out(s.xpath('a/@href'))
            item['title'] = xpath_out(s.xpath('a/text()'))
            item['hot'] = xpath_out(s.xpath('span/text()'))

            item['hot'] = re.match(self.hot_pattern, str(item['hot']))
            if item['hot'] is not None:
                item['hot'] = item['hot'].group(1)

            if item['title']:
                yield item

    def process_item(self, item):
        if not "hot" in item.keys():
            item['hot'] = None
        else:
            if item['hot'] is not None:
                item['hot'] = round(int(item['hot'])/10000, 2)

        return item


def run():
    sets = Pipeline(do.site_id, do.site_name).structure_set()
    Pipeline(do.site_id, do.site_name).open_spider(sets)

    for item in Douban().first_requests():
        Douban().process_item(item)
        Pipeline(do.site_id, do.site_name).process_item(item)
        Pipeline(do.site_id, do.site_name).upload_item(item, sets)

    try:
        Pipeline(do.site_id, do.site_name).close_spider()
    except:
        Logger().setLogger(do.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # do.log_path = "../" + do.log_path
    run()
