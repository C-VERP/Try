from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    bol_api_token = fields.Char(string="Bol.com API Token", config_parameter='bol.api_token')
