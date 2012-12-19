#coding=utf-8
'''
Created on 2012-10-18
@author: wasw100@gmail.com
'''

import httplib, urllib, Cookie

def cookie2dict(cookie):  
    cookie_dict = {}
    if cookie == None:
        return cookie_dict 
    for one in cookie.split('; '):  
        keyvalue = one.split('=', 2)
        if len(keyvalue) == 2:
            cookie_dict.setdefault(keyvalue[0], keyvalue[1])
    return cookie_dict  

def dict2cookie(dic):  
    cs = ['%s=%s' % (key, dic[key]) for key in dic] 
    return '; '.join(cs)

def get_url_value(params, key):
    """url参数中根据key获取value"""
    if "?" in params:
        begin = params.find('?')
        params = params[begin:]
    params.replace('&amp;', '&')
    for one in params.split('&'):
        keyvalue = one.split('=', 2)
        if len(keyvalue) == 2 and keyvalue[0] == key:
            return keyvalue[1]
    return None
        

class HttpToolkit:
    proxy = False
    ip = ""
    port = 80
    
    def __init__(self):
        """模拟chrome的请求头,可以根据需要修改"""
        self.cookie = ''
        self.cookie_dict = {}
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13'
        accept_encoding = 'gzip,deflate,sdch'
        content_type = 'application/x-www-form-urlencoded'
        accept_language = 'zh-CN,zh;q=0.8'
        accept_charset = 'GBK,utf-8;q=0.7,*;q=0.3'
        pragma = 'no-cache'
        cache_control = 'no-cache'
        self.headers = {'Accept': accept, 'User-Agent': user_agent, 'Accept-Encoding': accept_encoding, 'Content-Type':content_type, 
                        'Accept-Language': accept_language, 'Accept-Charset': accept_charset, 
                        'Pragma':pragma, 'Cache-Control':cache_control}
        
    @staticmethod
    def setproxy(ip, port):
        HttpToolkit.proxy = True
        HttpToolkit.ip = ip
        HttpToolkit.port = port

    def get(self, url=None, data=None, cookie=None, referer=None):
        params = self.__data2params(data)
        if '?' in url and params:
            url = '%s&%s' % (url, params)
        elif params:
            url = '%s?%s' % (url, params)
        return self.__request('GET', url, '', cookie, referer)
    def post(self, url=None, data={}, cookie=None, referer=None):
        return self.__request("POST", url, self.__data2params(data), cookie, referer)
    
    def __data2params(self, data={}):
        try:
            params = urllib.urlencode(data)
        except TypeError:
            params = data
        return params
        
    def __request(self, method='GET', url=None, params='', cookie=None, referer=None):
        if cookie != None:
            self.cookie_dict = cookie2dict(cookie)
            self.headers['Cookie'] = cookie
        if referer != None:
            self.headers['Referer'] = referer
        scheme, rest = urllib.splittype(url)  
        host, rest = urllib.splithost(rest)  
        if rest == '':
            rest = '/'
        if(HttpToolkit.proxy):
            self.conn = httplib.HTTPConnection('%s:%d' % (HttpToolkit.ip, HttpToolkit.port))
            request_url = '%s://%s%s' % (scheme, host, rest)
        else:
            self.conn = httplib.HTTPConnection(host)
            request_url = rest
        self.conn.request(method, request_url, params, self.headers)
        response = self.conn.getresponse()
        self.response = response
        
        '''
        handle cookie start
        '''
        set_cookies = response.getheader("Set-Cookie");
        #用, 分割为多份,单个处理
        if set_cookies != None:
            morsels = []
            for set_cookie in set_cookies.split(', '):
                morsels.extend(Cookie.BaseCookie(set_cookie).values())
            for morsel in morsels:
                key, value, path = morsel.key, morsel.value, morsel['path'].strip(', ')
                if value == 'null' and key in self.cookie_dict:
                    del self.cookie_dict[key]
                elif path == '/':
                    self.cookie_dict[key] = value
        self.cookie = dict2cookie(self.cookie_dict)
        '''
        handle cookie end
        '''
        
        '''
        if 301 or 302
        '''
        if response.status == 301 or response.status == 302:
            location = response.getheader("Location");
            return self.__request(method='GET', url=location, params=params, cookie=self.cookie, referer=url)
        
        content_type = response.getheader("Content-Type")
        charset = None
        if content_type != None and content_type.find('charset') != -1:
            charset = content_type.split('charset=')[-1]
        data = response.read()
        content_encoding = response.getheader("Content-Encoding")
        if 'gzip' == content_encoding:
            from cStringIO import StringIO
            from gzip import GzipFile
            data = GzipFile(fileobj=StringIO(data)).read()
        if charset != None:
            try:
                data = unicode(data, charset)
            except UnicodeDecodeError:
                pass
        return data
   
def test():
#    HttpToolkit.setproxy('127.0.0.1', 8888)
    url = "http://www.baidu.com/";
    http_toolkit = HttpToolkit()
    print http_toolkit.get(url=url)
    print http_toolkit.cookie

if __name__ == '__main__': test()

