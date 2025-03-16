import pymongo
import dotenv
import os
import sqlite3
import psycopg2
#from database import operations

dotenv.load_dotenv()
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWD')
mongo_host = os.getenv('MONGO_HOST')

"""
this adapter should folow PEP 249 – Python Database API Specification v2.0
https://peps.python.org/pep-0249/
"""

class MongoDatabase:
    def __init__(self):
        client = pymongo.MongoClient(f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}") #server_api=ServerApi('1'))
        db = client["documents"]
        self.collection = db["nf"]

    def insert_dict(self, data:dict)-> int:

        # insert the dictionary into the collection
        result = self.collection.insert_one(data)

        
        # print the ID of the inserted document
        return result.inserted_id
    

class PostgresDatabase:
    def __init__(self):
        self.db = self.get_connection_string()

    def get_connection_string(self):
        #conn_string = f"postgres://{os.environ.get('SQL_DATABASE')}:{os.environ.get('SQL_PASSWORD')}@{os.environ.get('SQL_HOST')}/{os.environ.get('SQL_USER')}"
        conn_string = f"postgresql://{os.environ.get('SQL_USER')}:{os.environ.get('SQL_PASSWORD')}@{os.environ.get('SQL_HOST')}/{os.environ.get('SQL_DATABASE')}"
                        #postgres://localhost:5432/meu_banco
                        #postgresql://user:password@localhost/mydatabase


        return conn_string
    
    # def exists_key(self, key):
    #     with psycopg2.connect(self.db) as conn:
    #         return operations.exists_key(key, conn)

    # def insert_header(self, data):
    #     with psycopg2.connect(self.db) as conn:
    #         return operations.insert_header(data, conn)

    # def insert_item(self, header_id, data_list):
    #     with psycopg2.connect(self.db) as conn:
    #         return operations.insert_item(header_id, data_list, conn)

    # def is_product_on_db(self, gtin):
    #     with psycopg2.connect(self.db) as conn:
    #         return operations.is_product_on_db(gtin, conn)
        
    # def insert_product_json(self, data):
    #     with psycopg2.connect(self.db) as conn:
    #         return operations.insert_product_json(data, conn)
        
    # def insert_products(self, data, product_api):
    #     with psycopg2.connect(self.db) as conn:
    #         return operations.insert_products(data, product_api, conn)