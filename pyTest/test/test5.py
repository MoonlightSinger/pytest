# coding: GBK
'''
Created on 2013-11-25
@author: yutao 
'''
import subprocess
import re
print('12����1')
t = subprocess.Popen('ping 10.181.83.78', stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)   
s=t.stdout.read()
print(t.stdout)
ss=s.decode(encoding='gbk')

t.wait()
print(t.returncode)
print('11')
ss1='10.181.83.78'
#p = re.compile(r'���� '+ss+' �Ļظ�: �ֽ�=(\d{1,3}) ʱ��[=<>](\d+)ms TTL=(\d+)')
p = re.compile(r'���� (10.181.83.78) �Ļظ�: �ֽ�=(\d{1,3}) ʱ��([=<>](?P<replytime>\d+)ms) TTL=(\d+)')
rs=p.findall(ss)
print(len(rs))