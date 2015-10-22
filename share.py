# -*- coding: utf-8 -*-
from logging.handlers import TimedRotatingFileHandler
import os
import logging
import time
import urllib
import urllib2
import web
try:
    import simplejson as json
except ImportError:
    import json
# 测试账号
appid_secret = r'appid=XXXXXXXXX&secret=XXXXXXXX'
# access_token = None

logfilename = '/var/log/revieve.log'
logformat = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(funcName)s %(message)s'
loglevel = logging.INFO
logger = logging.getLogger(__file__)
hdlr = TimedRotatingFileHandler(logfilename, when='D', interval=1, backupCount=40)
hdlr.setFormatter(logging.Formatter(logformat))
logger.addHandler(hdlr)
logger.setLevel(loglevel)



def get_json(url, data=None):
    req = urllib2.Request(url, data=data)
    content = urllib2.urlopen(req).read()
    result = json.loads(content)
    if check_error(result):
        return result
    else:
        return None


def check_error(json_result):
    if not json_result:
        return False

    if not isinstance(json_result, dict):
        return False

    errcode = json_result.get("errcode")
    if errcode:
        print u"发生错误：", str(errcode), (json_result.get("errmsg"))
        return False
    return True


# 获取access_token ,需要记录过期时间，默认7200秒，需要注意缓存。
def get_access_token():
    url = r'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&' + appid_secret
    result = get_json(url)
    if not result:
        logger.error(u"获取token失败")
        return None
    web.ctx.globals.access_token = result.get("access_token")
    web.ctx.globals.expiered_time = result.get("expires_in") + time.time()
    logger.info(u"刷新了token", web.ctx.globals.access_token)
    return web.ctx.globals.access_token


def get_newest_token():
    if not web.ctx.globals.access_token or time.time() - web.ctx.globals.expiered_time > 1000:
        return get_access_token()
    else:
        return web.ctx.globals.access_token

def send_kefu_message(msg):
    access_token = get_newest_token()
    logger.info("share:access_token:", access_token)
    logger.info("share:lastopenid:", web.ctx.globals.lastopenid)

    weixin_msg = {
            "touser": web.ctx.globals.lastopenid,
            "msgtype": "text",
            "text":
            {
                 "content": msg
            }
          }
    data = urllib.urlencode(weixin_msg)
    req = urllib2.Request("https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % access_token,
                          data=data)
    content = urllib2.urlopen(req).read()
    result = json.loads(content)
    print repr(result)
    if check_error(result):
        return result
    else:
        return None
