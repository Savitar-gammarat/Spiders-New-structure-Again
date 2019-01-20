#coding:utf-8
import sys
sys.path.append("..")
from config import ZhihuConfig as zh
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree

class Zhihu(object):
    url = 'https://www.zhihu.com/hot'
    cookies = {
      '_xsrf': 'c404292b-7b8e-4a95-a05a-65e476d76fb5',
      '_zap': 'f02b85e1-2791-4dc2-acaa-d3528d8134ef',
      'admckid': '1901191906001644282',
      'admses': '1906009576425',
      'd_c0': '"ADChmyOG2Q6PTsHPkdwUR9iQVzggBFCX8Xk=|1547895955"',
      'q_c1': '7de81d9f7756473b98551aaad9fc2815|1547895959000|1547895959000',
      'z_c0': '"2|1:0|10:1547895957|4:z_c0|92:Mi4xdnFmTEF3QUFBQUFBTUtHYkk0YlpEaVlBQUFCZ0FsVk5sVkl3WFFCSkFBUEduN1FKcDdNQ2VBdmdUYWU4TVJqUk5R|5ad2be1df85c0ebbf172adcfc685db36a76dae46325fb262d83f8a6c117dabc2"'
    }

    def first_requests(self):
        response = Req(url=self.url,cookies=self.cookies).get_select()
        selector = etree.HTML(response.content)
        sections = selector.xpath('//*[@id="TopstoryContent"]/div/section')

        for section in sections:
            item = dict()
            item['title'] = xpath_out(section.xpath('div[2]/a/h2/text()'))
            item['link'] = xpath_out(section.xpath('div[2]/a/@href'))
            item['hot'] = float(xpath_out(section.xpath('div[2]/div/text()'))[:-3])


            if item['title'] is not None:
                if item['hot'] <= 150:
                    item['home'] = False

                yield item
            else:
                Logger().setLogger(zh.log_path, 2, "Item's title is None, item is " + item)
                pass

def run():
    sets = Pipeline(zh.site_id, zh.site_name).structure_set()

    Pipeline(zh.site_id, zh.site_name).open_spider(sets)
    for item in Zhihu().first_requests():
        Pipeline(zh.site_id, zh.site_name).process_item(item)

        Pipeline(zh.site_id, zh.site_name).upload_item(item, sets)

    try:
        Pipeline(zh.site_id, zh.site_name).close_spider()
    except:
        Logger().setLogger(zh.log_path, 2, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # zh.log_path = "../" + zh.log_path
    run()
