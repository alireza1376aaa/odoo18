# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CompanyMessageRecipient(models.Model):
    _name = 'company.message.recipient'
    _description = 'Message recipients (original recipient and copy)'

    message_id = fields.Many2one('company.message', string='Message', required=True, ondelete='cascade')

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    
    is_editable = fields.Boolean(string="Is Editable", default=False)  

    recipient_type_val = [('receiver', 'Main recipient'),('cc', 'Copy')]
    recipient_type = fields.Selection(selection=recipient_type_val, string='Receiver type', default='receiver')

    delivery_mode_val= [('immediate', 'immediate'),('normal', 'normal')]
    delivery_mode = fields.Selection(selection=delivery_mode_val, string='Send mode', default='normal')

    show_in_copy = fields.Boolean(string='Show to recipient of copy',
                    help='In CC determines whether the person sees a copy of the message.',default=True)
    
    state_val=[('draft', 'Draft'),('sent','Sent'),('read', 'Read')]
    state = fields.Selection(selection=state_val, string='State', default='draft')