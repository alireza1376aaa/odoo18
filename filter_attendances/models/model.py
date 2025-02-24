# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, exceptions, _


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    
    @api.model
    def create(self, vals):
        """ جلوگیری از ایجاد رکورد برای کاربران محدود """
        if self.env.user.has_group('filter_attendances.group_hr_attendance_restricted'):
            raise models.ValidationError("شما مجاز به ایجاد رکورد جدید نیستید!")
        return super(HrAttendance, self).create(vals)