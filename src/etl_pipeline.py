import os
from src.extract import start_extraction_workers
from src.transform import start_transformation_workers
from src.load import start_mongodb_load_worker, start_mysql_load_workers
import queue
import time

def main():
    data_dir = 'data'
    excel_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.xlsx')]

    if not excel_files:
        print("Nenhum arquivo Excel encontrado na pasta 'data'.")
        return

    print("Iniciando o processo ETL...")

    # Fase de Extração
    print("Extraindo dados das planilhas...")
    raw_data_queue = start_extraction_workers(excel_files, num_workers=2)
    print(f"Total de registros para carregar no MongoDB: {raw_data_queue.qsize()}")

    # Fase de Load para MongoDB (paralelo à transformação)
    print("Carregando dados brutos para o MongoDB...")
    mongodb_load_thread = start_mongodb_load_worker(raw_data_queue)

    # Fase de Transformação
    print("Transformando os dados...")
    transformed_data_queue = queue.Queue()
    transformation_threads = start_transformation_workers(raw_data_queue, transformed_data_queue, num_workers=4)

    # Espera a extração e a transformação terminarem
    raw_data_queue.join()
    for _ in transformation_threads:
        transformed_data_queue.put(None) # Sinaliza o fim para os workers de load do MySQL
    for thread in transformation_threads:
        thread.join()
    mongodb_load_thread.join() # Espera o load do MongoDB terminar

    print(f"Total de registros para carregar no MySQL: {transformed_data_queue.qsize()}")

    # Fase de Load para MySQL
    print("Carregando dados transformados para o MySQL...")
    mysql_load_threads = start_mysql_load_workers(transformed_data_queue, num_workers=2)
    for thread in mysql_load_threads:
        thread.join()

    print("Processo ETL concluído!")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Tempo total de execução: {end_time - start_time:.2f} segundos")