# -*- coding: utf-8 -*-

from odoo import api, fields, models
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from odoo.exceptions import UserError
from odoo.modules.module import get_module_path


class MyModel(models.Model):
    _name = "my.model"
    _description = "My model example"

    name = fields.Char('Name')
    amount = fields.Float('Amount')

    def draw_pie_chart(self, labels, quantity):
        colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'purple']
        plt.pie(quantity, colors=colors, autopct='%1.1f%%',
                shadow=False, startangle=90, labeldistance=1.1)
        plt.axis('equal')
        plt.legend(labels=labels)
        path = get_module_path('pie_chart_print')
        plt.savefig(path + '/static/src/img/pie.png', bbox_inches='tight')
        img = mpimg.imread(path + '/static/src/img/pie.png')
        plt.close()
        return img

    @api.multi
    def get_chart_print(self):
        for record in self:
            data = {}
            # Build your own data lists
            list_data = self.env['my.model'].search([])
            if list_data:
                pie_chart_labels = list_data.mapped(
                    lambda x: x.name)
                pie_chart_quantities = list_data.mapped(lambda x: x.amount)
                pie = self.draw_pie_chart(pie_chart_labels, pie_chart_quantities)
                # The rest of the data in your report
                # data.update()
                return self.env.ref('pie_chart_print.report_pie_chart_pdf').report_action(self, data=data)
            else:
                raise UserError('Insert a few records')

