#coding:utf-8
from sqlalchemy import Table,Column,Integer,String,TIMESTAMP,create_engine,func,Boolean,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker,relationship
from sqlalchemy.schema import ForeignKey
from config import ORM
import pymysql
import datetime

#设置一系列的基本参数
Base = declarative_base()
# DB_CONNECT_STR = "mysql+pymysql://root:@localhost:3306/news-aggregation?charset=utf8"
DB_CONNECT_STR = "mysql+pymysql://" + ORM.username + ":" + ORM.password + "@" + ORM.host + ":" + ORM.port + "/" + ORM.database + "?charset=utf8"
engine = create_engine(DB_CONNECT_STR,encoding="utf8",convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


#创建news于keyword多对多关系的中间表
news_keyword = Table('news_keyword', Base.metadata,              #news表与keyword表的中间表
    Column('news_id', Integer, ForeignKey('news.id'), primary_key=True),
    Column('keyword_id', Integer, ForeignKey('keyword.id'), primary_key=True)
)

#创建news于field多对多关系的中间表
news_field = Table('news_field', Base.metadata,              #news表与keyword表的中间表
    Column('news_id', Integer, ForeignKey('news.id'), primary_key=True),
    Column('field_id', Integer, ForeignKey('field.id'), primary_key=True)
)

#news表
class News(Base):
    __tablename__ = 'news'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(255),nullable=False)
    link = Column(String(255),nullable=False)
    hot = Column(Float, nullable=True, server_default='0')
    click = Column(Integer, nullable=False, server_default='0')
    datetime = Column(TIMESTAMP(),nullable=False,server_default=func.now())
    status = Column(Boolean(),nullable=False, default=False)
    home = Column(Boolean(),nullable=False, default=True)

    site_id = Column(Integer,ForeignKey('site.id'),nullable=False)   #设置与site表的外键

    keywords = relationship('Keyword',secondary=news_keyword)   #与中间表相关联
    fields = relationship('Field',secondary=news_field)   #与中间表相关联

#创建站点site表
class Site(Base):
    __tablename__ = 'site'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer,autoincrement=True,primary_key=True,index=True)
    name = Column(String(25),nullable=False)
    pageviews = Column(Integer,nullable=True)
    color = Column(String(255),nullable=True)
    logo = Column(String(255),nullable=True)
    font = Column(String(255), nullable=True)

    site_news = relationship('News', backref='site')  #创建站点与新闻表之间的一对多关系


#创建关键词keyword表
class Keyword(Base):
    __tablename__ = 'keyword'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    keyword = Column(String(255),nullable=False)
    datetime = Column(TIMESTAMP(),nullable=False,server_default=func.now())

    key_news = relationship('News', secondary=news_keyword)  #创建与中间表相关联的字段

#创建领域field表
class Field(Base):
    __tablename__ = 'field'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    field = Column(String(60),nullable=False)

    field_news = relationship('News', secondary=news_field)  # 创建与中间表相关联的字段


#创建全部表的主函数
def main():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    main()
