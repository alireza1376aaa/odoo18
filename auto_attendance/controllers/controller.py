from odoo import http
from odoo.http import request

class PresenceController(http.Controller):

    @http.route('/custom/logout', type='json', auth='user')
    def force_logout(self):
        user_id = request.env.user.id
        presence = request.env['bus.presence'].sudo().search([('user_id', '=', user_id)])
        if presence:
            presence.unlink()  # حذف کاربر از bus.presence
        return {'status': 'offline'}
