# lev-etl



# Ferramenta ETL para processo seletivo LEV Negócios.

Este projeto implementa uma ferramenta ETL (Extrair, Transformar, Carregar).

## Funcionalidades

* **Extração:** Lê dados de arquivos de planilha (formato `.xlsx`).
* **Transformação:**
    * Remove acentos e caracteres especiais do nome.
    * Valida e formata o CPF.
    * Mantém apenas números no registro.
    * Converte o campo "OPTANTE" para 0 ou 1.
* **Carregamento:**
    * Carrega os dados brutos (sem tratamento) em uma coleção do MongoDB.
    * Carrega os dados transformados em uma tabela do MySQL.
* **Performance:** Utiliza filas (`queue`) e threads para processamento paralelo, melhorando a performance.

## Pré-requisitos

* Python 3 instalado.
* Pip instalado.
* MongoDB instalado e em execução.
* MySQL instalado e em execução.
* Arquivo `.env` configurado com as informações de conexão dos bancos de dados.

## Configuração

1.  Clone este repositório:
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd etl-desafio-fullstack
    ```
2.  Crie um ambiente virtual:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .venv\Scripts\activate  # Windows
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Crie um arquivo `.env` na raiz do projeto e configure as variáveis de ambiente com as informações de conexão do MongoDB e MySQL.
5.  Crie o banco de dados `etl_processed_data` e a tabela `usuarios` no MySQL (o script SQL está na seção de implementação).
6.  Coloque arquivos de planilha de teste (formato `.xlsx`) na pasta `data/`.

## Execução

Para executar a ferramenta ETL, navegue até a raiz do projeto e execute o seguinte comando:

```bash
python src/etl_pipeline.py