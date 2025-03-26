import pandas as pd
import queue
import threading
import os
from src.config import Config

def extract_from_excel(file_path, data_queue):
    """
    Extrai dados de um arquivo Excel e os coloca na fila.
    """
    try:
        df = pd.read_excel(file_path)
        records = df.to_dict('records')
        for record in records:
            data_queue.put(record)
        print(f"Dados extraídos de {file_path}")
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {file_path}")
    except Exception as e:
        print(f"Erro ao ler o arquivo {file_path}: {e}")

def start_extraction_workers(file_paths, num_workers=2):
    """
    Cria e inicia threads para extrair dados de múltiplos arquivos Excel.
    """
    data_queue = queue.Queue()
    threads = []
    for file_path in file_paths:
        thread = threading.Thread(target=extract_from_excel, args=(file_path, data_queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return data_queue

if __name__ == "__main__":
    # Exemplo de uso para teste
    data_dir = 'data'
    excel_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.xlsx')]

    if not excel_files:
        print("Nenhum arquivo Excel encontrado na pasta 'data'.")
    else:
        raw_data_queue = start_extraction_workers(excel_files)
        print(f"Total de registros extraídos: {raw_data_queue.qsize()}")