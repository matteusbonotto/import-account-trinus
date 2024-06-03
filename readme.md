# Gerador de Contas - Trinus

Este projeto é um gerador de contas que cria dados fictícios de usuários no formato CSV e JSON. Ele utiliza várias bibliotecas, como `Faker`, `PySimpleGUI` e `unidecode` para gerar dados realistas e apresentar uma interface gráfica para o usuário.

## Funcionalidades

-   Geração de dados no formato CSV e JSON.
-   Dados gerados incluem informações como nome, CPF/CNPJ, telefone, email, endereço, entre outros.
-   Interface gráfica para entrada de dados e configuração da geração.

## Requisitos

-   Python 3.x
-   Bibliotecas Python:
    -   `csv`
    -   `re`
    -   `json`
    -   `os`
    -   `faker`
    -   `unidecode`
    -   `PySimpleGUI`
    -   `datetime`
    -   `random`
    -   `string`

## Instalação

1.  Clone o repositório:
    
    bash
    
    Copiar código
    
    `git clone https://github.com/seu-usuario/gerador-de-contas-trinus.git` 
    
2.  Navegue até o diretório do projeto:
    
    bash
    
    Copiar código
    
    `cd gerador-de-contas-trinus` 
    
3.  Instale as dependências:
    
    bash
    
    Copiar código
    
    `pip install -r requirements.txt` 
    

## Uso

1.  Execute o script principal:
    
    bash
    
    Copiar código
    
    `python gerador_de_contas.py` 
    
2.  Na janela que se abre, selecione a aba desejada (CSV ou JSON).
3.  Preencha os campos necessários e clique em "Gerar".

### Parâmetros

-   **Número da conta**: Número da conta bancária.
-   **Número da Bankcore**: Número da Bankcore.
-   **Número de linhas a gerar**: Quantidade de registros que serão gerados.
-   **Tipo de documento**: Escolha entre CPF ou CNPJ.
-   **Usar CPF/CNPJ manualmente**: Marque esta opção se desejar inserir um CPF ou CNPJ manualmente.
-   **CPF/CNPJ (manual)**: Insira o CPF ou CNPJ manualmente, se a opção acima estiver marcada.

## Estrutura do Projeto

bash

Copiar código

`gerador-de-contas-trinus/
│
├── gerador_de_contas.py      # Script principal com o código de geração de dados
├── requirements.txt          # Lista de dependências do projeto
├── README.md                 # Documentação do projeto
└── arquivos gerados/         # Diretório onde os arquivos gerados serão salvos` 

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.