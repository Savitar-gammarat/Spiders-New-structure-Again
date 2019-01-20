#coding:utf-8
import datetime

class ORM(object):
    #服务器
    username = 'hao'
    password = '991004'
    host = '47.101.196.53'
    port = '3306'
    database= 'news-aggregation'

    # #本机
    # username = 'root'
    # password = ''
    # host = 'localhost'
    # port = '3306'
    # database = 'test'

    today = str(datetime.date.today())

class MainConfig(object):
    log_path = "log/main.log"


class PipelineConfig(object):
    log_path = "log/pipelines.log"

class FuncConfig(object):
    log_path = "log/req.log"

class ZhihuConfig(object):
    site_id = 1
    site_name = '知乎'
    log_path = "log/zhihu.log"


class TencentConfig(object):
    site_id = 2
    site_name = '腾讯'
    log_path = "log/tencent.log"


class DoubanConfig(object):
    site_id = 3
    site_name = '豆瓣'
    log_path = "log/douban.log"


class SinaConfig(object):
    site_id = 4
    site_name = '新浪'
    log_path = "log/sina.log"


class TiebaConfig(object):
    site_id = 5
    site_name = '百度贴吧'
    log_path = "log/tieba.log"


class PhoenixConfig(object):
    site_id = 6
    site_name = '凤凰网'
    log_path = "log/phoenix.log"


class NeteaseConfig(object):
    site_id = 7
    site_name = '网易新闻'
    log_path = "log/netease.log"


class HuanqiuConfig(object):
    site_id = 8
    site_name = '环球网'
    log_path = "log/huanqiu.log"


class XinHuaConfig(object):
    site_id = 9
    site_name = '新华网'
    log_path = "log/xinhua.log"


class DoNewsConfig(object):
    site_id = 10
    site_name = 'DoNews'
    log_path = "log/donews.log"


class SouHuConfig(object):
    site_id = 11
    site_name = '搜狐'
    log_path = "log/souhu.log"


class BBCConfig(object):
    site_id = 12
    site_name = 'BBC'
    log_path = "log/bbc.log"


class SlashDotConfig(object):
    site_id = 13
    site_name = 'SlashDot'
    log_path = "log/slashdot.log"


class WiredConfig(object):
    site_id = 14
    site_name = 'Wired'
    log_path = "log/wired.log"


class TimeConfig(object):
    site_id = 15
    site_name = 'Time'
    log_path = "log/time.log"


class NewYorkTimeConfig(object):
    site_id = 16
    site_name = 'New York Times'
    log_path = "log/newyork.log"


class EconomistConfig(object):
    site_id = 17
    site_name = 'The Economist'
    log_path = "log/economist.log"


class FortuneConfig(object):
    site_id = 18
    site_name = 'Fortune'
    log_path = "log/fortune.log"
