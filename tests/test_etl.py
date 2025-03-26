import unittest
import os
import pandas as pd
from pymongo import MongoClient
import mysql.connector
from src.config import Config
from src.extract import start_extraction_workers
from src.transform import transform_data
from src.load import load_to_mongodb, load_to_mysql
from src.etl_pipeline import main as run_etl
import queue

class TestETL(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Criar um arquivo de teste na pasta 'data'
        cls.test_file = 'data/test_data.xlsx'
        test_df = pd.DataFrame({
            "NOME_USUARIO": ["João da Silva Áçúcar", "Maria Souza Café"],
            "DOC_CPF": ["123.456.789-00", "98765432111"],
            "NUMERO_REGISTRO": ["ABC12345", "67890"],
            "OPTANTE": ["Sim", "Não"]
        })
        test_df.to_excel(cls.test_file, index=False)

        # Limpar coleções/tabelas de teste (se necessário)
        cls.mongo_client = MongoClient(Config.MONGODB_URI)
        cls.mongo_db = cls.mongo_client[Config.MONGODB_DATABASE]
        cls.mongo_collection = cls.mongo_db[Config.MONGODB_COLLECTION]
        cls.mongo_collection.delete_many({})

        cls.mysql_conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        cls.mysql_cursor = cls.mysql_conn.cursor()
        cls.mysql_cursor.execute("DELETE FROM usuarios")
        cls.mysql_conn.commit()

    @classmethod
    def tearDownClass(cls):
        # Remover o arquivo de teste
        os.remove(cls.test_file)
        # Fechar conexões
        cls.mongo_client.close()
        cls.mysql_cursor.close()
        cls.mysql_conn.close()

    def test_extraction(self):
        data_queue = start_extraction_workers([self.test_file])
        self.assertEqual(data_queue.qsize(), 2)
        record1 = data_queue.get()
        self.assertEqual(record1["NOME_USUARIO"], "João da Silva Áçúcar")

    def test_transformation(self):
        record = {"NOME_USUARIO": "João da Silva Áçúcar", "DOC_CPF": "123.456.789-00", "NUMERO_REGISTRO": "ABC12345", "OPTANTE": "Sim"}
        transformed = transform_data(record)
        self.assertEqual(transformed["nome"], "joao da silva acucar")
        self.assertEqual(transformed["cpf"], "123.456.789-00")
        self.assertEqual(transformed["registro"], "12345")
        self.assertEqual(transformed["optante"], 1)

    def test_etl_pipeline(self):
        run_etl()

        # Verificar dados no MongoDB
        mongo_data = list(self.mongo_collection.find())
        self.assertEqual(len(mongo_data), 2)
        self.assertEqual(mongo_data[0]["NOME_USUARIO"], "João da Silva Áçúcar")

        # Verificar dados no MySQL
        self.mysql_cursor.execute("SELECT * FROM usuarios")
        mysql_data = self.mysql_cursor.fetchall()
        self.assertEqual(len(mysql_data), 2)
        self.assertEqual(mysql_data[0][1], "joao da silva acucar")
        self.assertEqual(mysql_data[0][2], "123.456.789-00")

if __name__ == '__main__':
    unittest.main()