# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError,ValidationError
from . import company_message_recipient

class CompanyMessage(models.Model):
    _name = 'company.message'
    _description = 'Company Automation Messages'
    _rec_name =  'subject'
    
    _inherit = ['mail.thread', 'mail.activity.mixin']

    subject = fields.Char(string='Subject', required=True)

    body = fields.Html(string='Message text')

    attachment_ids = fields.Many2many('ir.attachment', string='Attachment files')
    
    def _default_sender(self):
        return self.env.user.employee_id if self.env.user.employee_id else False
    sender_id = fields.Many2one('hr.employee', string="Sender", default=_default_sender, readonly=True)

    target_department_id = fields.Many2one('hr.department', string='Target Department',
                        help="The department to which the message is intended to be sent.")

    recipient_line_ids = fields.One2many('company.message.recipient', 'message_id', string='Receivers')

    forward_user_id = fields.Many2one('res.users', string='Forward_person',default=None)

    parent_id = fields.Many2one('company.message', string='Reference message',
                        help='In case of reply or forwarding, the original message is kept in this field.')

    child_ids = fields.One2many('company.message', 'parent_id', string='Answers/References')

    count_child = fields.Integer(string='count_massage',compute='_countchild')

    message_type_val=[('new', 'New Message'),('reply', 'Reply'),('forward', 'Forward')]
    message_type = fields.Selection(selection=message_type_val, default='new', string="Message Type", readonly=True)

    date_sent = fields.Datetime(string="Send time", default=fields.Datetime.now, readonly=True)

    visible_recipient_line_ids = fields.One2many('company.message.recipient',string='Visible Recipients',
        compute='_compute_visible_recipient_line_ids')
    
    state_val=[('draft', 'Draft'),('sent', 'Sent'),('reply','Reply')]
    state = fields.Selection(selection=state_val, string='Status', default='draft', readonly=True)

    recipient_employe = fields.Char(string="Resiver", compute='_compute_recipient_names', store=True)

    is_read = fields.Boolean(string="Read", default=False)


# /////////////////////////////// my function ///////////////////////////////////

    def action_reply(self):
            return {
                'name': 'Reply to Message',
                'type': 'ir.actions.act_window',
                'res_model': 'company.message',
                'view_mode': 'form',
                'view_id': self.env.ref('my_office_automation.view_company_message_reply_form').id,
                'target': 'new',
                'context': {
                    'default_parent_id': self.id,
                    'default_subject': 'Re: ' + self.subject,
                    'default_message_type': 'reply',
                    'default_sender_id': self.env.user.employee_id.id,
                    'default_target_department_id': self.target_department_id.id,
                }
            }
        
    def action_send_reply(self):
        self.write({'state': 'reply'})


        if self.sender_id.id !=None:
                self.message_post(
                    body=self.body,
                    subject=self.subject,
                    partner_ids=[self.parent_id.sender_id.user_id.partner_id.id], 
                    message_type='notification',
                    subtype_xmlid='mail.mt_comment',
                )
                self.activity_schedule('my_office_automation.mail_activity_type_message',
                user_id=self.parent_id.sender_id.user_id.id,note=self.body)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Your reply has been sent successfully!'),
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'}
            }
        }

    def action_send(self):
        for record in self:
            if not record.recipient_line_ids:
                raise UserError(_("You must add at least one recipient before sending."))
            
            
            for recipient in record.recipient_line_ids.employee_id:

                record.message_post(
                    body=record.body,
                    subject=record.subject,
                    partner_ids=[recipient.user_id.partner_id.id], 
                    message_type='notification',
                    subtype_xmlid='mail.mt_comment',
                )
                record.activity_schedule(
                    'my_office_automation.mail_activity_type_message',
                    user_id=recipient.user_id.id,
                    note=record.body,
                )

            record.write({'state': 'sent', 'date_sent': fields.Datetime.now()})
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _('Message sent successfully!'),
                    'sticky': False,
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }
            
    def action_forward(self):
        return {
            'name': 'forward to Message',
            'type': 'ir.actions.act_window',
            'res_model': 'company.message',
            'view_mode': 'form',
            'view_id': self.env.ref('my_office_automation.view_company_message_forward_form').id,
            'target': 'new',
            'context': {
                'default_message_type': 'forward',
                'default_sender_id': self.env.user.employee_id.id,
                'default_subject': self.subject,

            }
        }

    def send_action_forward(self):
        for record in self:
            forward_message = self.create({
                'subject': record.subject,
                'body': record.body,
                'sender_id': self.env.user.employee_id.id,
                'message_type': 'forward',
                'date_sent': fields.Datetime.now(),
                'state': 'sent',
                'forward_user_id':self.forward_user_id.id,
            })
            
        if self.sender_id.id !=None:
                self.message_post(
                    body=self.body,
                    subject=self.subject,
                    partner_ids=[self.forward_user_id.partner_id.id], 
                    message_type='notification',
                    subtype_xmlid='mail.mt_comment',
                )
                self.activity_schedule(
                    'my_office_automation.mail_activity_type_message',
                    user_id=self.forward_user_id.id,
                    note=self.body,
                    
                )
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Your Forward Message has been sent successfully!'),
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'}
            }
        }

# /////////////////////////////// api model function ///////////////////////////////////


    @api.model
    def write(self, vals):
        for record in self:
            if record.state == 'sent':
                raise UserError(_("You cannot modify a sent message."))
        return super(CompanyMessage, self).write(vals) 

    @api.model    
    def unlink(self):
        for record in self:
            if record.state == 'sent':
                raise UserError(_("You cannot delete a sent message."))
        return super(CompanyMessage, self).unlink()


    @api.model
    def create(self, vals):
        if vals.get('parent_id'):
            vals['message_type'] = 'reply'
        return super(CompanyMessage, self).create(vals)


    @api.model
    def mark_as_read(self, record_id):
        record = self.sudo().browse(record_id)
        if record.exists() and not record.is_read:
            self.env.cr.execute("UPDATE company_message SET is_read = TRUE WHERE id = %s", (record.id,))
            self.env.cr.commit()
            return True 
        return False 


# /////////////////////////////// api depends function ///////////////////////////////////

    @api.depends('recipient_line_ids.employee_id.name')
    def _compute_recipient_names(self):
        for record in self:
            record.recipient_employe = ', '.join(record.recipient_line_ids.mapped('employee_id.name'))
            
             
    @api.depends('child_ids')
    def _countchild(self):
        for rec in self:
            count = len(rec.child_ids)
            rec.count_child = count
        

    
               
# /////////////////////////////// api onchange function ///////////////////////////////////

    @api.onchange('target_department_id')
    def _onchange_target_department(self):
        x=self.env['company.message'].search([])
        if not self.target_department_id:
            self.recipient_line_ids = [(5, 0, 0)]  
            return

# /////////////////////////////// api constrains function ///////////////////////////////////

    @api.constrains('target_department_id', 'recipient_line_ids')
    def _check_mandatory_cc(self):
        for record in self:
            if record.target_department_id and record.sender_id.department_id != record.target_department_id:
                dept_head = record.target_department_id.manager_id
                if dept_head:
                    found = False
                    for line in record.recipient_line_ids:
                        if line.employee_id.id == dept_head.id:
                            found = True
                            break
                    
                    if not found:
                        raise ValidationError(_(
                            "When sending to %(department)s department, a copy to the department head %(dept_head)s is required."
                        ) % {
                            'department': record.target_department_id.name,
                            'dept_head': dept_head.name
                        })

