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
    thread1=threading.Thread(target=timer) #����һ��Threadʵ��
    thread1.start()                          #start�����������߳�                       
    thread1.join()                            #join���������ڵȴ��߳̽���