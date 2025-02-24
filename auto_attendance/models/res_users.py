from odoo import models, api, fields
import logging

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    # @classmethod
    # def _login(cls, db, credential, user_agent_env):
    #     """ وقتی کاربر لاگین کرد، حضورش در hr.attendance ثبت شود، اگر قبلاً چک‌این نکرده باشد. """
    #     auth_info = super(ResUsers, cls)._login(db, credential, user_agent_env)

    #     with cls.pool.cursor() as cr:
    #         env = api.Environment(cr, auth_info['uid'], {})
    #         user = env['res.users'].browse(auth_info['uid'])

    #         # بررسی اینکه آیا این کاربر یک کارمند است
    #         employee = env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
    #         if employee:
    #             # بررسی آخرین رکورد حضور این کارمند
    #             last_attendance = env['hr.attendance'].search(
    #                 [('employee_id', '=', employee.id)],
    #                 order='check_in desc', limit=1
    #             )

    #             # شرط: اگر آخرین رکورد چک‌اوت نداشته باشد، چک‌این نزنیم
    #             if not last_attendance or last_attendance.check_out:
    #                 env['hr.attendance'].create({
    #                     'employee_id': employee.id,
    #                     'check_in': fields.Datetime.now(),
    #                 })
    #                 _logger.info(f"✅✅✅ حضور کاربر {user.name} در حضور و غیاب ثبت شد.")
    #             else:
    #                 _logger.info(f"⏳⏳⏳ کاربر {user.name} قبلاً حضور زده، چک‌این جدید ثبت نشد.")

    #     return auth_info
