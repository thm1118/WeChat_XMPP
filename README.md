# WeChat XMPP
    
   微信服务号集成XMPP服务，实现消息对接.
   
   服务端：使用web.py构建微信服务号服务，[OpenFire](http://www.igniterealtime.org/projects/openfire/) 作为XMPP服务.
   
   客户端：微信， [Conversations](https://github.com/siacs/Conversations) 作为mpp/jaber 移动客户端。
   
   本项目就是python实现的微信服务，并对微信消息，xmpp消息做相互转发。出于技术演示目的，仅仅以从微信服务号最近一次发送信息的微信用户为xmpp的发送对象。
   
   
## 基础环境和配置

- 搭建[OpenFire](http://www.igniterealtime.org/projects/openfire/)

    启动服务后，建立两个用户，一个代表微信发来的用户，比如weixin@XXXX， 一个是用来在客户端登录用的用户，比如 tiger@XXX
    
    注意如果服务可以对应域名，则使用域名，否则只能使用IP。上例的用户名@后，即为域名或IP。
    
- 微信服务号服务:

    python 2.x
    
    `pip install web.py`
    
    `pip install sleekxmpp`

- 微信服务号测试号

    申请微信服务号，获得的appid 与secret 在share.py 中的appid_secret变量上配置。
    
    OpenFire 服务的域名或者IP 配置在 weixin.py 的 `xmppServer = 'XXXX' xmppServerPort = 5222` 变量上
    
    对代码中的使用用户 weixin@XXXX，或  tiger@XXX 等 进行替换（出于技术验证目的，没有抽取配置,:)）。注意密码
    
    启动微信服务号服务，在微信官方管理后台内，配置微信服务号的IP地址，验证通过。
    
## 服务运行
   `python weixin.py`
    
    
## 注意：

   本项目是技术实现验证为目的，如果打算产品化，需要实现xmpp服务用户与微信服务号用户的对应关系，推荐在Openfire内实现用户自动转换插件。

