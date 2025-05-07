import requests
import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class BolQuestionFetcher(models.Model):
    _name = "bol.question.fetcher"
    _description = "Bol.com Partner Vragen Ophaler"

    @api.model
    def fetch_questions(self):
        bol_api_key = self.env['ir.config_parameter'].sudo().get_param('bol.api_token')
        if not bol_api_key:
            _logger.error("Geen Bol.com API-token gevonden in instellingen!")
            return

        headers = {
            "Accept": "application/vnd.retailer.v9+json",
            "Authorization": f"Bearer {bol_api_key}"
        }

        response = requests.get(
            "https://api.bol.com/retailer/questions",
            headers=headers
        )

        if response.status_code != 200:
            _logger.error(f"Fout bij ophalen vragen: {response.text}")
            return

        data = response.json()
        for question in data.get("questions", []):
            customer_email = question.get("customerEmail", "onbekend")
            subject = question.get("subject", "Geen onderwerp")
            message = question.get("question")

            existing = self.env['crm.lead'].search([('bol_question_id', '=', question['id'])])
            if existing:
                continue

            self.env['crm.lead'].create({
                'name': subject,
                'contact_name': customer_email,
                'description': message,
                'type': 'lead',
                'bol_question_id': question['id'],
            })
