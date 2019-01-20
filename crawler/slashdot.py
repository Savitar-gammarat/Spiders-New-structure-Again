#coding:utf-8
import sys
sys.path.append("..")
from config import SlashDotConfig as sd
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree
from datetime import datetime


class SlashDot(object):
    url = 'https://slashdot.org/'
    def first_requests(self):
        response = Req(self.url).get_select()
        selector = etree.HTML(response.text)
        part = selector.xpath('//div[@id="firehoselist"]/article')
        for article in part:
            item = dict()
            item['title'] = xpath_out(article.xpath('header/h2/span[1]/a/text()'))
            item['link'] = xpath_out(article.xpath('header/h2/span[1]/a/@href'))
            item['datetime'] = xpath_out(article.xpath('header/div[@class="details"]/span[2]/time/text()')).replace("@","")

            item['datetime'] = str(datetime.strptime(item['datetime'], 'on %A %B %d, %Y %I:%M%p'))
            item['link'] = "https://" + item['link']
            yield item


def run():
    sets = Pipeline(sd.site_id, sd.site_name).structure_set()
    Pipeline(sd.site_id, sd.site_name).open_spider(sets)

    for item in SlashDot().first_requests():
        Pipeline(sd.site_id, sd.site_name).process_item(item)
        Pipeline(sd.site_id, sd.site_name).upload_item(item, sets)

    try:
        Pipeline(sd.site_id, sd.site_name).close_spider()
    except:
        Logger().setLogger(sd.log_path, 4, "Failed to close spider,db_session may failed")


if __name__ == '__main__':
    # sd.log_path = "../" + sd.log_path
    run()
