from odoo import models, fields, api
from datetime import datetime, timedelta


class AutoAttendance(models.Model):
    _inherit = 'hr.attendance'

    @api.model
    def auto_check_in(self, user):
        employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        if employee:
            last_attendance = self.search([('employee_id', '=', employee.id)], order="check_in desc", limit=1)

            if not last_attendance or last_attendance.check_out:
                self.create({'employee_id': employee.id, 'check_in': fields.Datetime.now()})
                self.env.cr.commit()

    @api.model
    def auto_check_out(self):
        now = datetime.now()
        inactive_threshold = now - timedelta(minutes=5)
        active_sessions = self.env['bus.presence'].search([('status','=','online')]).mapped('user_id.id')
    

        attendances = self.search([
            ('check_out', '=', False),
            ('check_in', '<', inactive_threshold)
        ])
        
        for attendance in attendances:
            if attendance.employee_id.user_id.id not in active_sessions:
                attendance.write({'check_out': fields.Datetime.now()})
                self.env.cr.commit()
            else:
                pass
