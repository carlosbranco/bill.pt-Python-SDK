import requests
import json
from datetime import datetime

class Api:
    def __init__(self, mode="standard", version='1.0'):
        self.mode = mode
        self.version = version
        self.prefix = 'api/' + version + '/'
        self.api_token = ""
        self.http_code = None
        self.log = False
        self.log_file = 'errorlog.html'
        self.memory_log = []
        self.log_type = 'file'
        self.valid_currency = {
            "EUR_€": "Euro (€)", "USD_$": "U.S. dollar ($)", "GBP_£": "Pound sterling (£)",  # Add all currencies here
        }
        self.countries = {
            'AF': 'Afghanistan', 'AX': 'Aland Islands',  # Add all countries here
        }

    def is_valid_currency(self, currency):
        return currency in self.valid_currency

    def get_currency_list(self):
        return self.valid_currency

    def get_countries_list(self):
        return self.countries

    def get_log_from_memory(self):
        return self.memory_log

    def is_valid_date_time(self, date_str, format="%Y-%m-%d %H:%M:%S"):
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False

    def is_valid_zip_code(self, zip_code):
        return bool(re.match(r"[0-9]{4}-[0-9]{3}", zip_code))

    def valid_token(self):
        if len(self.api_token) < 120:
            return False
        self.post_check_token()
        return self.success()

    def post_check_token(self):
        return self.request('POST', 'valid-token', {})

    def get_mode_url(self, url):
        domain = "https://app.bill.pt/"
        if self.mode == "dev":
            domain = "https://dev.bill.pt/"
        elif self.mode == "world":
            domain = "https://int.bill.pt/"
        return domain + self.prefix + url

    def request(self, method, url, params=None):
        url = self.get_mode_url(url)
        params = params or {}
        params.update({'api_token': self.api_token, 'method': method})
        headers = {"Content-type": "application/json"}
        response = requests.request(method, url, json=params, headers=headers)
        self.http_code = response.status_code
        if self.log:
            # Log the time
            pass
        return response.json() if self.is_json(response.text) else response.text

    def success(self):
        return 199 < self.http_code < 300

    def get_http_code(self):
        return self.http_code

    def set_log(self, log, log_type="file"):
        self.log = log
        self.log_type = log_type

    def set_token(self, api_token):
        self.api_token = api_token

    def get_token(self, params):
        return self.request('POST', 'auth/login', params)

    def get_document_all_types(self):
        return self.request('GET', 'tipos-documento')

    def get_document_types_of(self, category):
        return self.request('GET', f'tipos-documento/{category}')

    def get_payment_methods(self):
        return self.request('GET', 'metodos-pagamento')

    def get_delivery_methods(self):
        return self.request('GET', 'metodos-expedicao')

    def create_delivery_method(self, params):
        return self.request('POST', 'metodos-expedicao', params)

    def update_delivery_method(self, id, params):
        return self.request('PATCH', f'metodos-expedicao/{id}', params)

    def delete_delivery_method(self, id):
        return self.request('DELETE', f'metodos-expedicao/{id}')

    def get_measurement_units(self):
        return self.request('GET', 'unidades-medida')

    def create_measurement_unit(self, params):
        return self.request('POST', 'unidades-medida', params)

    def update_measurement_unit(self, id, params):
        return self.request('PATCH', f'unidades-medida/{id}', params)

    def delete_measurement_unit(self, id):
        return self.request('DELETE', f'unidades-medida/{id}')

    def get_vehicles(self):
        return self.request('GET', 'viaturas')

    def create_vehicle(self, params):
        return self.request('POST', 'viaturas', params)

    def update_vehicle(self, id, params):
        return self.request('PATCH', f'viaturas/{id}', params)

    def delete_vehicle(self, id):
        return self.request('DELETE', f'viaturas/{id}')

    def get_document_sets(self):
        return self.request('GET', 'series')

    def create_document_set(self, params):
        return self.request('POST', 'series', params)

    def update_document_set(self, id, params):
        return self.request('PATCH', f'series/{id}', params)

    def delete_document_set(self, id):
        return self.request('DELETE', f'series/{id}')

    def get_taxes(self):
        return self.request('GET', 'impostos')

    def create_tax(self, params):
        return self.request('POST', 'impostos', params)

    def update_tax(self, id, params):
        return self.request('PATCH', f'impostos/{id}', params)

    def delete_tax(self, id):
        return self.request('DELETE', f'impostos/{id}')

    def get_tax_exemptions(self):
        return self.request('GET', 'motivos-isencao')

    def get_warehouses(self):
        return self.request('GET', 'lojas')

    def create_warehouse(self, params):
        return self.request('POST', 'lojas', params)

    def update_warehouse(self, id, params):
        return self.request('PATCH', f'lojas/{id}', params)

    def delete_warehouse(self, id):
        return self.request('DELETE', f'lojas/{id}')

    def get_contacts(self, params=None):
        return self.request('GET', 'contatos', params)

    def get_contact_with_id(self, id, params=None):
        return self.request('GET', f'contatos/{id}', params)

    def create_contact(self, params):
        return self.request('POST', 'contatos', params)

    def update_contact(self, id, params):
        return self.request('PATCH', f'contatos/{id}', params)

    def delete_contact(self, id):
        return self.request('DELETE', f'contatos/{id}')

    def get_items(self, params=None):
        return self.request('GET', 'items', params)

    def get_item_with_id(self, id, params=None):
        return self.request('GET', f'items/{id}', params)

    def create_item(self, params):
        return self.request('POST', 'items', params)

    def update_item(self, id, params):
        return self.request('PATCH', f'items/{id}', params)

    def delete_item(self, id):
        return self.request('DELETE', f'items/{id}')

    def get_documents(self, params=None):
        return self.request('GET', 'documentos', params)

    def get_document_with_id(self, id, params=None):
        return self.request('GET', f'documentos/{id}', params)

    def create_document(self, params):
        return self.request('POST', 'documentos', params)

    def void_document(self, params):
        return self.request('PATCH', 'documentos', params)

    def delete_document(self, id):
        return self.request('DELETE', f'documentos/{id}')

    def create_document_opening_balance(self, params):
        return self.request('POST', 'documentos/saldo-inicial', params)

    def communicate_bill_of_landing(self, id):
        return self.request('POST', f'documentos/comunicar/guia/{id}')

    def add_transportation_code_manually(self, params):
        return self.request('POST', 'documentos/adicionar/codigo-at', params)

    def email_document(self, params):
        return self.request('POST', 'documentos/enviar-por-email', params)

    def add_private_note_to_document(self, params):
        return self.request('POST', 'documentos/nota-documento', params)

    def get_stock(self, params=None):
        return self.request('GET', 'stock', params)

    def get_stock_single_item(self, params=None):
        return self.request('GET', 'stock/singular', params)

    def get_stock_movements(self, params=None):
        return self.request('GET', 'stock/movimentos', params)

    def documents_with_pending_movements_from_contact(self, params=None):
        return self.request('GET', 'movimentos-pendentes', params)

    def pending_movements_of_multiple_documents(self, params=None):
        return self.request('GET', 'movimentos-pendentes/multiplos', params)

    def pending_movements_of_single_document(self, id):
        return self.request('GET', f'movimentos-pendentes/{id}')

    def convert_document_with_id(self, document_id, convert_to, date=None, date_shipping=None, date_delivery=None):
        original = self.get_document_with_id(document_id)
        document = {
            'tipificacao': convert_to,
            'contato_id': original['contato_id'],
            'loja_id': original['loja_id'],
            'serie_id': original['serie_id'],
            'metodo_pagamento_id': original['metodo_pagamento_id'],
            'metodo_expedicao_id': original['metodo_expedicao_id']
        }
        
        if date is not None:
            document['data'] = date
            
        if 'morada' in original and original['morada'] != "":
            document['morada'] = original['morada']
        
        if 'codigo_postal' in original and original['codigo_postal'] != "":
            document['codigo_postal'] = original['codigo_postal']

        if 'cidade' in original and original['cidade'] != "":
            document['cidade'] = original['cidade']

        if 'pais' in original and original['pais'] != "":
            document['pais'] = original['pais']

        if 'carga_morada' in original and original['carga_morada'] != "":
            document['carga_morada'] = original['carga_morada']

        if 'carga_codigo_postal' in original and original['carga_codigo_postal'] != "":
            document['carga_codigo_postal'] = original['carga_codigo_postal']

        if 'carga_cidade' in original and original['carga_cidade'] != "":
            document['carga_cidade'] = original['carga_cidade']

        if 'carga_pais' in original and original['carga_pais'] != "":
            document['carga_pais'] = original['carga_pais']

        if 'carga_pais' in original and original['carga_pais'] != "":
            document['carga_pais'] = original['carga_pais']

        if date_shipping is not None and original.get('data_carga', ''):
            document['data_carga'] = date_shipping

        if original.get('descarga_morada', ''):
            document['descarga_morada'] = original['descarga_morada']

        if original.get('descarga_codigo_postal', ''):
            document['descarga_codigo_postal'] = original['descarga_codigo_postal']

        if original.get('descarga_cidade', ''):
            document['descarga_cidade'] = original['descarga_cidade']

        if original.get('descarga_pais', ''):
            document['descarga_pais'] = original['descarga_pais']

        if date_delivery is not None and original.get('data_descarga', ''):
            document['data_descarga'] = date_delivery

        produtos = []
        for key, lancamento in enumerate(original['lancamentos']):
            lancamento_pai = lancamento['id']
            produto = dict(lancamento)
            produto['lancamento_pai_id'] = lancamento_pai
            produtos.append(produto)
        
        document['produtos'] = produtos
        document['terminado'] = 1
        
        return self.create_document(document)

    def create_receipt(self, params):
        return self.request('POST', 'recibos/', params)

    def create_receipt_to_document_with_id(self, id, params=[]):
        return self.request('POST', f'recibos/pagar/{id}', params)

    def set_tax_authority_login_information(self, params):
        return self.request('POST', 'at/configurar', params)

    def test_tax_authority_login(self):
        return self.request('POST', 'at/teste-dados-at')

    def tax_authority_login_state(self):
        return self.request('POST', 'at/estado-configuracao')

    def tax_authority_communication_log(self, params=[]):
        return self.request('POST', 'at/registo-comunicacoes', params)

    def get_contact_types(self, params=[]):
        return self.request('GET', 'tipos', params)

    def create_contact_type(self, params=[]):
        return self.request('POST', 'tipos', params)

    def update_contact_type(self, id, params=[]):
        return self.request('PATCH', f'tipos/{id}', params)

    def get_item_categories(self, params=[]):
        return self.request('GET', 'categorias', params)

    def create_item_category(self, params=[]):
        return self.request('POST', 'categorias', params)

    def update_item_category(self, id, params=[]):
        return self.request('PATCH', f'categorias/{id}', params)

    def get_document_states(self, params=[]):
        return self.request('GET', 'estados', params)

    def create_document_state(self, params=[]):
        return self.request('POST', 'estados', params)

    def update_document_state(self, id, params=[]):
        return self.request('PATCH', f'estados/{id}', params)

    def delete_document_state(self, id):
        return self.request('DELETE', f'estados/{id}')

    def change_document_state(self, params=[]):
        return self.request('POST', 'estados/mudar-estado', params)

    def get_smtp(self):
        return self.request('GET', 'smtp')

    def create_smtp(self, params=[]):
        return self.request('POST', 'smtp', params)

    def delete_smtp(self):
        return self.request('DELETE', 'smtp')

    def send_smtp_email_test(self, params=[]):
        return self.request('POST', 'smtp/email-teste', params)

    def get_email_templates(self, params=[]):
        return self.request('GET', 'email-template', params)

    def create_email_template(self, params=[]):
        return self.request('POST', 'email-template', params)

    def update_email_template(self, id, params=[]):
        return self.request('PATCH', f'email-template/{id}', params)

    def delete_email_template(self, id):
        return self.request('DELETE', f'email-template/{id}')
        
    def is_json(self, text):
        try:
            json.loads(text)
            return True
        except ValueError:
            return False