'''
Created on 2013-10-13

@author: yutao
'''
import os
os.mkdir("d:/ew地方")
file_t=open('d:/ew地方/kkk.txt','w',100,encoding='utf-8')
file_t.write('5水电费1s2')
file_t.flush
file_t.close