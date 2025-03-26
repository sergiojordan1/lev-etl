import re
import unidecode

def normalize_name(name):
    """Remove acentos e caracteres especiais do nome."""
    name_without_accents = unidecode.unidecode(name).lower()
    return re.sub(r'[^a-z\s]', '', name_without_accents).strip()

def validate_cpf(cpf):
    """Valida e formata o CPF."""
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return None
    # Adicione aqui a lógica de validação completa do CPF se necessário
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def normalize_registro(registro):
    """Mantém apenas os números do registro."""
    return ''.join(filter(str.isdigit, str(registro)))

def normalize_optante(optante):
    """Converte o valor de optante para 1 ou 0."""
    optante_str = str(optante).strip().lower()
    if optante_str in ['sim', 'true', '1', 'yes']:
        return 1
    elif optante_str in ['não', 'false', '0', 'no']:
        return 0
    return 0 # Valor padrão caso não corresponda

def transform_data(record):
    """Aplica as transformações a um registro."""
    transformed_record = {}
    transformed_record['nome'] = normalize_name(record.get("NOME_USUARIO", ""))
    transformed_record['cpf'] = validate_cpf(record.get("DOC_CPF", ""))
    transformed_record['registro'] = normalize_registro(record.get("NUMERO_REGISTRO", ""))
    transformed_record['optante'] = normalize_optante(record.get("OPTANTE", ""))
    return transformed_record

def start_transformation_workers(raw_data_queue, transformed_data_queue, num_workers=2):
    """
    Cria e inicia threads para transformar os dados.
    """
    def worker():
        while True:
            record = raw_data_queue.get()
            if record is None:
                break
            transformed_record = transform_data(record)
            transformed_data_queue.put(transformed_record)
            raw_data_queue.task_done()

    threads = []
    for _ in range(num_workers):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    return threads

if __name__ == "__main__":
    # Exemplo de uso (para teste)
    import queue
    raw_queue = queue.Queue()
    raw_queue.put({"NOME_USUARIO": "João da Silva Áçúcar", "DOC_CPF": "123.456.789-00", "NUMERO_REGISTRO": "ABC12345", "OPTANTE": "Sim"})
    raw_queue.put({"NOME_USUARIO": "Maria Souza Café", "DOC_CPF": "98765432111", "NUMERO_REGISTRO": "67890", "OPTANTE": "Não"})

    transformed_queue = queue.Queue()
    threads = start_transformation_workers(raw_queue, transformed_queue)
    raw_queue.join() # Espera todas as tarefas serem concluídas
    for _ in threads:
        transformed_queue.put(None) # Sinaliza o fim para os workers de load

    while not transformed_queue.empty():
        print(transformed_queue.get())