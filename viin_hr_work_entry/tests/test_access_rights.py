from odoo import fields
from odoo.exceptions import AccessError
from odoo.tests import tagged

from .common import Common


@tagged('post_install', '-at_install')
class TestAccessRight(Common):
    
    def setUp(self):
        super(TestAccessRight, self).setUp()

        # group user
        group_internal = self.env.ref('base.group_user')
        group_hr_officer = self.env.ref('hr.group_hr_user')
        group_work_entry_user = self.env.ref('viin_hr_work_entry.work_entry_group_user')
        group_work_entry_admin = self.env.ref('viin_hr_work_entry.work_entry_group_admin')
        # User - employee
        groups_ids = [group_internal.id]
        self.leader_user = self.create_user('Leader User', 'leader_user', 'leader_user', groups_ids)
        self.leader_user.action_create_employee()
        self.leader_employee = self.leader_user.employee_id

        groups_ids = [group_internal.id, group_work_entry_user.id]
        self.officer_user = self.create_user('Officer User', 'officer_user', 'officer_user', groups_ids)
        self.officer_user.action_create_employee()
        self.officer_employee = self.officer_user.employee_id

        groups_ids = [group_internal.id, group_work_entry_admin.id]
        self.manager_user = self.create_user('Manager User', 'manager_user', 'manager_user', groups_ids)
        self.manager_user.action_create_employee()
        self.manager_employee = self.manager_user.employee_id

        groups_ids = [group_internal.id]
        self.product_user_1 = self.create_user('Product Employee 1', 'product_employee1', 'product_employee1', groups_ids)
        self.product_user_1.action_create_employee()
        self.product_employee_1 = self.product_user_1.employee_id

        self.product_user_2 = self.create_user('Product Employee 2', 'product_employee2', 'product_employee2', groups_ids)
        self.product_user_2.action_create_employee()
        self.product_employee_2 = self.product_user_2.employee_id

        self.product_department_user = self.create_user(
            'Product Department Manager',
            'product_department_user',
            'product_department_user',
            groups_ids)

        self.contract_employee_1 = self.create_contract(
            self.product_employee_1.id,
            fields.Date.from_string('2021-1-1'),
            wage=35000000)
        self.contract_employee_2 = self.create_contract(
            self.product_employee_2.id,
            fields.Date.from_string('2021-1-1'),
            wage=35000000)
        self.contract_team_leader = self.create_contract(
            self.leader_employee.id,
            fields.Date.from_string('2021-1-1'),
            wage=35000000)
        self.contract_officer_employee = self.create_contract(
            self.officer_employee.id,
            fields.Date.from_string('2021-1-1'),
            wage=35000000)
        self.contract_qaqc_employee = self.create_contract(
            self.qaqc_dep_manager.id,
            fields.Date.from_string('2021-1-1'),
            wage=35000000)


    def test_access_rights_1(self):
        """
        Case 1: User is Admin, having full CRUD rights
        """
        self.assertTrue(self.env['hr.work.entry'].with_user(self.env.ref('base.user_admin')).check_access_rights('read'))
        self.assertTrue(self.env['hr.work.entry'].with_user(self.env.ref('base.user_admin')).check_access_rights('write'))
        self.assertTrue(self.env['hr.work.entry'].with_user(self.env.ref('base.user_admin')).check_access_rights('create'))
        self.assertTrue(self.env['hr.work.entry'].with_user(self.env.ref('base.user_admin')).check_access_rights('unlink'))


    def test_access_rights_2(self):
        """
        Case 2: User is internal user, only able to read record
        """
        WorkEntry = self.env['hr.work.entry'].with_user(self.product_user_1)
        self.assertTrue(WorkEntry.check_access_rights('read'), 'Test Access Right (Work Entry) for internal user not oke')
        self.assertRaises(AccessError, WorkEntry.check_access_rights, 'create')
        self.assertRaises(AccessError, WorkEntry.check_access_rights, 'write')
        self.assertRaises(AccessError, WorkEntry.check_access_rights, 'unlink')
        
    def test_work_entry_security_internal_user(self):
        """
        1. Người dùng nội bộ
                TH1: Nhìn thấy Work entry của chính mình
                TH2: Không nhìn thấy Work entry của người khác
        """
        # Prepare data for test access rule
        work_entry_1 = self.create_work_entry(
            self.product_employee_1.id,
            fields.Datetime.from_string('2023-04-01 06:00:00'),
            fields.Datetime.from_string('2023-04-01 10:00:00'))

        work_entry_2 = self.create_work_entry(
            self.product_employee_2.id,
            fields.Datetime.from_string('2023-04-01 06:00:00'),
            fields.Datetime.from_string('2023-04-01 10:00:00'))
         
        # TH1: Work entry của chính mình
        self.assertIsNone(work_entry_1.with_user(
            self.product_user_1).check_access_rule('read'),
            'Test access rule (Work entry) for internal user not oke')

        # TH2: Work entry của người khác
        self.assertRaises(AccessError, work_entry_2.with_user(self.product_user_1).check_access_rule, 'read')

          
    def test_work_entry_security_team_leader_1(self):
        """
        1. Người dùng trưởng nhóm
            Case 1: Check quyền truy cập bản ghi work entry (Access Rules)
                 Nhìn thấy Work entry của mình và nhân viên thuộc phòng ban mình quản lý
        """
        self.product_employee_2.write({
            'parent_id': False,
            'department_id': self.product_department.id,
        })
        self.product_department.write({
            'manager_id': self.leader_employee.id
        })
        work_entry_1 = self.create_work_entry(
            self.product_employee_2.id,
            fields.Datetime.from_string('2023-04-01 06:00:00'),
            fields.Datetime.from_string('2023-04-01 10:00:00'))
        work_entry_2 = self.create_work_entry(
            self.leader_employee.id,
            fields.Datetime.from_string('2023-04-01 06:00:00'),
            fields.Datetime.from_string('2023-04-01 10:00:00'))
        self.assertIsNone(
            work_entry_1.with_user(self.leader_user).check_access_rule('read'),
            'Test access rule (Work entry) for team leader not oke')
        self.assertIsNone(
            work_entry_2.with_user(self.leader_user).check_access_rule('read'),
            'Test access rule (Work entry) for team leader not oke')
        
    def test_work_entry_security_team_leader_2(self):
        """
        1. Người dùng trưởng nhóm
            Case 2: Check quyền truy cập bản ghi Work entry (Access Rules)
                 Work entry của người khác, không thuộc phòng ban quản lý
        """
        self.qaqc_dep_manager.write({
            'department_id':self.qaqc_department.id
        })
        work_entry = self.create_work_entry(
            self.qaqc_dep_manager.id,
            fields.Datetime.from_string('2023-04-01 06:00:00'),
            fields.Datetime.from_string('2023-04-01 10:00:00'))
        self.assertRaises(AccessError, work_entry.with_user(self.leader_user).check_access_rule, 'read')    
    
    def test_work_entry_security_officer_0(self):
        """
        1. Người dùng cán bộ
            Case 0: Có quyền Officer (hr.group_hr_user) của HR
        """
        self.assertTrue(
            self.officer_user.has_group('viin_hr_work_entry.work_entry_group_user'),
            'Test Officer (hr.group_hr_user) not oke')

    def test_work_entry_security_officer_1(self):
        """
        3. Người dùng cán bộ
            Case 1: Check quyền truy cập của người dùng trưởng nhóm (Access Rights)
                TH1: Check quyền truy cập model work entry
        """
        # TH1: Check quyền truy cập model Work entry
        work_entry = self.env['hr.work.entry'].with_user(self.officer_user)
        self.assertTrue(work_entry.check_access_rights('read'), 'Test Access Right (Work entry) for officer not oke')
        self.assertTrue(work_entry.check_access_rights('create'), 'Test Access Right (Work entry) for officer not oke')
        self.assertTrue(work_entry.check_access_rights('write'), 'Test Access Right (Work entry) for officer not oke')
        self.assertTrue(work_entry.check_access_rights('unlink'), 'Test Access Right (Work entry) for officer not oke')
  
    # 3. Người dùng cán bộ
    def test_work_entry_security_officer_2(self):
        """
        Case 2: Check quyền truy cập bản ghi work entry (Access Rules)
            TH1: work entry của chính mình
                Output: không có quyền sửa xóa work entry của chính mình
        """
        work_entry = self.create_work_entry(
            self.officer_employee.id,
            fields.Datetime.from_string('2023-04-01 06:00:00'),
            fields.Datetime.from_string('2023-04-01 10:00:00'))
        self.assertIsNone(
            work_entry.with_user(self.officer_user).check_access_rule('read'),
        'Test access rule (Work entry) for officer not oke')
        self.assertRaises(AccessError, work_entry.with_user(self.officer_user).check_access_rule, 'write')
        self.assertRaises(AccessError, work_entry.with_user(self.officer_user).check_access_rule, 'unlink')
    
    # 3. Người dùng cán bộ
    def test_work_entry_security_officer_3(self):
        """
        Case 2: Check quyền truy cập bản ghi Work entry (Access Rules)
            TH2: Work entry của nhân viên cấp dưới
                Output: Full quyền
        """
        self.product_employee_2.write({'parent_id': self.officer_employee.id})
        work_entry = self.env['hr.work.entry'].with_user(self.officer_user).create({
            'employee_id': self.product_employee_2.id,
            'date_start': fields.Datetime.from_string('2023-04-01 06:00:00'),
            'date_stop': fields.Datetime.from_string('2023-04-01 10:00:00'),
            'state': 'draft',
            'active': True,
            'conflict': False,
            'name':'Attendance: %s'%self.product_employee_2,
            'work_entry_type_id': 1,
            'department_id': self.product_department.id,
            'company_id': self.env.company.id
        })
        self.assertIsNone(
            work_entry.with_user(self.officer_user).check_access_rule('read'),
            'Test access rule (Work entry) for officer not oke')
        self.assertIsNone(
            work_entry.with_user(self.officer_user).check_access_rule('write'),
            'Test access rule (Work entry) for officer not oke')
        self.assertIsNone(
            work_entry.with_user(self.officer_user).check_access_rule('unlink'),
            'Test access rule (Work entry) for officer not oke')
    
    def test_work_entry_security_manager_0(self):
        """
        1. Người dùng quản lý
            Case 0: Có quyền Administrator (hr_contract.group_hr_contract_manager) của HR Contract
        """
        self.assertTrue(
            self.manager_user.has_group('hr_contract.group_hr_contract_manager'),
            'Test Contract Manager (hr_contract.group_hr_contract_manager) not oke')
        self.assertTrue(
            self.manager_user.has_group('viin_hr_work_entry.work_entry_group_admin'),
            'Test Contract Manager (hr.group_hr_user) not oke')
