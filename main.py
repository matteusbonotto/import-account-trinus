import csv
import re
import json
import os
from faker import Faker
import unidecode
import PySimpleGUI as sg
from datetime import datetime
import random
import string

# Inicialização do Faker
fake = Faker('pt_BR')  # Usar o local pt_BR para gerar CPFs no formato correto

# Função para remover máscaras de strings
def remove_masks(value):
    return re.sub(r'\D', '', value)

# Função para remover caracteres especiais de uma string
def remove_special_characters(value):
    return unidecode.unidecode(value)

# Função para gerar o userId
def generate_userId(tax_id):
    return '190c6f655974441da71bef35c' + tax_id[-7:]

# Função para gerar os dados para CSV
def generate_data_csv(core_bank_id, bank_account, use_cnpj, manual_tax_id=None):
    tax_id = manual_tax_id if manual_tax_id else remove_masks(fake.cnpj() if use_cnpj else fake.cpf())
    name = remove_special_characters(fake.name())
    username = bank_account  # username igual ao número da conta
    email = name.replace(" ", ".").lower() + "@example.com"
    cellphone = remove_masks(fake.phone_number())
    motherName = remove_special_characters(fake.name())
    bornAt = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d')
    fantasyName = remove_special_characters(fake.company())
    street = remove_special_characters(fake.street_name())
    addressNumber = fake.building_number()
    complement = ""
    zipCode = remove_masks(fake.postcode())
    neighborhood = remove_special_characters(fake.neighborhood())
    city = remove_special_characters(fake.city())
    state = fake.estado_sigla()
    country = "Brasil"

    return [
        name,  # "name"
        username,  # "username"
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

# Função para gerar os dados para JSON
def generate_data_json(use_cnpj, manual_tax_id=None):
    # Gerar bank account com 6 números aleatórios
    bank_account = ''.join(random.choices(string.digits, k=6))

    tax_id = manual_tax_id if manual_tax_id else remove_masks(fake.cnpj() if use_cnpj else fake.cpf())
    name = remove_special_characters(fake.name())
    username = bank_account
    email = name.replace(" ", ".").lower() + "@example.com"
    cellphone = remove_masks(fake.phone_number())
    motherName = remove_special_characters(fake.name())
    bornAt = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d')
    fantasyName = remove_special_characters(fake.company())
    street = remove_special_characters(fake.street_name())
    addressNumber = fake.building_number()
    complement = ""
    zipCode = remove_masks(fake.postcode())
    neighborhood = remove_special_characters(fake.neighborhood())
    city = remove_special_characters(fake.city())
    state = fake.estado_sigla()
    country = "Brasil"

    return {
        "name": name,
        "username": username,
        "taxIdentifier": tax_id,
        "externalID": generate_userId(tax_id),
        "cellphone": cellphone,
        "email": email,
        "bornAt": bornAt,
        "motherName": motherName,
        "fantasyName": fantasyName,
        "bankBranchAccount": "0001",
        "bankAccount": bank_account,
        "alias": fantasyName,
        "street": street,
        "addressNumber": addressNumber,
        "complement": complement,
        "zipCode": zipCode,
        "neighborhood": neighborhood,
        "city": city,
        "state": state,
        "country": country
    }

# Cabeçalho do CSV
header = [
    "name", "username", "taxIdentifier", "externalID", "cellphone", "email", "bornAt", "motherName", "fantasyName",
    "bankBranchAccount", "bankAccount", "alias", "street", "addressNumber", "complement", "zipCode", "neighborhood",
    "city", "state", "country"
]

# Layout para a aba CSV
csv_layout = [
    [sg.Text("Número da conta"), sg.Input(key='-CSV_CONTA-')],
    [sg.Text("Número da Bankcore"), sg.Input(key='-CSV_BANKCORE-')],
    [sg.Text("Número de linhas a gerar"), sg.Input(key='-CSV_NUM_LINHAS-', default_text='1')],
    [sg.Radio('CPF', "CSV_RADIO1", key='-CSV_CPF-', enable_events=True), sg.Radio('CNPJ', "CSV_RADIO1", key='-CSV_CNPJ-', enable_events=True)],
    [sg.Checkbox('Usar CPF/CNPJ manualmente', key='-CSV_MANUAL-', enable_events=True)],
    [sg.Text("CPF/CNPJ (manual)"), sg.Input(key='-CSV_TAX_ID-', visible=False)],
    [sg.Button('Gerar', key='-CSV_GERAR-', disabled=True)]
]

# Layout para a aba JSON
json_layout = [
    [sg.Text("Número de linhas a gerar"), sg.Input(key='-JSON_NUM_LINHAS-', default_text='1')],
    [sg.Radio('CPF', "JSON_RADIO1", key='-JSON_CPF-', enable_events=True), sg.Radio('CNPJ', "JSON_RADIO1", key='-JSON_CNPJ-', enable_events=True)],
    [sg.Checkbox('Usar CPF/CNPJ manualmente', key='-JSON_MANUAL-', enable_events=True)],
    [sg.Text("CPF/CNPJ (manual)"), sg.Input(key='-JSON_TAX_ID-', visible=False)],
    [sg.Button('Gerar', key='-JSON_GERAR-', disabled=True)]
]

# Definir o layout principal com abas
layout = [
    [sg.TabGroup([[
        sg.Tab('CSV', csv_layout),
        sg.Tab('JSON', json_layout)
    ]])]
]

# Criar a janela
window = sg.Window('Gerador de contas - Trinus', layout)

def update_buttons_csv(window, values):
    if values['-CSV_CONTA-'] and values['-CSV_BANKCORE-'] and (values['-CSV_CPF-'] or values['-CSV_CNPJ-']) and (not values['-CSV_MANUAL-'] or values['-CSV_TAX_ID-']):
        window['-CSV_GERAR-'].update(disabled=False)
    else:
        window['-CSV_GERAR-'].update(disabled=True)

def update_buttons_json(window, values):
    if values['-JSON_CPF-'] or values['-JSON_CNPJ-'] and (not values['-JSON_MANUAL-'] or values['-JSON_TAX_ID-']):
        window['-JSON_GERAR-'].update(disabled=False)
    else:
        window['-JSON_GERAR-'].update(disabled=True)

# Loop de eventos
while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED:
        break
    
    if event == '-CSV_MANUAL-':
        window['-CSV_TAX_ID-'].update(visible=values['-CSV_MANUAL-'])
        update_buttons_csv(window, values)
    
    if event == '-JSON_MANUAL-':
        window['-JSON_TAX_ID-'].update(visible=values['-JSON_MANUAL-'])
        update_buttons_json(window, values)
    
    if event == 'Gerar' or event == '-CSV_GERAR-':
        nconta = values['-CSV_CONTA-']
        bcore = values['-CSV_BANKCORE-']
        num_linhas = int(values['-CSV_NUM_LINHAS-'])
        use_cnpj = values['-CSV_CNPJ-']
        manual_tax_id = remove_masks(values['-CSV_TAX_ID-']) if values['-CSV_MANUAL-'] else None
        
        # Geração dos dados para CSV
        rows = [generate_data_csv(bcore, nconta, use_cnpj, manual_tax_id) for _ in range(num_linhas)]
        
        # Criar pasta se não existir
        output_dir = 'arquivos gerados'
        os.makedirs(output_dir, exist_ok=True)
        
        # Obter a data e hora atual
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Salvando no arquivo CSV
        csv_file = os.path.join(output_dir, f'dados_{current_time}.csv')
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for row in rows:
                writer.writerow(row)
        
        sg.popup("CSV gerado com sucesso!")
    
    if event == 'Gerar' or event == '-JSON_GERAR-':
        num_linhas = int(values['-JSON_NUM_LINHAS-'])
        use_cnpj = values['-JSON_CNPJ-']
        manual_tax_id = remove_masks(values['-JSON_TAX_ID-']) if values['-JSON_MANUAL-'] else None
        
        # Geração dos dados para JSON
        rows = [generate_data_json(use_cnpj, manual_tax_id) for _ in range(num_linhas)]
        
        # Criar pasta se não existir
        output_dir = 'arquivos gerados'
        os.makedirs(output_dir, exist_ok=True)
        
        # Obter a data e hora atual
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Salvando no arquivo JSON
        json_file = os.path.join(output_dir, f'dados_{current_time}.json')
        with open(json_file, 'w') as file:
            json.dump(rows, file, ensure_ascii=False, indent=4)
        
        sg.popup("JSON gerado com sucesso!")

    update_buttons_csv(window, values)
    update_buttons_json(window, values)

# Fechar a janela
window.close()

