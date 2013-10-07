'''
Created on 2013-9-24

@author: yutao
'''
import urllib.request
import http.cookiejar
import zlib
globalCookie = None;

def initAutoHandleCookies(localCookieFileName):
    """Add cookiejar to support auto handle cookies.
    support designate cookie file
    
    Note:
    after this init, later urllib.request.urlopen will automatically handle cookies
    """

    #globalCookie = cookielib.FileCookieJar(localCookieFileName); #NotImplementedError
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
if __name__=="__main__":
    #demo auto handle cookie
    initAutoHandleCookies("localCookie.txt");
    demoUrl = "http://www.crifan.com";
    respHtml = getUrlRespHtml(demoUrl);
    print ("respHtml=",respHtml);
    #later process urllib.request related things, will auto handle cookie