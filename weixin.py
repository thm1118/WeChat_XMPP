# -*- coding: utf-8 -*-
import sys
import web
from recieve import EchoBot
import time

from weixinInterface import WeixinInterface
import sleekxmpp

if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding

    setdefaultencoding('utf8')
else:
    raw_input = input

from send_client import SendMsgBot

urls = (
    '/', 'index',
    '/weixin', 'WeixinInterface',
)

xmppServer = 'XXXX'
xmppServerPort = 5222

class index:
    def GET(self):
        xmpp = SendMsgBot("weixin@XXXX", 'a', "tiger@XXXX", u"微信服务启动")
        print "SendMsgBot"
        xmpp.register_plugin('xep_0030')  # Service Discovery
        xmpp.register_plugin('xep_0199')  # XMPP Ping
        if xmpp.connect((xmppServer, xmppServerPort)):
            xmpp.process(block=False)
        else:
            print "XXXX"
        return "Hello, world!"


def add_global_hook():
    g = web.storage({"lastopenid": None, "access_token":None, "expiered_time": time.time()})

    def _wrapper(handler):
        web.ctx.globals = g
        return handler()

    return _wrapper


if __name__ == "__main__":
    xmpp = EchoBot('weixin@XXX', 'a')
    xmpp.connect()
    xmpp.process(block=False)
    app = web.application(urls, globals())
    app.add_processor(add_global_hook())
    app.run()
