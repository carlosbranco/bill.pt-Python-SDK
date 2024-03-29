# SDK Bill.pt Python

## Descrição

Este SDK Python foi desenvolvido para auxiliar no desenvolvimento de integrações com a API do Bill.pt, um software de faturação certificado pela autoridade tributária em Portugal. A API permite a criação de vários tipos de documentos, incluindo faturas, recibos, notas de crédito, entre outros.

## Documentação da API

A documentação completa da API pode ser encontrada em [https://api.bill.pt](https://api.bill.pt).

## Site Oficial

Visite o [site oficial do Bill.pt](https://bill.pt) para obter mais informações sobre o software de faturação.

## Exemplos
Para instalar as dependencias faça npm install.

Para obter uma de desenvolvimento contacte o suporte do bill.pt.

Este repositório inclui uma série de exemplos que demonstram como usar o SDK para interagir com a API do Bill.pt. Os exemplos podem ser encontrados no diretório de exemplos.

```python
# Development
api_client = Api(mode='dev')

# Production
# api_client = Api(mode='app')

# Set the token
api_client.set_token('CHANGE_YOUR_TOKEN_HERE')

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
```

## Instalação de Dependências

Para executar este código, é necessário instalar algumas dependências Python. Você pode fazer isso facilmente usando o `pip`, o gerenciador de pacotes do Python.

1. **requests**: Este módulo é utilizado para fazer requisições HTTP em Python. Para instalá-lo, execute o seguinte comando no terminal:

   ```
   pip install requests
   ```

2. **json**: O módulo `json` já faz parte da biblioteca padrão do Python, então você não precisa instalá-lo separadamente.

3. **datetime**: Este é outro módulo da biblioteca padrão do Python, que é utilizado para trabalhar com objetos de data e hora. Você não precisa instalar nada adicional para usá-lo.

Depois de instalar o módulo `requests`, você poderá importá-lo e usá-lo em seus scripts Python. Os módulos `json` e `datetime` já estão disponíveis para uso sem a necessidade de instalação adicional.

---

