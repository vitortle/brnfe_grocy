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

def save_data(cfe_header_data, cfe_item_data):
    sqlite = SqliteDatabase()
    
    idh = sqlite.insert_header(cfe_header_data)
    idi = sqlite.insert_item(idh, cfe_item_data)
    
    print(f'Record ID {idh}, {idi} saved!')

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
            query = "INSERT INTO cfe_header (cfeid, access_key, purchase_date, place_name, address, city) VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(query, (data['cfeid'], data['access_key'], data['purchase_date'], data['place_name'], data['address'], data['city']))
            conn.commit()
        return cursor.lastrowid


    def insert_item(self, header_id, data_list:list)-> int:
        data = data_list[0]
        print(data['item'],
                                        data['description'],
                                        data['qtty'],
                                        data['unit'],
                                        data['liquid_price'],
                                        data['aditional_info'],
                                        data['product_code'],
                                        data['gtin_code'],
                                        data['ncm_code'],
                                        data['unit_price'],
                                        data['gross_price'],
                                        data['calc_rule'],
                                        data['discount'],
                                        data['icms_value'],
                                        data['pis_value'],
                                        data['pis_st_value'],
                                        data['cofins_value'],
                                        data['confins_st_value'], 
                                        data['issqn_value'],
                                        data['total_tax_value'],
                                        header_id)

        with sqlite3.connect('/home/rogerio/sources/bestprice/bestprice/db.sqlite3') as conn:
            cursor = conn.cursor()
            query = "INSERT INTO cfe_item ('item', 'description', 'qtty', 'unit', 'liquid_price',"
            "'aditional_info', 'product_code', 'gtin_code',"
            "'ncm_code','unit_price', 'gross_price', 'calc_rule', 'discount',"
            "'icms_value', 'pis_value', 'pis_st_value', 'cofins_value', 'confins_st_value',"
            "'issqn_value', 'total_tax_value', 'purchase_id')"
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            for data in data_list:
                cursor.execute(query, 
                                    (
                                        data['item'],
                                        data['description'],
                                        data['qtty'],
                                        data['unit'],
                                        data['liquid_price'],
                                        data['aditional_info'],
                                        data['product_code'],
                                        data['gtin_code'],
                                        data['ncm_code'],
                                        data['unit_price'],
                                        data['gross_price'],
                                        data['calc_rule'],
                                        data['discount'],
                                        data['icms_value'],
                                        data['pis_value'],
                                        data['pis_st_value'],
                                        data['cofins_value'],
                                        data['confins_st_value'], 
                                        data['issqn_value'],
                                        data['total_tax_value'],
                                        header_id
                                    )
                                )
                conn.commit()
        return cursor.lastrowid
            