#coding:UTF-8
import hashlib
from logging.handlers import TimedRotatingFileHandler
import web
import time
import os
from lxml import etree
from send_client import SendMsgBot
import logging
logfilename = '/var/log/revieve.log'
logformat = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(funcName)s %(message)s'
loglevel = logging.INFO
logger = logging.getLogger(__file__)
hdlr = TimedRotatingFileHandler(logfilename, when='D', interval=1, backupCount=40)
hdlr.setFormatter(logging.Formatter(logformat))
logger.addHandler(hdlr)
logger.setLevel(loglevel)

class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
        self.content = None
        self.msgType = None
        self.fromUser = None
        self.toUser = None
        self.eventKey = None
        self.Label = None
        self.Title = None
        self.MediaId = None
        self.PicUrl = None
        self.MsgId = 0
        self.xmpp = SendMsgBot("weixin@XXX", 'a', "tiger@XXX", u"测试消息")
        self.xmpp.register_plugin('xep_0030') # Service Discovery
        self.xmpp.register_plugin('xep_0199') # XMPP Ping
        self.xmpp.connect()
        if self.xmpp.connect():
            print u"连接xmpp成功"
        else:
            print u"连接xmpp失败"

    def GET(self):
        #获取输入参数
        data = web.input()

        # if data is None | data.signature is None | data.timestamp is None \
        #         | data.timestamp is None | data.echostr is None:
        if not data or "signature" not in data:
            print u"有人扫描,注意注意"
            return u"不要扫描，请不要扫描"
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        #自己的token
        token = "thm1118"
        #字典序排序
        list = [token, timestamp, nonce]
        list.sort()
        #sha1加密算法
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            print u"是微信请求，已通过"
            return echostr
        else:
            print u"不是微信请求，要注意要注意"
        
    def POST(self):
        global lastopenid
        #从获取的xml构造xml dom树
        str_xml = web.data()
        xml = etree.fromstring(str_xml)
        print str_xml
        #提取信息
        self.content = "" if xml.find("Content") is None else xml.find("Content").text
        self.msgType = "" if xml.find("MsgType") is None else xml.find("MsgType").text
        self.fromUser = "" if xml.find("FromUserName") is None else xml.find("FromUserName").text
        lastopenid = self.fromUser
        web.ctx.globals.lastopenid = lastopenid

        self.toUser = "" if xml.find("ToUserName") is None else xml.find("ToUserName").text
        self.Label = "" if xml.find("Label") is None else xml.find("Label").text
        self.Title = "" if xml.find("Title") is None else xml.find("Title").text
        self.MediaId = "" if xml.find("MediaId") is None else xml.find("MediaId").text
        self.PicUrl = "" if xml.find("PicUrl") is None else xml.find("PicUrl").text
        return self.process_msg_type(self.msgType, xml, str_xml)

    #返回消息问题
    def reply_text(self, replytext):
        print "回复消息为：", replytext
        #模板渲染
        return self.render.reply_text(self.fromUser, self.toUser, int(time.time()), replytext)

    #处理消息类型
    def process_msg_type(self, msgtype, xml, str_xml):
        if not msgtype:
            return self.reply_text(u"消息类型为空")
        elif msgtype == 'event':
            event = xml.find("Event").text
            return self.process_event_msg(event, xml, str_xml)
        elif msgtype == "text":
            if self.xmpp.connect():
                self.xmpp.msg = self.content
                self.xmpp.process(block=True)
            else:
                print u"连接xmpp失败，无法发送消息"
            return self.reply_text(u"你刚才发来的文本消息是："+self.content)
        elif msgtype == "image":
            return self.reply_text(u"你刚才发来的消息是图片："+self.PicUrl)
        elif msgtype == "voice":
            return self.reply_text(u"你刚才发来的消息是声音剪辑："+self.MediaId)
        elif msgtype == "video":
            return self.reply_text(u"你刚才发来的消息是视频："+self.MediaId)
        elif msgtype == "location":
            return self.reply_text(u"你刚才发来的消息是定位："+self.Label)
        elif msgtype == "link":
            return self.reply_text(u"你刚才发来的消息是链接："+self.Title)
        else:
        #未知消息类型
            return self.reply_text(u"未处理的消息类型："+msgtype)

    #当消息是 event类型时，处理各种事件类型：todo：测试阶段，都直接发回微信post消息，以便检查
    def process_event_msg(self, event, xml, str_xml):
        self.eventKey = 0 if xml.find("EventKey") is None else xml.find("EventKey").text
        self.MsgId = 0 if xml.find("MsgId") is None else xml.find("MsgId").text
        #触发条件：用户已关注该公众帐号，扫描了带场景值的二维码
        if event == 'SCAN':
            return self.reply_text(u"你已关注，是再次扫描。二维码场景值："+self.eventKey)
        #触发条件：用户通过带场景值二维码订阅公众号。
        elif event == 'subscribe':
            return self.reply_text(u"你刚关注，二维码场景值："+self.eventKey)
        elif event == 'CLICK':
            return self.reply_text(u"你点击了菜单，触发CLICK事件："+self.eventKey)
        return self.reply_text(u"未处理的的事件类型："+event)

