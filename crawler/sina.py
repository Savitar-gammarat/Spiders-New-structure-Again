#coding:utf-8
import sys
sys.path.append("..")
from config import SinaConfig as sina
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
import datetime
import json
import time

class Sina(object):
    url = 'http://top.news.sina.com.cn/ws/GetTopDataList.php'
    params = {
        'top_type': 'day',
        'top_cat': 'www_www_all_suda_suda',
        'top_show_num': '10',
        'top_order': 'DESC'
    }

    def first_requests(self):
        self.params['top_time'] = str(datetime.date.today()).replace("-","")
        response = Req(url=self.url, params=self.params).get_select()

        data = json.loads(response.content[10:-2].decode('utf8'))['data']
        for news in data:
            item = dict()
            item['title'] = news['title']
            item['link'] = news['url']
            item['datetime'] = time.strptime(news['time'][:-6], '%a, %d %b %Y %H:%M:%S')
            item['datetime'] = time.strftime('%Y-%m-%d %H:%M:%S', item['datetime'])
            yield item

def run():
    sets = Pipeline(sina.site_id, sina.site_name).structure_set()
    Pipeline(sina.site_id, sina.site_name).open_spider(sets)

    for item in Sina().first_requests():
        Pipeline(sina.site_id, sina.site_name).process_item(item)
        Pipeline(sina.site_id, sina.site_name).upload_item(item, sets)

    try:
        Pipeline(sina.site_id, sina.site_name).close_spider()
    except:
        Logger().setLogger(sina.log_path, 2, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # sina.log_path = "../" + sina.log_path
    run()
