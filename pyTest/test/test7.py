# coding: GBK
'''
Created on 2013-11-27

@author: yutao
'''
import test.test6
import time
import _thread
import threading
import subprocess
import re
def timer(interval=2):
    while True:
        time.sleep(interval)
        test.test6.getLanDict()
        
def changeToDhcp(ipdict):
    s1='netsh interface ipv4 set dnsservers  '+ipDict['��������']+'  dhcp'
    print(s1)
    t = subprocess.Popen( s1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s2 = 'netsh interface ipv4 set address   '+ipDict['��������']+'  dhcp'
    print(s2)
    t = subprocess.Popen( s2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s = t.stdout.read()
    ss = s.decode(encoding='gbk')
    print(ss)
def changeToStatic(ipdict):
    s1='netsh interface ipv4 set dnsservers  '+ipDict['��������']+'  static '+ipDict['DNS ������']
    print(s1)
    t = subprocess.Popen(s1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s2 ='netsh interface ipv4 set address   '+ipDict['��������']+'  static  '+ipDict['IPv4 ��ַ']+'   '+ipDict['��������'] +'  '+ipDict['Ĭ������']
    print(s2)
    t = subprocess.Popen(s2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s = t.stdout.read()
    ss = s.decode(encoding='gbk')
    print(ss)
if __name__=="__main__":
    #  thread1=threading.Thread(target=timer) #����һ��Threadʵ��
    # thread1.start()                          #start�����������߳�                       
    # thread1.join()                            #join���������ڵȴ��߳̽���
    ipDict=test.test6.getLanDict()
    changeToDhcp(ipDict)
    time.sleep(5)   
    ipDict=test.test6.getLanDict()
    ipDict['IPv4 ��ַ']=re.search(r'\d+\.\d+\.\d+\.\d+',ipDict['IPv4 ��ַ']).group()
    changeToStatic(ipDict)