from odoo.tests.common import TransactionCase, Form
from odoo import fields

class Common(TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super(Common, cls).setUpClass()
        # company
        cls.company_demo = cls.env['res.company'].create({
            'name': 'Company demo'
            })  
        # Job
        cls.job_product_dev = cls.create_job('Product Developer')
        cls.job_product_manager = cls.create_job('Product Department - Manager')
        cls.job_qaqc_manager = cls.create_job('QA/QC Department - Manager')
        #
        # Employee
        cls.product_emp_A = cls.create_employee(
            'Product Employee 1',
            job_id=cls.job_product_dev.id)
        cls.product_dep_manager = cls.create_employee(
            'Product Department Manager',
            job_id=cls.job_product_manager.id)
        cls.qaqc_dep_manager = cls.create_employee(
            'QA/QC Department Manager',
            job_id=cls.job_qaqc_manager.id)
        
        # Department
        members = [cls.product_emp_A.id, cls.product_dep_manager.id]
        cls.product_department = cls.create_department(
            'Product Department',
        cls.product_dep_manager.id,
        members)
        cls.qaqc_department = cls.create_department(
            'QA/QC Department',
        cls.qaqc_dep_manager.id)
        
    @classmethod
    def create_user(cls, name, login, email_name, groups_ids):
        Users = cls.env['res.users'].with_context({
            'no_reset_password': True,
            'mail_create_nosubscribe': True
        })
        return Users.create({
            'name': name, 'login': login,
            'email': '%s@example.viindoo.com' % (email_name),
            'groups_id': [(6, 0, groups_ids)]
        })
    @classmethod
    def create_partner(cls, name):
        return cls.env['res.partner'].with_context(tracking_disable=True).create({
            'name': name,
            'country_id': cls.env.company.country_id.id
        })
    @classmethod
    def create_employee(cls, name, job_id=None, department_id=None):
        asdress_home_id = cls.create_partner('name')
        return  cls.env['hr.employee'].with_context(tracking_disable=True).create({
            'name': name,
            'job_id': job_id,
            'department_id': department_id,
            'address_home_id': asdress_home_id.id
        })
        
    @classmethod
    def create_contract(cls, employee_id, start, end=None, state='open', wage=None, department_id=False, job_id=False):
        return cls.env['hr.contract'].with_context(tracking_disable=True).create({
            'name': 'Contract',
            'employee_id': employee_id,
            'state': state,
            'date_start': start,
            'date_end': end,
            'kanban_state': 'normal',
            'wage': wage or 15000000,
            'department_id': department_id or cls.product_department.id,
            'job_id': job_id or cls.job_product_dev.id,
            'hr_responsible_id': cls.env.ref('base.user_admin').id
        })

    @classmethod
    def create_department(cls, name, manager_id=False, employee_ids=None):
        if not employee_ids:
            employee_ids = []
        return cls.env['hr.department'].with_context(tracking_disable=True).create({
                'name': name,
                'manager_id': manager_id,
                'member_ids': [(6, 0, employee_ids)]
            })    
    @classmethod
    def create_job(cls, name):
        return cls.env['hr.job'].with_context(tracking_disable=True).create({'name': name})
    
    @classmethod
    def create_work_entry(cls, employee_id, start, end, department_id=False):
        return cls.env['hr.work.entry'].with_context(tracking_disable=True).create({
            'employee_id': employee_id,
            'date_start': start,
            'date_stop': end,
            'state': 'draft',
            'active': True,
            'conflict': False,
            'name':'Attendance: %s'%employee_id,
            'work_entry_type_id': 1,
            'company_id': cls.env.company.id,
            'department_id': department_id or cls.product_department.id,
        })
