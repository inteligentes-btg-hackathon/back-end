from services import Template
from services.utils import Formatter
from database import db, QueryConstructor
from models import ProfitLoss
from services import Base64Manager
import os


class DarfRepository:
    def generate_darf(customer_id, date):
        query = QueryConstructor(ProfitLoss)
        query.select()
        query.where("customer_id", "=", customer_id)
        query.and_("to_char(generate_date, 'YYYY-MM')", "=", date)
        query.execute()

        if(len(query.results) == 0):
            return {
                "error": "No profit loss found for this customer"
            }

        darf_data = query.results[0]

        query_supply = QueryConstructor(ProfitLoss)
        query_supply.select()
        query_supply.where("customer_id", "=", customer_id)
        query_supply.execute()

        template = Template()
        template.update_value_id(
            'total_geral', Formatter.number(darf_data['taxes']))
        template.update_value_id('emitido_em', darf_data['generate_date'])
        template.update_value_id('CPF', Formatter.cpf(customer_id))
        template.update_value_id('codigo', '%03d' % len(query_supply.results))
        # check exist temp file
        if not os.path.exists('tmp'):
            os.makedirs('tmp')
        path = f'tmp/darf_{customer_id}.pdf'
        template.generate_pdf(path)

        return {
            "link": path
        }

    def check_payment(customer_id, date):
        query = QueryConstructor(ProfitLoss)
        query.select()
        query.where("customer_id", "=", customer_id)
        query.and_("to_char(generate_date, 'YYYY-MM')", "=", date)
        query.execute()

        if(len(query.results) == 0):
            return {
                "error": "No profit loss found for this customer"
            }
        query = QueryConstructor(ProfitLoss)

        query.update({
            "paid": 'true'
        })

        return {
            "status": 'success'
        }
