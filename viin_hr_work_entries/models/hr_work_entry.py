from odoo import models, fields, api

class HrWorkEntry(models.Model):
    #_name = 'hr.work.entry'
    _description = 'Work Entries'
    _inherit = ['hr.work.entry']