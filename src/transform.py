# src/transform.py

import re
import unidecode
import threading

def validate_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return None

def transform_data(record):
    transformed_record = {}
    transformed_record['nome'] = unidecode.unidecode(record.get("NOME_USUARIO", "").strip().lower())
    cpf = validate_cpf(record.get("DOC_CPF", ""))
    transformed_record['cpf'] = cpf if cpf else ''
    transformed_record['registro'] = ''.join(filter(str.isdigit, str(record.get("NUMERO_REGISTRO ", ""))))
    optante_value = record.get("OPTANTE", "")
    transformed_record['optante'] = 1 if str(optante_value).strip().lower() in ['sim', 'true', 'yes', '1'] else 0
    return transformed_record

def start_transformation_workers(raw_data_queue, transformed_data_queue, num_workers=2):
    def worker():
        while True:
            record = raw_data_queue.get()
            if record is None:
                break
            print(f"Thread {threading.current_thread().name}: Recebeu registro para transformar: {record}")
            transformed_record = transform_data(record)
            transformed_data_queue.put(transformed_record)
            print(f"Thread {threading.current_thread().name}: Transformou e colocou na fila de load: {transformed_record}")
            raw_data_queue.task_done()

    threads = []
    for _ in range(num_workers):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    return threads

# if __name__ == "__main__":
#     # Exemplo de uso (para teste)
#     import queue
#     raw_queue = queue.Queue()
#     raw_queue.put({"NOME_USUARIO": "João da Silva Áçúcar", "DOC_CPF": "123.456.789-00", "NUMERO_REGISTRO": "ABC12345", "OPTANTE": "Sim"})
#     raw_queue.put({"NOME_USUARIO": "Maria Souza Café", "DOC_CPF": "98765432111", "NUMERO_REGISTRO": "67890", "OPTANTE": "Não"})
#
#     transformed_queue = queue.Queue()
#     threads = start_transformation_workers(raw_queue, transformed_queue)
#     raw_queue.join() # Espera todas as tarefas serem concluídas
#     for _ in threads:
#         transformed_queue.put(None) # Sinaliza o fim para os workers de load
#
#     while not transformed_queue.empty():
#         print(transformed_queue.get())