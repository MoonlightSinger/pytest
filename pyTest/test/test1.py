'''
Created on 2013-9-12

@author: yutao
'''
import urllib.request
import http.cookiejar
s=urllib.request.Request('http://login.xiami.com/member/login')
print(s.headers)
s.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0')
s.add_header('Host', 'www.xiami.com')	

s.add_header('Connection', 'keep-alive')
s.add_header('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3')
s.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
s.data=b'_xiamitoken=f210de75d171dc2395f10ef4884735c0&done=%2F&email=236593306%40qq.com&password=2504364&submit=%E7%99%BB+%E5%BD%95'
print(s.get_method())
print(s.get_data())
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
file_t=open('ttt.html','w',100,encoding='utf-8')
f=opener.open(s)
print(f)
print(f.geturl())
print(f.getcode())
print(dict(f.headers))
file_t.writelines(f.read().decode('utf-8'))
file_t.flush
file_t.close

