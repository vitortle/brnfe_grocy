import pymongo
import dotenv
import os
import sqlite3
import datetime


dotenv.load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWD')

def convert_date(date:str)-> str:
    """Converts date from dd/mm/yyyy to yyyy-mm-dd"""
    format_str = '%d/%m/%Y - %H:%M:%S' # The format
    return datetime.datetime.strptime(date, format_str).strftime('%Y-%m-%d %H:%M:%S')

class MongoDatabase():
    def __init__(self):
        client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@bestprice.uizfzp3.mongodb.net/?retryWrites=true&w=majority", 
                                    ) #server_api=ServerApi('1'))
        db = client["bestprice"]
        self.collection = db["bpcollection"]

    def insert_dict(self, data:dict)-> int:

        # insert the dictionary into the collection
        result = self.collection.insert_one(data)

        # print the ID of the inserted document
        return result.inserted_id
    

class SqliteDatabase():

    def insert_header(self, data:dict)-> int:
        with sqlite3.connect('/home/rogerio/sources/bestprice/bestprice/db.sqlite3') as conn:
            cursor = conn.cursor()
            query = "INSERT INTO cfe_header (cfeid, purchase_date, place_name, address, city) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query, (data['cfeid'], convert_date(data['purchase_date']), data['place_name'], data['address'], data['city']))
            conn.commit()
        return cursor.lastrowid


    def insert_item(self, purchase_id, data_list:dict)-> int:
        with sqlite3.connect('/home/rogerio/sources/bestprice/bestprice/db.sqlite3') as conn:
            cursor = conn.cursor()
            query = "INSERT INTO cfe_item (item, product_code, description, qtty, unit, unit_price, tax, total_price, purchase_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            for data in data_list:
                cursor.execute(query, 
                                    (
                                        data['item'], 
                                        data['product_code'], 
                                        data['description'], 
                                        data['qtty'].replace(',','.'), 
                                        data['unit'], 
                                        data['unit_price'].replace(',','.'), 
                                        data['tax'].replace(',','.').replace('(','').replace(')',''),
                                        data['total_price'].replace(',','.'), 
                                        purchase_id
                                    )
                                )
                conn.commit()
        return cursor.lastrowid
            