# model 信息

本模块采用华信短信服务提供商提供的 WSDL 短信服务

python depends: suds

## SMSSendConfig 类

定义了odoo数据对象sms_send.config，用于保存短信账户信息如用户名和密码

- 基本属性：name, url, username, password

> name: 别名
> 
> url: 服务接口URL
> 
> username: 账户名
> 
> password: 账户密码


## SMSSender 类

odoo 'sms_send.sender'

负责短信发送

TransientModel，不会在odoo上显示以往记录

- 基本属性：config, mobiles, content, suffix, extnumber, plansendtime

> config: 关联的sms_send.config
> 
> mobiles: 短信接收手机号
> 
> content: 短信内容
> 
> suffix: 公司后缀。根据手册，后缀也是必填项。
> 
> extnumber: 扩展子号
> 
> plansendtime: 定时发送时间

- 基本方法：send, log

send: 依赖python suds包。根据填写的信息构造请求参数，发送短信并写入日志。

log: 记录短信日志

## SMSSendlog 类

记录短信发送日志

- 基本属性：上述class的属性构造而成

# 短信发送

```python
config = self.env['sms_send.config']
sender = self.env['sms_send.sender']
conf = config.search([ domain ])
args = {'config': conf.id, 'mobiles': XXXXXXXXXXX, 'content': 'Message body', 'suffix': 'odoo', ...}
sender.create(args).send()
```
