#coding:utf-8
import alchemy as db
from config import PipelineConfig as ne
from logger import Logger
from datetime import datetime
from sqlalchemy import func

import jieba
import re

class Pipeline(object):
    item_set = set()
    jieba_pattern = re.compile(u"[\u4e00-\u9fa5_a-zA-Z0-9]+")

    def __init__(self, site_id, site_name):

        self.site_id = site_id
        self.site_name = site_name

    def orm_sort(self, dict):
        set_out = []
        for i in dict:
            set_out.append(i[0])
        set_out = set(set_out)

        return set_out

    def word_compile(self, x):
        return bool(re.search(self.jieba_pattern, x))

    def structure_set(self):
        container = dict()
        today = datetime.today().day
        try:
            container['site_set'] = db.db_session.query(db.Site).filter(db.Site.id == self.site_id).first()
            container['key_set'] = self.orm_sort(db.db_session.query(db.Keyword.keyword).all())
            container['news_set'] = self.orm_sort(db.db_session.query(db.News.link).filter(db.News.site_id == self.site_id and func.DATE(db.News.datetime).between(today-5,today+5)).all())
            container['set_notsql'] = {}

            return container
        except:
            print("Structure sets failed")
            Logger().setLogger(ne.log_path, 2, "Pipelines, Failed to structure set")
            pass

    def open_spider(self, structure):
        try:
            if structure['site_set']:  # 判断该站点是否已经建立在site表内，如未建立则创建之，id须从settings内提前设置正确
                pass
            else:
                new_site = db.Site(  # 创建新的site对象，并尝试插入到site表
                    id=self.site_id,
                    name=self.site_name
                )
                try:
                    db.db_session.add(new_site)
                    db.db_session.commit()
                    print("成功插入site信息")
                except:
                    print("Failed to insert site")
                    pass
            print("Succeed open spider")
        except:
            print("Open spider failed")
            Logger().setLogger(ne.log_path, 3, "Failed to open spider(site info may not be inserted)")
            pass

    def process_item(self, item):
        try:
            item['site_id'] = self.site_id
            if item['title'] != None:
                try:  # 尝试对title进行中文分词操作
                    item['jieba'] = list(jieba.cut_for_search(item['title'].lower()))
                    item['jieba'] = list(set(filter(self.word_compile, item['jieba'])))
                    print("jieba Succeed")
                except:
                    Logger().setLogger(ne.log_path, 2, "Pipelines, Failed to process item,So no jieba or site_id,may cause error,url is")
            else:
                item['jieba'] = None
            if not 'hot' in item.keys():
                item['hot'] = 0
            if not 'datetime' in item.keys():
                item['datetime'] = None

            if not 'status' in item.keys():
                item['status'] = False
            else:
                item['status'] = True

            if not 'home' in item.keys():
                item['home'] = True
            else:
                item['home'] = False
        except:
            Logger().setLogger(ne.log_path, 2, "Pipelines, Failed to process item, item is " + item)
            pass

    def process_keyword(self, item, structure):
        try:
            key_list = []
            if item['jieba'] is None:  # 如果item['jieba']为空则表示jieba分词失败
                print("JieBa failed so no item['jieba']")
            else:
                for i in item['jieba']:  # 遍历item['jieba']内的每个词项
                    if i is None:
                        pass
                    elif i in structure['set_notsql'].keys():  # 获取存在于set但不存在于数据库内的词汇orm对象
                        key_list.append(structure['set_notsql'][i])
                    else:
                        x = db.db_session.query(db.Keyword).filter(db.Keyword.keyword == i).all()
                        if len(x) != 0:
                            x = x[0]
                            key_list.append(x)
                        else:  # 如果该词不存在于set内则创建SQLAlchemy对象并插入之，在添加到key_list,key_set与set_notsql内
                            new_keyword = db.Keyword(
                                keyword=i
                            )
                            try:
                                db.db_session.add(new_keyword)
                            except Exception:
                                print("Failed to insert keyword")

                            # 对变量进行更新
                            structure['key_set'].add(i)
                            structure['set_notsql'][i] = new_keyword

                            # 插入到该item下收集所有对应keyword的列表
                            key_list.append(new_keyword)
            print("Succeed add keywords")
            return key_list
        except:
            Logger().setLogger(ne.log_path, 2, "Pipelines, Failed to process keyword,SQLAlchemy or some other Error")
            pass
    def process_field(self, item):
        try:
            if not 'field' in item.keys():
                field_list = []
            else:
                field_list = db.db_session.query(db.Field).filter(db.Field.id == item['field']).all()

            return field_list
        except:
            Logger().setLogger(ne.log_path, 2, "Pipelines, Failed to process field,Maybe SQLAlchemy Error")
            pass

    def upload_item(self, item, structure):
        try:
            key_list = self.process_keyword(item, structure)
            field_list = self.process_field(item)

            if item['title'] is not None:  #判断如果item['title']不为空则执行插入操作
                if item['link'] not in structure['news_set'] and item['link'] not in self.item_set:  #如果该link已经存在于数据表内略过
                    new_news = db.News(
                        link=item['link'],
                        title=item['title'],
                        hot=item['hot'],
                        datetime=item['datetime'],
                        site_id=item['site_id'],
                        status=item['status'],
                        home=item['home']
                    )
                    new_news.keywords = key_list  # 建立每个news和与他相关的keyword的关系
                    new_news.fields = field_list  # 建立每个news和与他相关的field的关系
                    try:
                        db.db_session.add(new_news)
                        db.db_session.commit()
                    except Exception:
                        Logger().setLogger(ne.log_path, 4, "Failed to insert new news,url is " + item['link'])
                        pass

                    self.item_set.add(item['link'])

            print("Upload Succeed")
        except:
            Logger().setLogger(ne.log_path, 2, "Pipelines, Failed to upload item,url is" + item['link'])
            pass

    def close_spider(self):
        try:
            db.db_session.commit()
            db.db_session.close()
            print("Spider Finished")
        except:
            print("Close spider failed")
            Logger().setLogger(ne.log_path, 4, "Failed to commit or close db_session")
