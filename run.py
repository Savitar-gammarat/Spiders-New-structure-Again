#coding:utf-8
from config import MainConfig as m
from logger import Logger
import threading
from time import sleep

from crawler import zhihu,tencent,douban,sina,tieba,phoenix,netease,huanqiu,xinhua,donews,souhu,bbc,slashdot,wired,time,newyork,economist,fortune

list = [zhihu, tencent, douban, sina, tieba, phoenix, netease, huanqiu, xinhua, donews, souhu, bbc, slashdot, wired, time, newyork, economist, fortune]


def thread_main(className):
    global count, mutex

    # 取得锁
    mutex.acquire()
    count = count + 1
    # 释放锁
    mutex.release()

    try:
        className.run()
        print(str(className) + "Succeed！")
    except:
        Logger.setLogger(m.log_path, 4, className + " Spider Failed")

    sleep(1)

def main():
    global count, mutex
    threads = []

    count = 1
    # 创建一个锁
    mutex = threading.Lock()
    # 先创建线程对象
    for x in list:
        threads.append(threading.Thread(target=thread_main, args=(x,)))
    # 启动所有线程
    for t in threads:
        t.start()
    # 主线程中等待所有子线程退出
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
