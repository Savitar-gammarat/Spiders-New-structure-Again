#coding:utf-8
import sys
sys.path.append("..")
from config import DoNewsConfig as dn
from logger import Logger
from pipelines import Pipeline
from func import Req,xpath_out
from lxml import etree


class DoNews(object):
    url = 'http://www.donews.com/'

    def first_requests(self):
        response = Req(self.url).get_select()

        if response is not None:
            selector = etree.HTML(response.text)
            partA = selector.xpath('/html/body/div[5]/div[3]/div[2]/dl')
            partB = selector.xpath('/html/body/div[9]/div[2]/div/dl')
            for part in partA:
                item = dict()
                item['link'] = xpath_out(part.xpath('dd/h3/a/@href'))
                item['title'] = xpath_out(part.xpath('dd/h3/a/text()'))
                yield item

            for part in partB:
                item = dict()
                item['link'] = xpath_out(part.xpath('dd/h3/a/@href'))
                item['title'] = xpath_out(part.xpath('dd/h3/a/text()'))
                yield item

def run():
    sets = Pipeline(dn.site_id, dn.site_name).structure_set()
    Pipeline(dn.site_id, dn.site_name).open_spider(sets)

    for item in DoNews().first_requests():
        Pipeline(dn.site_id, dn.site_name).process_item(item)
        Pipeline(dn.site_id, dn.site_name).upload_item(item, sets)

    try:
        Pipeline(dn.site_id, dn.site_name).close_spider()
    except:
        Logger().setLogger(dn.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # dn.log_path = "../" + dn.log_path
    run()
