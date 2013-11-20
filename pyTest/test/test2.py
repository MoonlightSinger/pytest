'''
Created on 2013-9-24

@author: yutao
'''
import urllib.request
import http.cookiejar
import zlib
import re
import os
globalCookie = None;

def initAutoHandleCookies(localCookieFileName):
    """Add cookiejar to support auto handle cookies.
    support designate cookie file
    
    Note:
    after this init, later urllib.request.urlopen will automatically handle cookies
    """

    #globalCookie = cookielib.FileCookieJar(localCookieFileName); #NotImplementedError
    global globalCookie 
    globalCookie = http.cookiejar.LWPCookieJar(localCookieFileName); # prefer use this
    #globalCookie = cookielib.MozillaCookieJar(localCookieFileName); # second consideration
    #create cookie file
    globalCookie.save();

    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(globalCookie));
    urllib.request.install_opener(opener);

    #print "Auto handle cookies inited OK";
    return;    

#------------------------------------------------------------------------------
def getUrlResponse(url, postDict={}, headerDict={}, timeout=0, useGzip=False, postDataDelimiter="&") :
    """Get response from url, support optional postDict,headerDict,timeout,useGzip

    Note:
    1. if postDict not null, url request auto become to POST instead of default GET
    2  if you want to auto handle cookies, should call initAutoHandleCookies() before use this function.
       then following urllib.request.Request will auto handle cookies
    """

    # makesure url is string, not unicode, otherwise urllib.request.urlopen will error
    url = str(url);

    if (postDict) :
        if(postDataDelimiter=="&"):
            postData = urllib.parse.urlencode(postDict);
        else:
            postData = "";
            for eachKey in postDict.keys() :
                postData += str(eachKey) + "="  + str(postDict[eachKey]) + postDataDelimiter;
        postData = postData.strip();
        req = urllib.request.Request(url, postData);
    else :
        req = urllib.request.Request(url);

    if(headerDict) :
        #print "added header:",headerDict;
        for key in headerDict.keys() :
            # here also can overwrite Content-Type
            req.add_header(key, headerDict[key]);
        
    defHeaderDict = {
        'User-Agent'    : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
        'Accept-Encoding':'gzip, deflate',  
        'Connection'    : 'Keep-Alive',
        'Cache-Control' : 'max-age=0',
        'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    };

    # add default headers firstly
    for eachDefHd in defHeaderDict.keys() :
        #print "add default header: %s=%s"%(eachDefHd,defHeaderDict[eachDefHd]);
        req.add_header(eachDefHd, defHeaderDict[eachDefHd]);

    # add customized header later -> allow overwrite default header 
    if(headerDict) :
        #print "added header:",headerDict;
        for key in headerDict.keys() :
            req.add_header(key, headerDict[key]);

    if(timeout > 0) :
        # set timeout value if necessary
        resp = urllib.request.urlopen(req, timeout=timeout);
    else :
        resp = urllib.request.urlopen(req);

    #update cookies into local file
    global globalCookie 
    globalCookie.save();
    
    return resp;

#------------------------------------------------------------------------------
# get response html==body from url
#def getUrlRespHtml(url, postDict={}, headerDict={}, timeout=0, useGzip=False) :
def getUrlRespHtml(url, postDict={}, headerDict={}, timeout=0, useGzip=True, postDataDelimiter="&") :
    resp = getUrlResponse(url, postDict, headerDict, timeout, useGzip, postDataDelimiter);
    respHtml = resp.read();
    if(useGzip) :
        #print "---before unzip, len(respHtml)=",len(respHtml);
        respInfo = resp.info();
        
        # Server: nginx/1.0.8
        # Date: Sun, 08 Apr 2012 12:30:35 GMT
        # Content-Type: text/html
        # Transfer-Encoding: chunked
        # Connection: close
        # Vary: Accept-Encoding
        # ...
        # Content-Encoding: gzip
        
        # sometime, the request use gzip,deflate, but actually returned is un-gzip html
        # -> response info not include above "Content-Encoding: gzip"
        # eg: http://blog.sina.com.cn/s/comment_730793bf010144j7_3.html
        # -> so here only decode when it is indeed is gziped data
        if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")) :
            respHtml = zlib.decompress(respHtml, 16+zlib.MAX_WBITS);
            #print "+++ after unzip, len(respHtml)=",len(respHtml);

    return respHtml;

#------------------------------------------------------------------------------
def downloadPic(picAddr, min_Length=50000,savePath=''):
    resp = getUrlResponse(picAddr, postDict={}, headerDict={}, timeout=0, useGzip=False, postDataDelimiter="&")
    if int(dict(resp.headers)['Content-Length']) > min_Length:
        savePath=savePath+picAddr.split('/')[-1]
        file_t = open(savePath, 'wb', buffering=1000)
        file_t.write(resp.read())
        print(savePath)
        file_t.flush
        file_t.close
#------------------------------------------------------------------------------
def findNextHtml(nowHtml,nextRex):
    pass
def spiderPic(htmlStr):
    htmlStr
#------------------------------------------------------------------------------
def downloadHtml(demoUrl,picRex,nextHtmlFunc):
    #demo auto handle cookie
    initAutoHandleCookies("localCookie.txt");
    # = "http://koreanracequeens.tumblr.com/page/88";
    respHtml = getUrlRespHtml(demoUrl);
    t=respHtml.decode('utf-8')
    print ("respHtml=",t);
#     file_t=open('ttt.html','w',100,encoding='utf-8')
#     file_t.write(respHtml.decode('utf-8'))
#     file_t.flush
#     file_t.close
#     p = re.compile(r'(src|href)="(?P<picHttpAddr>http://\S+?/([\S^/]+\.jpg))"')
    p = re.compile(picRex)
    for m in p.finditer(t):
        print(m.group('picHttpAddr'))
        downloadPic(m.group('picHttpAddr'))
    return t
#------------------------------------------------------------------------------
def download2(demoUrl,dir):
        #demo auto handle cookie
    initAutoHandleCookies("localCookie.txt");
    respHtml = getUrlRespHtml(demoUrl);
    t=respHtml.decode('utf-8')
    file_t=open('ttt.html','w',100,encoding='utf-8')
    file_t.write(respHtml.decode('utf-8'))
    file_t.flush
    file_t.close
    p = re.compile(r'(src|href)="(http://cfile\S+/(image)/?\S*/([\w^/]+))"')
    if not os.path.exists(dir):
        os.mkdir(dir)
    for m in p.finditer(t):
        print(m.group())
        print(m.group(2))
        org_addr=m.group(2).replace('image','original')
        print(org_addr)
        local_filename=dir+'/'+m.group(4)+'.jpg'
        resp=getUrlResponse(org_addr,postDict={}, headerDict={}, timeout=0, useGzip=False, postDataDelimiter="&")
        min_Length=40000
        if int(dict(resp.headers)['Content-Length']) > min_Length:
            file_t=open(local_filename,'wb',buffering=1000)
            file_t.write(resp.read())
            print(local_filename)
            file_t.flush
            file_t.close
if __name__=="__main__":
    demoUrl = "http://illuce.tistory.com/category/Portrait/Photographer%27s%20cut?page=";
    for i in range(1,27):
        print('开始下载',i)
        download2(demoUrl+str(i),dir='pic')
        
    
   
        


        
    

    
    #later process urllib.request related things, will auto handle cookie
