# -*- coding: utf-8 -*-
# from odoo import http


# class ViinHrWorkEntries(http.Controller):
#     @http.route('/viin_hr_work_entries/viin_hr_work_entries', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/viin_hr_work_entries/viin_hr_work_entries/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('viin_hr_work_entries.listing', {
#             'root': '/viin_hr_work_entries/viin_hr_work_entries',
#             'objects': http.request.env['viin_hr_work_entries.viin_hr_work_entries'].search([]),
#         })

#     @http.route('/viin_hr_work_entries/viin_hr_work_entries/objects/<model("viin_hr_work_entries.viin_hr_work_entries"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('viin_hr_work_entries.object', {
#             'object': obj
#         })
