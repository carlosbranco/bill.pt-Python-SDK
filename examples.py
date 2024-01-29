from api import Api
# Examples

# Development
api_client = Api(mode='dev')

# Production
# api_client = Api(mode='app')

# Set the token
api_client.set_token('KHo3hrxmtxyTkmX4XVIgaX4SwLRaWRJ8QZUBnOC4Wqth5Rgs5sXnGmxWENIybee7CVL9OZ4yYAbjBeMzaAWHRuCsDVPrPZKUhhvVNUGtzFkrRLpBiY5hfmz0lpFGfZYB')

# Check the token
response = api_client.valid_token()
print(response)

# Get all document types
response = api_client.get_document_all_types()
print(response)

# Read measurement units
response = api_client.get_measurement_units()
print(response)

# Read payment methods
response = api_client.get_payment_methods()
print(response)

# Create a measurement unit
response = api_client.create_measurement_unit({'nome': 'Kelvin', 'simbolo': 'K'})
print(response)

# Read document sets
response = api_client.get_document_sets()
print(response)

# Read taxes
response = api_client.get_taxes()
print(response)

# Read tax exemptions
response = api_client.get_tax_exemptions()
print(response)

# Create a contact
response = api_client.create_contact({
    'nome': 'John Doe',
    'nif': '12345789',
    'country': 'PT'
})
print(response)

# Create an item
response = api_client.create_item({
    'descricao': 'Porta de Madeira',
    'codigo': 'AAA1234',
    'unidade_medida_id': 2938,  # Measurement unit ID
    'imposto_id': 399,  # VAT ID
    'iva_compra': 399,  # VAT ID
})
print(response)

# Create a final consumer document
response = api_client.create_document({
    'tipificacao': 'FT',
    'produtos': [
        {
            'item_id': 13017,
            'nome': 'Porta de Madeira',
            'quantidade': 1,
            'imposto': 23,
            'preco_unitario': 12
        }
    ],
    'terminado': 1  # 0 <- draft
})
print(response)

# Create an invoice for a new contact
contact = {
    'nome': 'Raul Borges',
    'pais': 'PT',
    'nif': '123456789'
}

response = api_client.create_document({
    'contato': contact,
    'tipificacao': 'FT',
    'produtos': [
        {
            'item_id': 13017,
            'nome': 'Porta de Madeira',
            'quantidade': 1,
            'imposto': 23,
            'preco_unitario': 12
        }
    ],
    'terminado': 1  # 0 <- draft
})
print(response)

# Create a quote for an old contact
response = api_client.create_document({
    'contato_id': 12983,  # Contact ID
    'tipificacao': 'ORC',
    'produtos': [
        {
            'item_id': 13017,
            'nome': 'Porta de Madeira',
            'quantidade': 1,
            'imposto': 23,
            'preco_unitario': 12
        }
    ],
    'terminado': 1  # 0 <- draft
})
print(response)

# Create a document with non-existent products
response = api_client.create_document({
    'contato_id': 12983,  # Contact ID
    'tipificacao': 'FR',
    'produtos': [
        {
            'codigo': 'AAA39922',  # new product
            'nome': 'Janela XPTO',
            'unidade_medida_id': 82,  # correct ID
            'ProductCategory': 'P',
            'movimenta_stock': 1,
            'quantidade': 1,
            'imposto': 23,
            'preco_unitario': 12
        }
    ],
    'terminado': 1  # 0 <- draft
})
print(response)

# Create a receipt for the invoice using the invoice ID
response = api_client.create_receipt_to_document_with_id(2939)
print(response)

# Create a manual receipt (partial or multiple documents)
response = api_client.create_receipt({
    'contato_id': 12983,  # Contact ID
    'tipo_documento_id': 28,  # receipt, 29 supplier receipt
    'documentos': [
        {
            'documento_id': 939,
            'total': 100,  # Float (total payment amount)
            'total_desconto': 0
        },
        {
            'documento_id': 944,
            'total': 89,
            'total_desconto': 10
        }
    ]
})
print(response)

# Void a document
response = api_client.void_document({
    'documento_id': 10039,
    'motivo_anular': 'Erro no preço.'
})
print(response)

# Create a partial credit note for an invoice
response = api_client.create_document({
    'contato_id': 12983,  # Contact ID
    'tipificacao': 'NC',
    'produtos': [
        {
            'codigo': 'AAA39922',  # new product
            'nome': 'Janela XPTO',
            'unidade_medida_id': 82,  # correct ID
            'ProductCategory': 'P',
            'movimenta_stock': 1,
            'quantidade': 1,  # quantity can never be greater than the original
            'imposto': 23,
            'preco_unitario': 12,  # price can never be greater than the original

            # Two options to reference the original document
            # Option 1 (choose one of the options)
            'referencia_manual': 'FR BILL/3',  # put the name of the original document
            # Option 2 (choose one of the options)
            'lancamento_pai_id': 399,  # put the ID of the parent transaction
            # To get the list and ID of transactions, use the getDocumentWithID route
        }
    ],
    'terminado': 1  # 0 <- draft
})
print(response)

# How to create a total credit note from an invoice
response = api_client.convert_document_with_id({
    'documento_id': 10309,  # change the ID
    'convert_to': 'NC'
})
print(response)
