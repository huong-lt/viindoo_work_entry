from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_to_hr_payroll = fields.Boolean(string='Work Entry Payroll Integration')
    module_viin_hr_holidays = fields.Boolean(string='Work Entry Holiday Integration')
    module_viin_hr_contract=fields.Boolean(string='Work Entry Contract Integration')
    module_hr_attendance=fields.Boolean(string='Work Entry Attendance Integration')
    module_viin_hr_overtime=fields.Boolean(string='Work Entry Overtime Integration')