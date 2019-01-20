#coding:utf-8
import sys
sys.path.append("..")
from config import BBCConfig as bbc
from logger import Logger
from pipelines import Pipeline
from func import Req,css_out
from lxml import etree

class BBC(object):
    url = 'https://www.bbc.com/news'

    def first_requests(self):
        response = Req(url=self.url, proxy=True).get_select()
        if response is not None:
            selector = etree.HTML(response.content)
            partA = selector.cssselect('.nw-c-most-watched div ol li')
            partB = selector.cssselect('.nw-c-most-read div div:nth-child(2) ol li')
            partA_url = []
            partB_url = []

            for part in partA:
                A = css_out(part.xpath('span/div/a/@href'))
                if A is not None:
                    partA_url.append('https://www.bbc.com' + A)
            for part in partB:
                B = css_out(part.xpath('span/div/a/@href'))
                if B is not None:
                    partB_url.append('https://www.bbc.com' + B)

            urls = dict()
            urls['A'] = partA_url
            urls['B'] = partB_url
            return urls

    def second_requests(self, urls):
        for url in urls['A']:
            response = Req(url=url, proxy=True).get_select()
            if response is not None:
                selector = etree.HTML(response.content)
                item = dict()
                item['title'] = css_out(selector.cssselect('.vxp-media__body h1')).text
                item['link'] = response.url
                yield item

        for url in urls['B']:
            response = Req(url=url, proxy=True).get_select()
            if response is not None:
                selector = etree.HTML(response.content)
                item = dict()
                item['title'] = css_out(selector.cssselect('.story-body__h1'))
                if item['title'] != None:
                    item['title'] = item['title'].text
                    item['link'] = response.url
                    yield item

def run():
    sets = Pipeline(bbc.site_id, bbc.site_name).structure_set()
    Pipeline(bbc.site_id, bbc.site_name).open_spider(sets)

    urls = BBC().first_requests()
    for item in BBC().second_requests(urls):
        Pipeline(bbc.site_id, bbc.site_name).process_item(item)
        Pipeline(bbc.site_id, bbc.site_name).upload_item(item, sets)

    try:
        Pipeline(bbc.site_id, bbc.site_name).close_spider()
    except:
        Logger().setLogger(bbc.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # bbc.log_path = "../" + bbc.log_path
    run()