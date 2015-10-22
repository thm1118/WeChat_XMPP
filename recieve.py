# -*- coding: utf-8 -*-
import logging
from logging.handlers import TimedRotatingFileHandler
import web
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from share import send_kefu_message

logfilename = '/var/log/revieve.log'
logformat = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(funcName)s %(message)s'
loglevel = logging.INFO
logger = logging.getLogger(__file__)
hdlr = TimedRotatingFileHandler(logfilename, when='D', interval=1, backupCount=40)
hdlr.setFormatter(logging.Formatter(logformat))
logger.addHandler(hdlr)
logger.setLevel(loglevel)

class EchoBot(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

        # If you wanted more functionality, here's how to register plugins:
        # self.register_plugin('xep_0030') # Service Discovery
        # self.register_plugin('xep_0199') # XMPP Ping

        # Here's how to access plugins once you've registered them:
        # self['xep_0030'].add_feature('echo_demo')

        # If you are working with an OpenFire server, you will
        # need to use a different SSL version:
        # import ssl
        # self.ssl_version = ssl.PROTOCOL_SSLv3

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

        # Most get_*/set_* methods from plugins use Iq stanzas, which
        # can generate IqError and IqTimeout exceptions
        #
        # try:
        #     self.get_roster()
        # except IqError as err:
        #     logging.error('There was an error getting the roster')
        #     logging.error(err.iq['error']['condition'])
        #     self.disconnect()
        # except IqTimeout:
        #     logging.error('Server is taking too long to respond')
        #     self.disconnect()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal') and web.ctx.globals.lastopenid:
            # msg.reply("Thanks for sending\n%(body)s" % msg).send()
            logger.info("recieve: lastopenid", web.ctx.globals.lastopenid)
            logger.info("xmp message", repr(msg))

            send_kefu_message(msg["body"])
        else:
            msg.reply(u"没有收到微信消息，缺少openid：\n%(body)s" % msg).send()


if __name__ == '__main__':
    # Ideally use optparse or argparse to get JID,
    # password, and log level.

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

    xmpp = EchoBot('weixin@XXXX', 'a')
    xmpp.connect()
    xmpp.process(block=True)
