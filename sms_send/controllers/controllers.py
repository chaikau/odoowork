# -*- coding: utf-8 -*-
from openerp import http

# class MsmSend(http.Controller):
#     @http.route('/sms_send/sms_send/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sms_send/sms_send/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sms_send.listing', {
#             'root': '/sms_send/sms_send',
#             'objects': http.request.env['sms_send.sms_send'].search([]),
#         })

#     @http.route('/sms_send/sms_send/objects/<model("sms_send.sms_send"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sms_send.object', {
#             'object': obj
#         })