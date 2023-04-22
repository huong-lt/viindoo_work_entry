from odoo import models, fields, api, tools


class WorkEntryReport(models.Model):
    _name = 'work.entry.report'
    _description = 'Work Entry Analysis'
    _auto = False
    employee_id = fields.Many2one('hr.employee', readonly=True)
    work_entry_type_id = fields.Many2one('hr.work.entry.type', readonly=True)
    name = fields.Char(string='Name', readonly=True)
    state = fields.Char(readonly=True)
    conflict = fields.Boolean(readonly=True)
    active = fields.Boolean(readonly=True)
    date_start = fields.Date(string='Start Date', readonly=True)
    date_stop = fields.Date(string='End Date', readonly=True)
    
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
       CREATE OR REPLACE VIEW %s AS (%s %s)
        """ % (self._table, self._select(), self._from()))

    def _select(self):
        return """
        SELECT we.id AS id, 
            hr.id AS employee_id, 
            we_type.id AS work_entry_type_id, 
            we.name AS name, 
            we.state AS state, 
            we.conflict AS conflict, 
            we.active AS active, 
            we.date_start AS date_start, 
            we.date_stop AS date_stop
        """
    
    def _from(self):
        return """
        FROM hr_work_entry we
            JOIN hr_employee hr on  we.employee_id=hr.id
            JOIN hr_work_entry_type we_type on we.work_entry_type_id=we_type.id
        """
        
