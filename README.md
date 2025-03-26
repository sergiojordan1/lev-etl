# Pipeline ETL de Dados de Planilhas para MongoDB e MySQL

Este projeto implementa um pipeline de Extração, Transformação e Carga (ETL) para processar dados de planilhas Excel e carregá-los em bancos de dados MongoDB e MySQL.

## Descrição

O pipeline ETL realiza as seguintes etapas:

1.  **Extração:** Lê dados de arquivos Excel localizados na pasta `data`.
2.  **Transformação:** Processa os dados extraídos, realizando limpeza, formatação e conversão de tipos.
3.  **Carga:**
    * Carrega os dados brutos (diretamente das planilhas) no MongoDB.
    * Carrega os dados transformados no MySQL.

## Pré-requisitos

Antes de executar o projeto, você precisará ter as seguintes ferramentas e softwares instalados:

* **Python 3.x:** Certifique-se de ter o Python instalado em sua máquina.
* **pip:** O gerenciador de pacotes do Python.
* **virtualenv (opcional, mas recomendado):** Para criar um ambiente virtual isolado para o projeto. Você pode instalá-lo com `pip install virtualenv`.
* **MongoDB:** Um servidor MongoDB em execução.
* **MySQL:** Um servidor MySQL em execução.
* **Pacotes Python:** As seguintes bibliotecas Python são utilizadas no projeto e precisam ser instaladas:
    * `pandas`
    * `openpyxl`
    * `pymongo`
    * `mysql-connector-python`
    * `python-dotenv`
    * `unidecode`

## Instalação

1.  **Clone o repositório**

2.  **Crie um ambiente virtual:**
    ```bash
    python -m venv .venv
    # Ou
    virtualenv .venv
    ```

3.  **Ative o ambiente virtual:**
    * **No Windows (PowerShell):**
        ```powershell
        .venv\Scripts\Activate.ps1
        ```
    * **No Windows (CMD):**
        ```bash
        .venv\Scripts\activate
        ```
    * **No Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```

4.  **Instale as dependências:**
    Primeiro, você precisará criar um arquivo `requirements.txt` listando as dependências do projeto. Você pode fazer isso executando o seguinte comando no seu ambiente virtual (após ter instalado as bibliotecas):
    ```bash
    pip freeze > requirements.txt
    ```
    Em seguida, instale as dependências usando o `pip`:
    ```bash
    pip install -r requirements.txt
    ```

## Execução

1.  **Configure as variáveis de ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes variáveis com as suas configurações de banco de dados:
    ```dotenv
    MONGODB_HOST=mongodb://localhost:27017/
    MONGODB_DATABASE=etl_raw_data
    MONGODB_COLLECTION=usuarios_raw

    MYSQL_HOST=localhost
    MYSQL_USER=root
    MYSQL_PASSWORD=
    MYSQL_DATABASE=etl_processed_data
    ```
    **Observações:**
    * Certifique-se de substituir os valores pelos seus dados de conexão do MongoDB e MySQL.
    * Se você usa senha no MySQL, adicione-a em `MYSQL_PASSWORD=sua_senha`.

2.  **Coloque seus arquivos Excel na pasta `data`:**
    Certifique-se de que os arquivos Excel que você deseja processar (`teste1.xlsx`, `teste2.xlsx`) estejam localizados dentro da pasta chamada `data` na raiz do projeto.

3.  **Execute o pipeline ETL:**
    Abra o seu terminal (certifique-se de que o ambiente virtual esteja ativado) e navegue até a raiz do diretório do projeto. Execute o seguinte comando:
    ```bash
    python -m src.etl_pipeline
    ```

    Você deverá ver mensagens no terminal indicando o progresso do processo ETL, incluindo a extração, transformação e carregamento dos dados.

## Estrutura do Projeto

```
lev-etl/
├── data/
│   ├── teste1.xlsx
│   └── teste2.xlsx
├── src/
│   ├── config.py
│   ├── extract.py
│   ├── load.py
│   ├── transform.py
│   └── etl_pipeline.py
├── .env
└── README.md
```


* `data/`: Contém os arquivos Excel de entrada.
* `src/`: Contém o código fonte do projeto:
    * `config.py`: Define as configurações do projeto (lendo do `.env`).
    * `extract.py`: Contém a lógica para extrair dados das planilhas Excel.
    * `load.py`: Contém a lógica para carregar dados no MongoDB e MySQL.
    * `transform.py`: Contém a lógica para transformar os dados extraídos.
    * `etl_pipeline.py`: O script principal que coordena o processo ETL.
* `.env`: Arquivo para configurar as variáveis de ambiente (conexão com os bancos de dados).
* `README.md`: Este arquivo, com as instruções de execução.

## Observações Finais

* Certifique-se de que os servidores MongoDB e MySQL estejam em execução antes de executar o pipeline.
* O script irá criar o banco de dados e a coleção/tabela se eles não existirem (dependendo da configuração do seu servidor e das permissões do usuário).
* Em caso de problemas, verifique as mensagens de erro no terminal e os logs dos seus servidores de banco de dados.

Este guia deve fornecer os passos necessários para executar o projeto ETL. Se você encontrar algum problema, consulte as mensagens de erro ou entre em contato.
