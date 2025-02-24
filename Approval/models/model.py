# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    send_to_person = fields.Many2one(
        string='Send To',
        comodel_name='res.users',
    )

class ApprovalRequest(models.Model):
    _inherit = 'approval.request'
    
    @api.constrains('request_status')
    def _check_Send(self):
        for request in self:
            if request.request_status == 'approved':
                if request.category_id.send_to_person !=None:
                    existing_project = self.env['project.project'].search([('name', '=', request.name)], limit=1)

                    if not existing_project:
                        project = self.env['project.project'].create({
                            'name': request.category_id.name,
                            # 'privacy_visibility': 'employees',
                            # 'allow_timesheets': True,
                            # 'user_id': self.env.user.id,
                        })
                    else:
                        project = existing_project

                    task = self.env['project.task'].create({
                        'name': request.name,
                        'user_ids': [(4, request.category_id.send_to_person.id)],
                        'project_id': project.id, 
                        'date_deadline': request.date_confirmed,
                        'description': request.reason,
                    })

            else:
                pass
            