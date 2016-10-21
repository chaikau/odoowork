# -*- coding: utf-8 -*-
{
    'name': "sms_send",

    'summary': """
    发送短信
        """,

    'description': """基于WSDL服务的短信发送模块

短信模块

功能：

- 发送短信

- 配置短信发送

- 短信历史记录

**发送规则**：

- 同一个号码，发送内容带有（验证码），3分钟之内只能3条，超过3条，系统会默认为（恶意注册）

- 同一个号码，系统默认一天之内只能发送10条信息，超过10条会超限失败（特殊号码、或特殊客户需要找客服处理）

- 短信内请勿出现“测试”字样，如有需要，请联系工作人员进行报备

模块：

- 短信配置、短信发送、短信发送记录（日志）

视图：

同上

用户组及其权限（设置界面）：

1. 普通用户：

- 发送短信

- 短信配置（部分可见，只读）

- 历史记录（只读）

2. 管理员：所有权限
""",

    'author': "OdooStart",
    'website': "http://www.odoostart.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/sms_send_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
