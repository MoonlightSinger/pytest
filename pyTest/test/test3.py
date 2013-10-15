'''
Created on 2013-10-13

@author: yutao
'''
import os

import time
import _thread
import threading
def timer(no, interval):
    cnt = 0
    while cnt<10:
        print ('Thread:(%d) Time:%s  第%d次'%(no,time.ctime(),cnt))
        time.sleep(interval)
        cnt+=1 
   
 
def test1(): #Use thread.start_new_thread() to create 2 new threads
    _thread.start_new_thread(timer, (1,1))
    _thread.start_new_thread(timer, (2,1))
def test2():
    thread1=threading.Thread(target=timer,args=(1,1)) #创建一个Thread实例
    thread2=threading.Thread(target=timer,args=(2,1))
    thread1.start()                          #start函数，启动线程                       
    thread2.start()
    thread1.join()                            #join函数，用于等待线程结束
    thread2.join()
 
if __name__=='__main__':
    print(2)
    test2()
    print(1)
