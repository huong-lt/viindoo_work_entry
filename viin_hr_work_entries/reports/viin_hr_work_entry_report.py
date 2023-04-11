from odoo import models, fields, api, tools


class AcademyReport(models.Model):
    _name = 'academy.report2'
    _description = 'Academy Report 2'
    _auto=False
    student_id = fields.Many2one('education.student', readonly=True)
    class_id = fields.Many2one('education.class', readonly=True)
    ethnic_id = fields.Many2one('res.ethnic', readonly=True)
    date = fields.Date(string='Enroll Date', readonly=True)
    start_date = fields.Date(string='Start Date', readonly=True)
    end_date = fields.Date(string='End Date', readonly=True)
    
    
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
       CREATE OR REPLACE VIEW %s AS (%s %s)
        """%(self._table, self._select(), self._from()))

    def _select(self):
        return """
        SELECT enrollment.id AS id,
            student.id AS student_id,
            class.id AS class_id,
            enrollment.date AS date,
            class.start_date AS start_date,
            class.end_date AS end_date,
            eth.id AS ethnic_id
        """
    
    def _from(self):
        return """
        FROM education_enrollment enrollment
            JOIN education_student student ON enrollment.student_id = student.id
            JOIN education_class class ON enrollment.class_id = class.id
            LEFT JOIN res_ethnic eth ON eth.id = student.ethnic_id
        """
        
        
        