#coding:utf-8
import sys
sys.path.append("..")
from config import TencentConfig as tc
from logger import Logger
from pipelines import Pipeline

from func import Req,xpath_out
from lxml import etree
import re
import json

class Tencent(object):
    url = 'https://www.qq.com/'
    A_urls = []   #A类详情页面的url列表
    B_urls = []   #B类详情页面的url列表,B类需要通过js获取详情页信息，且B类中又有两类
    pattern_a = re.compile(r'.*?news.qq.com/a.*?',re.S)
    pattern_b = re.compile(r'.*?new.qq.com/omn.*?',re.S)

    def first_requests(self):   #第一次请求首页以获取详情页url
        selector = etree.HTML(Req(self.url).get_select().content)
        uls = selector.xpath('//*[@id="tab-news-01"]/ul')
        try:
            for ul in uls:
                lis = ul.xpath('li')
                for li in lis:
                    hrefs = li.xpath('a/@href')
                    for href in hrefs:       #对所有的url进行分类A或B
                        if re.match(self.pattern_a, href):
                            self.A_urls.append(href)
                        elif re.match(self.pattern_b, href):
                            self.B_urls.append(href)
                        else:
                            pass
            print("First Time Requests Succeed")
        except:
            Logger().setLogger(tc.log_path, 4, "Failed to get detail_page_urls")
            pass


    def second_requests(self):    #第二次请求详情页
        for url in self.A_urls:   #A类url直接请求，得到数据
            try:
                selector = etree.HTML(Req(url).get_select().content)
                item = dict()
                item['link'] = url
                item['title'] = selector.xpath('//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/h1/text()')
                item['datetime'] = selector.xpath('//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/div/div[1]/span[3]/text()')
                if item['title'] != [] and item['datetime'] != []:
                    item['title'] = item['title'][0]
                    item['datetime'] = item['datetime'][0]
                elif item['title'] != [] and item['datetime'] == []:
                    item['title'] = item['title'][0]
                    item['datetime'] = selector.xpath('//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/div/div[1]/span[2]/text()')[0]
                else:
                    item['title'] = selector.xpath('//*[@id="Main-Article-QQ"]/div[2]/div[1]/div[2]/div[1]/h1/text()')[0]
                    item['datetime'] = selector.xpath('//*[@id="Main-Article-QQ"]/div[2]/div[1]/div[2]/div[1]/div/div[1]/span[3]/text()')[0]
                yield item
            except:
                Logger().setLogger(tc.log_path, 2, "Failed to get A class detail page info,url is" + url)
                pass

        for url in self.B_urls:    #B类
            try:
                response = Req(url).get_select()
                selector = etree.HTML(response.text)
                data = selector.xpath('/html/head/script[5]/text()')
                if data:        #B类中部分js渲染的页面
                    item = dict()
                    data = json.loads(data[0].strip()[14:])
                    item['link'] = url
                    item['title'] = data['title']
                    item['datetime'] = data['pubtime']
                    yield item
                else:     #B类中全部js渲染的页面
                    self.third_requests(url)
            except:
                Logger().setLogger(tc.log_path, 2, "Get B class detail page info failed,url is" + url)
                pass

        print("Second Time Requests Finished")

    def third_requests(self, url):
        content_api = 'https://openapi.inews.qq.com/getQQNewsNormalContent'   #腾讯异步请求新闻内容的url
        pattern_id = re.compile(r'.*?/([\s\w]*)$', re.S)
        headers = {
            'referer': url,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
        }
        params = {
            'id': re.match(pattern_id, url).group(1),
            'chlid': 'news_rss',
            'refer': 'mobilewwwqqcom',
            'otype': 'jsonp',
            'ext_data': 'all',
            'srcfrom': 'newsapp',
            'callback': 'getNewsContentOnlyOutput'
        }
        response = Req(url=content_api, headers=headers, params=params).get_select()
        data = eval("'" + response.content.decode('ascii') + "'")

        pattern_item = re.compile(r'.*?"title":"(.*?)",.*?"pubtime":"(.*?)",.*?$',re.S)
        info = re.match(pattern_item, data).group(1,2)
        item = dict()
        item['link'] = url
        item['title'] = info[0]
        item['datetime'] = info[1]
        if item['title'] is not None:
            yield item
        else:
            Logger().setLogger(tc.log_path, 2, "Get B2 class detail page info failed, title is None")

def run():

    sets = Pipeline(tc.site_id, tc.site_name).structure_set()
    Pipeline(tc.site_id, tc.site_name).open_spider(sets)
    Tencent().first_requests()

    for item in Tencent().second_requests():
        Pipeline(tc.site_id, tc.site_name).process_item(item)
        Pipeline(tc.site_id, tc.site_name).upload_item(item, sets)

    try:
        Pipeline(tc.site_id, tc.site_name).close_spider()
    except:
        Logger().setLogger(tc.log_path, 4, "Failed to close spider,db_session may failed")
        pass

if __name__ == '__main__':
    # tc.log_path = "../" + tc.log_path
    run()
