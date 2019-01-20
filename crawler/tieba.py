#coding:utf-8
import sys
sys.path.append("..")
from config import TiebaConfig as tb
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
import json

class Tieba(object):
    url = 'http://tieba.baidu.com/hottopic/browse/topicList'

    def first_requests(self):
        response = Req(self.url).get_select()
        topics = json.loads(response.content.decode('utf8'))['data']['bang_topic']['topic_list']
        for topic in topics:
            item = dict()
            item['title'] = topic['topic_name']
            item['link'] = topic['topic_url'].replace("&amp;", "&")
            item['hot'] = topic['discuss_num']
            item['hot'] = round(int(item['hot']) / 10000, 2)
            yield item

def run():
    sets = Pipeline(tb.site_id, tb.site_name).structure_set()
    Pipeline(tb.site_id, tb.site_name).open_spider(sets)

    for item in Tieba().first_requests():
        Pipeline(tb.site_id, tb.site_name).process_item(item)
        Pipeline(tb.site_id, tb.site_name).upload_item(item, sets)

    try:
        Pipeline(tb.site_id, tb.site_name).close_spider()
    except:
        Logger().setLogger(tb.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # tb.log_path = "../" + tb.log_path
    run()
