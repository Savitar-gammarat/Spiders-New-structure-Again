#coding:utf-8
import logging
import os

class Logger(object):


    def setLogger(self, path, level, error):

        # 创建一个logger,可以考虑如何将它封装
        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(os.path.join(os.getcwd(), path),encoding='utf8')
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('[' + '%(asctime)s' + ']' +' - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)

        if level == 1:
            logger.debug(error)
        elif level == 2:
            logger.info(error)
        elif level == 3:
            logger.warning(error)
        elif level == 4:
            logger.error(error)
        else:
            logger.critical(error)
        return logger

        # # 记录一条日志
        # logger.debug('还好')
        # logger.info('hello world, i\'m log helper in python, may i help you')
        # return logger

