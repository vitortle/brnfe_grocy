from api import product_api
from .database import db_adapters
import dotenv


dotenv.load_dotenv()

def insert_gtins():
    gtins = [
        "8076802085738",
        "8711000362556",
        "8711000431108"
    ]
    
    db = db_adapters.PostgresDatabase()
    db.insert_products(gtins, product_api)

insert_gtins()

