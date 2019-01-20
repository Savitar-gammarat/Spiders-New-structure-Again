#coding:utf-8
import sys
sys.path.append("..")
from config import NewYorkTimeConfig as nyk
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree

class NewYork(object):
    url = 'https://www.nytimes.com/trending/'
    def first_requests(self):
        response = Req(self.url, proxy=True).get_select()
        selector = etree.HTML(response.text)
        partA = selector.xpath('//main[@id="site-content"]/div/div[2]/div[2]/div[1]/div/article')
        partB = selector.xpath('//main[@id="site-content"]/div/div[2]/div[2]/div[1]/div/ul/li')

        for part in partA:
            item = dict()
            item['title'] = xpath_out(part.xpath('a[2]/div/h2/text()'))
            item['link'] = xpath_out(part.xpath('a[2]/@href'))
            yield item

        for part in partB:
            item = dict()
            item['title'] = xpath_out(part.xpath('a/div/h1/text()'))
            item['link'] = xpath_out(part.xpath('a/@href'))
            yield item


def run():
    sets = Pipeline(nyk.site_id, nyk.site_name).structure_set()
    Pipeline(nyk.site_id, nyk.site_name).open_spider(sets)

    for item in NewYork().first_requests():
        Pipeline(nyk.site_id, nyk.site_name).process_item(item)
        Pipeline(nyk.site_id, nyk.site_name).upload_item(item, sets)

    try:
        Pipeline(nyk.site_id, nyk.site_name).close_spider()
    except:
        Logger().setLogger(nyk.log_path, 4, "Failed to close spider,db_session may failed")

if __name__ == '__main__':
    # nyk.log_path = "../" + nyk.log_path
    run()
