# coding: GBK
'''
Created on 2013-11-25
@author: yutao 
'''
import subprocess
import re
print('12竖的1')
t = subprocess.Popen('ping 10.181.83.78', stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)   
s=t.stdout.read()
print(t.stdout)
ss=s.decode(encoding='gbk')

t.wait()
print(t.returncode)
print('11')
ss1='10.181.83.78'
#p = re.compile(r'来自 '+ss+' 的回复: 字节=(\d{1,3}) 时间[=<>](\d+)ms TTL=(\d+)')
p = re.compile(r'来自 (10.181.83.78) 的回复: 字节=(\d{1,3}) 时间([=<>](?P<replytime>\d+)ms) TTL=(\d+)')
rs=p.findall(ss)
print(len(rs))