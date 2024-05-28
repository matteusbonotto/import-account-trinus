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
def generate_data(core_bank_id, bank_account):
    tax_id = remove_masks(fake.cpf())
    name = fake.name()
    email = name.replace(" ", ".").lower() + "@example.com"
    cellphone = remove_masks(fake.phone_number())
    # corebankid
    motherName = fake.name()
    bornAt = fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat()
    paymentAccountType = 1
    # paymentAccountCoreBankId
    bankBranchAccount = 1
    login = tax_id
    investmentProfile = 1

    return [
        generate_userId(tax_id), name, generate_userId(tax_id), name, tax_id, email, cellphone, 'c', motherName, bornAt,
        paymentAccountType, core_bank_id, bankBranchAccount, login, investmentProfile, email, cellphone, bank_account,
        motherName, bornAt, paymentAccountType, core_bank_id, bankBranchAccount, login, investmentProfile
    ]

# Cabeçalho do CSV
header = [
    "userId", "name", "userId", "name", "taxIdentifier", "email", "cellphone", "c", "motherName", "bornAt",
    "paymentAccountType", "paymentAccountCoreBankId", "bankBranchAccount", "login", "investmentProfile", "email",
    "cellphone", "bankAccount", "motherName", "bornAt", "paymentAccountType", "paymentAccountCoreBankId",
    "bankBranchAccount", "login", "investmentProfile"
]

# Definir o layout da interface
layout = [
    [sg.Text("Número da conta"), sg.Input(key='-CONTA-')],
    [sg.Text("Número da Bankcore"), sg.Input(key='-BANKCORE-')],
    [sg.Text("Número de linhas a gerar"), sg.Input(key='-NUM_LINHAS-', default_text='1')],
    [sg.Button('Gerar CSV'), sg.Button('Gerar JSON')]
]

# Criar a janela
window = sg.Window('Gerador de contas - Trinus', layout)

# Loop de eventos
while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Gerar CSV':
        nconta = values['-CONTA-']
        bcore = values['-BANKCORE-']
        num_linhas = int(values['-NUM_LINHAS-'])
        
        # Geração dos dados
        rows = [generate_data(bcore, nconta) for _ in range(num_linhas)]  # Ajuste o número de linhas conforme necessário
        
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
        
        # Geração dos dados
        rows = [generate_data(bcore, nconta) for _ in range(num_linhas)]  # Ajuste o número de linhas conforme necessário
        
        # Salvando no arquivo JSON
        with open('dados.json', 'w') as file:
            json.dump(rows, file, ensure_ascii=False, indent=4)
        
        sg.popup("JSON gerado com sucesso!")

# Fechar a janela
window.close()
