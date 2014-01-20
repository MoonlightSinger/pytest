# coding: GBK
'''
Created on 2013-11-27

@author: yutao
'''

import time
import subprocess
import re
#import test.test6
def getLanDict():
    t = subprocess.Popen(['ipconfig', '/all'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s = t.stdout.read()
    ss = s.decode(encoding='gbk')
    #'''
    #tt=open('123.txt', mode='w',  encoding='gbk',newline='')
    #tt.write(ss)
    #tt.flush()
    #tt.close()
    #'''
    rex = r'以太网适配器 (本地连接.*?):\r\n\r\n(.+?)\r\n\r\n'
    rs = re.search(rex, ss, re.DOTALL)
    rs1 = rs.group(2)
    listt = rs1.split('\r\n')
    lanDict = {}
    lanDict['网卡名字']=rs.group(1)
    for temps in listt:
        ts = temps.strip()
        ts2 = re.split(r'[\s\.]+:\s*', ts)
        if len(ts2)==2:
            lanDict[ts2[0]] = ts2[1]
            print(ts2)
    #print(lanDict['IPv4 地址'])
    #print(lanDict['网卡名字'])
    return lanDict
        
def changeToDhcp(ipDict):
    s1='netsh interface ipv4 set dnsservers  '+ipDict['网卡名字']+'  dhcp'
    print(s1)
    t = subprocess.Popen( s1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s2 = 'netsh interface ipv4 set address   '+ipDict['网卡名字']+'  dhcp'
    print(s2)
    t = subprocess.Popen( s2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    
def changeToStatic(ipDict):
    s1='netsh interface ipv4 set dnsservers  '+ipDict['网卡名字']+'  static '+ipDict['DNS 服务器']
    print(s1)
    t = subprocess.Popen(s1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s2 ='netsh interface ipv4 set address   '+ipDict['网卡名字']+'  static  '+ipDict['IPv4 地址']+'   '+ipDict['子网掩码'] +'  '+ipDict['默认网关']
    print(s2)
    t = subprocess.Popen(s2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
  
def getOfferIp():
    ipDict=getLanDict()
    changeToDhcp(ipDict)
    while True:
        time.sleep(3)
        ipDict=getLanDict()
        if '默认网关' in ipDict and ipDict['默认网关']!='':
            break
    ipDict['IPv4 地址']=re.search(r'\d+\.\d+\.\d+\.\d+',ipDict['IPv4 地址']).group()
    ipDict['DNS 服务器']='none'
    ipDict['默认网关']='none'
    changeToStatic(ipDict)

if __name__=="__main__":
    while True:
        getOfferIp()
        s=input('执行完毕！回车重新获得IP，输入任意值退出！')
        if(s!=''):
            break
    print('感谢使用，祝你有开心的一天！\n\r')
    time.sleep(1.5)