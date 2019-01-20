#coding:utf-8
import sys
sys.path.append("..")
from config import XinHuaConfig as xh
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree
import datetime
import re


class Xinhua(object):
    url = 'http://www.news.cn/'
    today = str(datetime.date.today()).replace('-','')
    re_title = re.compile(r'.{4,}',re.S)

    def first_requests(self):
        response = Req(self.url).get_select()
        selector = etree.HTML(response.content)
        hrefs = selector.xpath('//*[@id="hpart2L"]//a')
        url_set = []
        for href in hrefs:
            if not href in url_set:
                url_set.append(href)  #去重操作

                item = dict()
                item['title'] = xpath_out(href.xpath('text()'))
                item['link'] = xpath_out(href.xpath('@href'))

                if item['title'] != None:
                    if re.match(self.re_title, item['title']):
                        yield item


def run():
    sets = Pipeline(xh.site_id, xh.site_name).structure_set()
    Pipeline(xh.site_id, xh.site_name).open_spider(sets)

    for item in Xinhua().first_requests():
        Pipeline(xh.site_id, xh.site_name).process_item(item)
        Pipeline(xh.site_id, xh.site_name).upload_item(item, sets)

    try:
        Pipeline(xh.site_id, xh.site_name).close_spider()
    except:
        Logger().setLogger(xh.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # xh.log_path = "../" + xh.log_path
    run()
