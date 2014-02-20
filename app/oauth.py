#encoding:utf-8
import urllib, urllib2
import json


google = {
    "auth_url": "https://accounts.google.com/o/oauth2/auth",
    "token_url": "https://accounts.google.com/o/oauth2/token",
    "client_id" :"453224369183-hbge7c784dj0bgutcf52mq3s64d08m69.apps.googleusercontent.com",
    "client_secret" : "TDDatFwSX5qqAW70UIRdeZ-f",
    "redirect_uri" : "http://127.0.0.1:5000/auth_google_callback",
    "scope": "email",
    "info_url": "https://www.googleapis.com/plus/v1/people/me"
    }

douban = {
    "auth_url": "https://www.douban.com/service/auth2/auth",
    "token_url": "https://www.douban.com/service/auth2/token",
    "client_id" :"0ca82b02a5dde13225f88107f199a396",
    "client_secret" : "677827aeca893119",
    "redirect_uri" : "http://127.0.0.1:5000/auth_douban_callback",
    "scope": "douban_basic_common",
    "info_url": "https://api.douban.com/v2/user/~me"
    }


class MyRequest(object):
    def __init__(self, url, data={}, method='GET', headers={}):
        self.url = url
        self.data = data
        self.headers = headers
        if method in ('GET', 'POST'):
            self.method = method
        else:
            raise 'errot method'

    def request(self):
        if self.method == 'GET':
            self.url += '?'
            for (k, v) in self.data.items():
                param = k + '=' + v + '&'
                self .url += param
            req = urllib2.Request(self.url)
        elif self.method == 'POST':
            data = urllib.urlencode(self.data)
            req = urllib2.Request(self.url, data=data)

        for (k, v) in self.headers.items():
            req.add_header(k, v)

        return req
    
def get_auth(auth_server):
    data = {
            'response_type' : 'code',
            'client_id': auth_server['client_id'],
            'redirect_uri': auth_server['redirect_uri'],
            'scope' : auth_server['scope']
            }
    req = MyRequest(auth_server['auth_url'], data)
    req.request()
    print req.url
    return req.url

def get_token(auth_server, code):
    data = {
            'code': code,
            'client_id': auth_server['client_id'],
            'client_secret': auth_server['client_secret'],
            'redirect_uri': auth_server['redirect_uri'],
            'grant_type': 'authorization_code'
            }
    req = MyRequest(auth_server['token_url'], data, 'POST')
    try:
        res = urllib2.urlopen(req.request()).read()
    except  urllib2.URLError, e:
        print e.reason
        return None
    token = json.loads(res)['access_token']
    return token

def get_info(auth_server, token):
    headers = {
            'authorization': 'Bearer ' + token
            }
    req = MyRequest(auth_server['info_url'], headers=headers)
    res = urllib2.urlopen(req.request()).read()
    return res

