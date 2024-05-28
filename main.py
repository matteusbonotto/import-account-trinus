import csv
import re
import json
from faker import Faker
import PySimpleGUI as sg

# Inicialização do Faker
fake = Faker('pt_BR')  # Usar o local pt_BR para gerar CPFs no formato correto

# Função para remover máscaras de strings
def remove_masks(value):
    return re.sub(r'\D', '', value)

# Função para gerar o userId
def generate_userId(tax_id):
    return '190c6f655974441da71bef35c' + tax_id[-7:]

# Função para gerar os dados
def generate_data(core_bank_id, bank_account, use_cnpj):
    tax_id = remove_masks(fake.cnpj() if use_cnpj else fake.cpf())
    name = fake.name()
    email = name.replace(" ", ".").lower() + "@example.com"
    cellphone = remove_masks(fake.phone_number())
    motherName = fake.name()
    bornAt = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d')
    fantasyName = "Trinus Account"
    street = "Rua Arnaldo de Jesus"
    addressNumber = "10"
    complement = ""
    zipCode = "24460220"
    neighborhood = "MUTUA"
    city = "SAO GONCALO"
    state = "RJ"
    country = "Brasil"

    return [
        name,  # "name"
        tax_id,  # "taxIdentifier"
        generate_userId(tax_id),  # "externalID"
        cellphone,  # "cellphone"
        email,  # "email"
        bornAt,  # "bornAt"
        motherName,  # "motherName"
        fantasyName,  # "fantasyName"
        "0001",  # "bankBranchAccount"
        bank_account,  # "bankAccount"
        fantasyName,  # "alias"
        street,  # "street"
        addressNumber,  # "addressNumber"
        complement,  # "complement"
        zipCode,  # "zipCode"
        neighborhood,  # "neighborhood"
        city,  # "city"
        state,  # "state"
        country  # "country"
    ]

# Cabeçalho do CSV
header = [
    "name", "taxIdentifier", "externalID", "cellphone", "email", "bornAt", "motherName", "fantasyName",
    "bankBranchAccount", "bankAccount", "alias", "street", "addressNumber", "complement", "zipCode", "neighborhood",
    "city", "state", "country"
]

# Definir o layout da interface
layout = [
    [sg.Text("Número da conta"), sg.Input(key='-CONTA-')],
    [sg.Text("Número da Bankcore"), sg.Input(key='-BANKCORE-')],
    [sg.Text("Número de linhas a gerar"), sg.Input(key='-NUM_LINHAS-', default_text='1')],
    [sg.Radio('CPF', "RADIO1", key='-CPF-', enable_events=True), sg.Radio('CNPJ', "RADIO1", key='-CNPJ-', enable_events=True)],
    [sg.Button('Gerar CSV', disabled=True), sg.Button('Gerar JSON', disabled=True)]
]

# Criar a janela
window = sg.Window('Gerador de contas - Trinus', layout)

def update_buttons(window, values):
    if values['-CONTA-'] and values['-BANKCORE-'] and (values['-CPF-'] or values['-CNPJ-']):
        window['Gerar CSV'].update(disabled=False)
        window['Gerar JSON'].update(disabled=False)
    else:
        window['Gerar CSV'].update(disabled=True)
        window['Gerar JSON'].update(disabled=True)

# Loop de eventos
while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED:
        break
    
    update_buttons(window, values)
    
    if event == 'Gerar CSV':
        nconta = values['-CONTA-']
        bcore = values['-BANKCORE-']
        num_linhas = int(values['-NUM_LINHAS-'])
        use_cnpj = values['-CNPJ-']
        
        # Geração dos dados
        rows = [generate_data(bcore, nconta, use_cnpj) for _ in range(num_linhas)]
        
        # Salvando no arquivo CSV
        with open('dados.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for row in rows:
                writer.writerow(row)
        
        sg.popup("CSV gerado com sucesso!")
    
    if event == 'Gerar JSON':
        nconta = values['-CONTA-']
        bcore = values['-BANKCORE-']
        num_linhas = int(values['-NUM_LINHAS-'])
        use_cnpj = values['-CNPJ-']
        
        # Geração dos dados
        rows = [generate_data(bcore, nconta, use_cnpj) for _ in range(num_linhas)]
        
        # Salvando no arquivo JSON
        json_data = [dict(zip(header, row)) for row in rows]
        with open('dados.json', 'w') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
        
        sg.popup("JSON gerado com sucesso!")

# Fechar a janela
window.close()
