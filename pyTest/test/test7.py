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
    rex = r'��̫�������� (��������.*?):\r\n\r\n(.+?)\r\n\r\n'
    rs = re.search(rex, ss, re.DOTALL)
    rs1 = rs.group(2)
    listt = rs1.split('\r\n')
    lanDict = {}
    lanDict['��������']=rs.group(1)
    for temps in listt:
        ts = temps.strip()
        ts2 = re.split(r'[\s\.]+:\s*', ts)
        if len(ts2)==2:
            lanDict[ts2[0]] = ts2[1]
            print(ts2)
    #print(lanDict['IPv4 ��ַ'])
    #print(lanDict['��������'])
    return lanDict
        
def changeToDhcp(ipDict):
    s1='netsh interface ipv4 set dnsservers  '+ipDict['��������']+'  dhcp'
    print(s1)
    t = subprocess.Popen( s1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s2 = 'netsh interface ipv4 set address   '+ipDict['��������']+'  dhcp'
    print(s2)
    t = subprocess.Popen( s2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    
def changeToStatic(ipDict):
    s1='netsh interface ipv4 set dnsservers  '+ipDict['��������']+'  static '+ipDict['DNS ������']
    print(s1)
    t = subprocess.Popen(s1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s2 ='netsh interface ipv4 set address   '+ipDict['��������']+'  static  '+ipDict['IPv4 ��ַ']+'   '+ipDict['��������'] +'  '+ipDict['Ĭ������']
    print(s2)
    t = subprocess.Popen(s2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
  
def getOfferIp():
    ipDict=getLanDict()
    changeToDhcp(ipDict)
    while True:
        time.sleep(3)
        ipDict=getLanDict()
        if 'Ĭ������' in ipDict and ipDict['Ĭ������']!='':
            break
    ipDict['IPv4 ��ַ']=re.search(r'\d+\.\d+\.\d+\.\d+',ipDict['IPv4 ��ַ']).group()
    ipDict['DNS ������']='none'
    ipDict['Ĭ������']='none'
    changeToStatic(ipDict)

if __name__=="__main__":
    while True:
        getOfferIp()
        s=input('ִ����ϣ��س����»��IP����������ֵ�˳���')
        if(s!=''):
            break
    print('��лʹ�ã�ף���п��ĵ�һ�죡\n\r')
    time.sleep(1.5)