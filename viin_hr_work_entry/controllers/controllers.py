# -*- coding: utf-8 -*-
# from odoo import http


# class ViinHrWorkEntries(http.Controller):
#     @http.route('/viin_hr_work_entry/viin_hr_work_entry', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viin_hr_work_entry/viin_hr_work_entry/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('viin_hr_work_entry.listing', {
#             'root': '/viin_hr_work_entry/viin_hr_work_entry',
#             'objects': http.request.env['viin_hr_work_entry.viin_hr_work_entry'].search([]),
#         })

#     @http.route('/viin_hr_work_entry/viin_hr_work_entry/objects/<model("viin_hr_work_entry.viin_hr_work_entry"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viin_hr_work_entry.object', {
#             'object': obj
#         })
