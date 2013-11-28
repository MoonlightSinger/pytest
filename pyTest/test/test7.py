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
    s1='netsh interface ipv4 set dnsservers  '+ipDict['网卡名字']+'  dhcp'
    print(s1)
    t = subprocess.Popen( s1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s2 = 'netsh interface ipv4 set address   '+ipDict['网卡名字']+'  dhcp'
    print(s2)
    t = subprocess.Popen( s2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s = t.stdout.read()
    ss = s.decode(encoding='gbk')
    print(ss)
def changeToStatic(ipdict):
    s1='netsh interface ipv4 set dnsservers  '+ipDict['网卡名字']+'  static '+ipDict['DNS 服务器']
    print(s1)
    t = subprocess.Popen(s1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s2 ='netsh interface ipv4 set address   '+ipDict['网卡名字']+'  static  '+ipDict['IPv4 地址']+'   '+ipDict['子网掩码'] +'  '+ipDict['默认网关']
    print(s2)
    t = subprocess.Popen(s2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s = t.stdout.read()
    ss = s.decode(encoding='gbk')
    print(ss)
if __name__=="__main__":
    #  thread1=threading.Thread(target=timer) #创建一个Thread实例
    # thread1.start()                          #start函数，启动线程                       
    # thread1.join()                            #join函数，用于等待线程结束
    ipDict=test.test6.getLanDict()
    changeToDhcp(ipDict)
    time.sleep(5)   
    ipDict=test.test6.getLanDict()
    ipDict['IPv4 地址']=re.search(r'\d+\.\d+\.\d+\.\d+',ipDict['IPv4 地址']).group()
    changeToStatic(ipDict)