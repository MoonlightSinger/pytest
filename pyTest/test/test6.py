# coding: GBK
'''
Created on 2013-11-25
@author: yutao 
'''
import subprocess
import re
def getIP():
    t = subprocess.Popen(['ipconfig', '/all'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    s = t.stdout.read()
    ss = s.decode(encoding='gbk')
    '''
    tt=open('123.txt', mode='w',  encoding='gbk',newline='')
   tt.write(ss)
   tt.flush()
   tt.close()
   '''
    rex = r'以太网适配器 本地连接(.*?):\r\n\r\n(.+?)\r\n\r\n'
    rs = re.search(rex, ss, re.DOTALL)
    rs1 = rs.group(2)
    listt = rs1.split('\r\n')
    mydict = {}
    for temps in listt:
        ts = temps.strip()
        ts2 = re.split(r'[\s\.]+:\s*', ts)
    # ts2=re.split(r'(\s|\.)+:\s*',ts)
        mydict[ts2[0]] = ts2[1]
        print(ts2)  # print(mydict)
    
    print(mydict['IPv4 地址'])
if __name__=="__main__":
    getIP()
