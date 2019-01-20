#coding:utf-8
import sys
sys.path.append("..")
from config import HuanqiuConfig as hq
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree
import re


class Huanqiu(object):
    url = 'http://www.huanqiu.com/'

    def first_requests(self):
        response = Req(self.url).get_select()
        selector = etree.HTML(response.content)
        detail_urls = []
        partA = selector.xpath('/html/body/div[2]/div[5]/div/div[1]/div[2]/div[2]/dl//a/@href')
        for part in partA:
            detail_urls.append(part)

        partB = selector.xpath('/html/body/div[2]/div[5]/div/div[1]/div[3]/div[3]/div//a/@href')
        for part in partB:
            detail_urls.append(part)

        return detail_urls

    def second_requests(self, detail_urls):
        for detail_url in detail_urls:
            response = Req(detail_url).get_select()
            selector = etree.HTML(response.content)
            item = dict()
            item['link'] = detail_url
            item['title'] = xpath_out(selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/h1/text()'))
            if item['title']:
                item['datetime'] = xpath_out(selector.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[1]/span[1]/text()'))
            else:
                item['title'] = xpath_out(selector.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/h1/text()'))
                if item['title']:
                    item['datetime'] = xpath_out(selector.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[1]/span[1]/text()'))
                else:
                    item['title'] = xpath_out(selector.xpath('/html/body/div[4]/div/div[2]/div[1]/h1/text()'))
                    item['datetime'] = xpath_out(selector.xpath('//*[@id="time"]/text()'))
            yield item

    def process_item(self, item):
        # 对item['datetime']进行格式化处理
        datetime_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', re.S)
        datetime_patternB = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', re.S)
        if type(item['title']) == str:
            if re.match(datetime_pattern, item['datetime']) or re.match(datetime_patternB, item['datetime']):
                pass
            else:
                item['datetime'] = None
        else:
            pass

        if item['title'] is not None:
            return item

def run():
    sets = Pipeline(hq.site_id, hq.site_name).structure_set()
    Pipeline(hq.site_id, hq.site_name).open_spider(sets)

    detail_url = Huanqiu().first_requests()

    for item in Huanqiu().second_requests(detail_url):
        Huanqiu().process_item(item)

        Pipeline(hq.site_id, hq.site_name).process_item(item)
        Pipeline(hq.site_id, hq.site_name).upload_item(item, sets)

    try:
        Pipeline(hq.site_id, hq.site_name).close_spider()
    except:
        Logger().setLogger(hq.log_path, 4, "Failed to close spider,db_session may failed")
        pass


if __name__ == '__main__':
    # hq.log_path = "../" + hq.log_path
    run()
