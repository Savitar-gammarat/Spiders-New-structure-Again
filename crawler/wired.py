#coding:utf-8
import sys
sys.path.append("..")
from config import WiredConfig as wd
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree

class Wired(object):
    url = 'https://www.wired.com/most-recent/'

    def first_requests(self):
        response = Req(self.url, proxy=True).get_select()
        selector = etree.HTML(response.content)
        part = selector.xpath('//div[@class="archive-listing-component"]/div[1]/ul/li')
        for article in part:
            item=dict()
            item['link'] = "https://www.wired.com" + xpath_out(article.xpath('div[@class="archive-item-component__info"]/a/@href')).encode('utf8').decode('utf8')
            item['title'] = xpath_out(article.xpath('div[@class="archive-item-component__info"]/a/h2/text()'))
            yield item

def run():
    sets = Pipeline(wd.site_id, wd.site_name).structure_set()
    Pipeline(wd.site_id, wd.site_name).open_spider(sets)

    for item in Wired().first_requests():
        Pipeline(wd.site_id, wd.site_name).process_item(item)
        Pipeline(wd.site_id, wd.site_name).upload_item(item, sets)

    try:
        Pipeline(wd.site_id, wd.site_name).close_spider()
    except:
        Logger().setLogger(wd.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # wd.log_path = "../" + wd.log_path
    run()
