# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, fields, models, _

class Employee(models.Model):
    _inherit = "hr.employee"

    opportunitiy_count = fields.Integer(compute='_compute_opportunitiy', string='Number of opportunitiy')
    opportunitiy_stages = fields.Char(compute='_compute_opportunitiy', string='Status')

    def _compute_opportunitiy(self):
        for employee in self:
            user = employee.user_id
            if user:
                opportunities = self.env['crm.lead'].sudo().search([('user_id','=',user.id)])
                employee.opportunitiy_count = str(len(opportunities))
                tt_opportunitiy = {}
                count = 0
                opportunitiy_stage_text = ''
                for opportunitiy in opportunities:
                    if opportunitiy.stage_id not in tt_opportunitiy:
                        tt_opportunitiy.update({opportunitiy.stage_id.name:0})
                    state_opportunitiy = self.env['crm.lead'].sudo().search([('user_id','=',user.id),('stage_id','=',opportunitiy.stage_id.id)])
                    tt_opportunitiy[opportunitiy.stage_id.name] = len(state_opportunitiy)
                for item in tt_opportunitiy:
                    if tt_opportunitiy[item] != 0:
                        if opportunitiy_stage_text:
                            opportunitiy_stage_text = opportunitiy_stage_text + ' | ' + item + ': ' + str(tt_opportunitiy[item])
                        else:
                            opportunitiy_stage_text =  item + ': ' + str(tt_opportunitiy[item])
                employee.opportunitiy_stages = opportunitiy_stage_text
            else:
                employee.opportunitiy_stages = ''
                employee.opportunitiy_count = 0

    def display_employee_opportunitiy(self):
        """Display employee opportunitiy"""
        if self.user_id:
            context="{'group_by':'stage_id'}"
            template_id = self.env.ref('crm.crm_case_kanban_view_leads').id
            search_id = self.env.ref('crm.view_crm_case_opportunities_filter').id
            return {
                'name': _('Employee Pipeline'),
                'view_type': 'form',
                'view_mode': 'kanban,tree,graph,calendar,pivot,form',
                'res_model': 'crm.lead',
                'type': 'ir.actions.act_window',
                'view_id': template_id,
                'views': [(self.env.ref('crm.crm_case_kanban_view_leads').id, 'kanban'),
                          (self.env.ref('crm.crm_case_tree_view_oppor').id, 'tree'),
                          (self.env.ref('crm.crm_lead_view_graph').id, 'graph'),
                          (self.env.ref('crm.crm_case_calendar_view_leads').id, 'calendar'),
                          (self.env.ref('crm.crm_lead_view_pivot').id, 'pivot'),
                          (self.env.ref('crm.crm_lead_view_form').id, 'form')],
                'search_view_id': search_id,
                'domain': [('user_id','=',self.user_id.id)],
                'context': context
             }



