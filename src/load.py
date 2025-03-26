from pymongo import MongoClient
import mysql.connector
from src.config import Config
import queue
import threading

def load_to_mongodb(data_queue):
    """Carrega dados brutos para o MongoDB."""
    try:
        client = MongoClient(Config.MONGODB_URI)
        db = client[Config.MONGODB_DATABASE]
        collection = db[Config.MONGODB_COLLECTION]
        while not data_queue.empty():
            record = data_queue.get()
            collection.insert_one(record)
            data_queue.task_done()
        print("Dados carregados para o MongoDB.")
    except Exception as e:
        print(f"Erro ao conectar ou inserir dados no MongoDB: {e}")
    finally:
        if 'client' in locals():
            client.close()

def load_to_mysql(data_queue):
    """Carrega dados transformados para o MySQL."""
    try:
        mydb = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO usuarios (nome, cpf, registro, optante) VALUES (%s, %s, %s, %s)"
        while True:
            record = data_queue.get()
            if record is None:
                break
            val = (record['nome'], record['cpf'], record['registro'], record['optante'])
            mycursor.execute(sql, val)
            data_queue.task_done()
        mydb.commit()
        print("Dados carregados para o MySQL.")
    except Exception as e:
        print(f"Erro ao conectar ou inserir dados no MySQL: {e}")
    finally:
        if 'mydb' in locals() and mydb.is_connected():
            mycursor.close()
            mydb.close()

def start_mongodb_load_worker(raw_data_queue):
    """Cria e inicia um thread para carregar dados no MongoDB."""
    thread = threading.Thread(target=load_to_mongodb, args=(raw_data_queue,))
    thread.start()
    return thread

def start_mysql_load_workers(transformed_data_queue, num_workers=2):
    """Cria e inicia threads para carregar dados no MySQL."""
    threads = []
    for _ in range(num_workers):
        thread = threading.Thread(target=load_to_mysql, args=(transformed_data_queue,))
        threads.append(thread)
        thread.start()
    return threads

if __name__ == "__main__":
    # Exemplo de uso (para teste)
    import queue
    raw_queue_test = queue.Queue()
    raw_queue_test.put({"NOME_USUARIO": "Teste", "DOC_CPF": "111.222.333-44", "NUMERO_REGISTRO": "123", "OPTANTE": "Sim"})
    start_mongodb_load_worker(raw_queue_test)

    transformed_queue_test = queue.Queue()
    transformed_queue_test.put({"nome": "teste", "cpf": "111.222.333-44", "registro": "123", "optante": 1})
    threads_mysql = start_mysql_load_workers(transformed_queue_test)
    for _ in threads_mysql:
        transformed_queue_test.put(None)
    for thread in threads_mysql:
        thread.join()