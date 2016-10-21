# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from suds.client import Client
from suds import WebFault
from urllib2 import HTTPError, URLError
from suds.transport.http import TransportError
import logging
import datetime
logger = logging.getLogger(__name__)

class SMSSendConfig(models.Model):
    _name = 'sms_send.config'
    name = fields.Char("账号别名", help="为账号起一个别名")
    url = fields.Char("URL", default="https://dx.ipyy.net/webservice.asmx?wsdl", required=True)
    username = fields.Char("用户名", required=True)
    password = fields.Char("密码", required=True)


class SMSSender(models.TransientModel):
    _name = 'sms_send.sender'
    config = fields.Many2one("sms_send.config", string="短信配置", required=True)
    mobiles = fields.Text("手机号", required=True, help="多个手机号用“,”分隔")
    content = fields.Text("短信内容", required=True)
    suffix = fields.Char("公司后缀", required=True)
    extnumber = fields.Char("扩展子号",default='')
    plansendtime = fields.Datetime("短信发送时间", default=None)

    @api.multi
    def log(self, logtype='' ,response=''):
        smslog = self.env['sms_send.sendlog']
        return smslog.create({'config': self.config.id,
            'mobiles': self.mobiles,
            'content': self.contentfix,
            'extnumber': self.extnumber,
            'plansendtime': self.plansendtime,
            'logtype': logtype,
            'response': response,
            })

    @api.multi
    def send(self):
        if not self.mobiles:
            raise exceptions.Warning('请填写手机号')
        if not self.content:
            raise exceptions.Warning('请填写短信内容')
        if not self.suffix:
            raise exceptions.Warning('请填写短信后缀')

        self.mobiles = self.mobiles.replace(u'，', u',')
        self.contentfix = self.content + u'【%s】' % self.suffix
        sms={"Msisdns": self.mobiles, "SMSContent": self.contentfix}
        if self.extnumber:
            sms['ExtNumber']=self.extnumber
        else:
            sms['ExtNumber']=''
        if self.plansendtime:
            # CST = UTC + 9h 中国标准时间(东八区)
            CST = datetime.datetime.strptime(self.plansendtime, DEFAULT_SERVER_DATETIME_FORMAT) + datetime.timedelta(hours=8)
            sms['PlanSendTime'] = datetime.datetime.strftime(CST, "%Y-%m-%dT%H:%M:%S")
        logger.info('Send Message: ' + str(sms))

        try:
            client = Client(self.config.url)
            rlt = client.service.SendSms(self.config.username, self.config.password, sms)
        except WebFault as e:
            log = self.log(logtype = 'Web Fault', response = str(e))
        except (TransportError, HTTPError, URLError) as e:
            log = self.log(logtype = 'URL Error', response = str(e))
        except Exception as e:
            log = self.log(logtype = 'Unknown Error', response = str(e))
        else:
            response = \
u"""返回信息提示：{info}
返回状态为：{state}
返回余额：{left}
返回本次任务ID：{taskid}
返回成功短信数：{count}""".format(
                    info = getattr(rlt,'Description', 'N/A'), 
                    state = getattr(rlt, 'StatusCode', 'N/A'), 
                    left = getattr(rlt, 'Amount','N/A'), 
                    taskid = getattr(rlt, 'MsgId','N/A'), 
                    count = getattr(rlt, 'SuccessCounts','N/A')
                    )
            log = self.log(logtype = getattr(rlt, 'StatusCode', 'N/A'), response = response)
        return {
           'type': 'ir.actions.act_window',
           'res_model': 'sms_send.sendlog',
           'res_id': log.id,
           'view_mode': 'form',
           'target': 'new',
           }


class SMSSendlog(models.Model):
    _name = 'sms_send.sendlog'
    config = fields.Many2one("sms_send.config", string="账号配置", readonly=True)
    user_id = fields.Many2one("res.users", string="发送者", readonly=True, default=lambda self: self.env.uid, read=['sms_send.group_sms_send_user'])
    logtype = fields.Char("日志类型")
    mobiles = fields.Text("手机号", required=True)
    content = fields.Text("短信内容", required=True)
    #suffix = fields.Char("公司后缀", required=True)
    extnumber = fields.Char("扩展子号",default = '')
    plansendtime = fields.Datetime("发送时间", default = None)
    response = fields.Text("发送结果", default = None)

