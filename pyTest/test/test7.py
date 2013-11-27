# coding: GBK
'''
Created on 2013-11-27

@author: yutao
'''
import test.test6
import time
import _thread
import threading
def timer(interval=2):
    while True:
        time.sleep(interval)
        test.test6.getIP();
if __name__=="__main__":
    thread1=threading.Thread(target=timer) #创建一个Thread实例
    thread1.start()                          #start函数，启动线程                       
    thread1.join()                            #join函数，用于等待线程结束