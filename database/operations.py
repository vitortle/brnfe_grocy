import logging
import json


logger = logging.getLogger(__name__)


def exists_key(key, conn) -> bool:
    rows = []
    cursor = conn.cursor()
    cursor.execute(f"SELECT count(*) FROM cfe_header where access_key='{key}'")
    rows = cursor.fetchall()
    print('***',key, rows[0][0] == 0)
    return False if rows[0][0] == 0 else True

def insert_header(data:dict, conn)-> int:
    cursor = conn.cursor()
    query = "INSERT INTO cfe_header (cfeid, access_key, purchase_date, place_name, address, city) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
    cursor.execute(query, (data['cfeid'], data['access_key'], data['purchase_date'], data['place_name'], data['address'], data['city']))
    inserted_id = cursor.fetchone()[0]
    conn.commit()
    return inserted_id

def insert_item(header_id, data_list:list, conn)-> int:
    # data = data_list[0]
    cursor = conn.cursor()
    query = """INSERT INTO cfe_item (item, description, qtty, unit, liquid_price,
    aditional_info, product_code, gtin_code,
    ncm_code,unit_price, gross_price, calc_rule, discount,
    icms_value, pis_value, pis_st_value, cofins_value, confins_st_value,
    issqn_value, total_tax_value, purchase_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """

    for data in data_list:
        cursor.execute(
            query, 
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
        inserted_id = cursor.fetchone()[0]
        conn.commit()
    return inserted_id

def is_product_on_db(gtin:str, conn) -> bool:
    cursor = conn.cursor()
    query = f"SELECT 1 FROM cfe_product WHERE gtin = '{gtin}'"
    cursor.execute(query)
    return cursor.fetchone()

def insert_product_json(gtin, product_data:dict, conn)-> int:
    """
    Insert one row of product data on the product table
    """
    cursor = conn.cursor()
    query = f"insert into public.cfe_product(data, gtin) values('{ json.dumps(product_data)}', '{gtin}'::jsonb) RETURNING id"
    cursor.execute(query)
    inserted_id = cursor.fetchone()[0]
    conn.commit()
    return inserted_id

def insert_product(item_data:dict, product_api, conn):
    """
        Checks the just inserted items for new products. 
        If there is a new product on items table, insert on products.
    """
    def is_gtin_valid(gtin):
        return gtin.isnumeric()
    
    for item in item_data:
        gtin = item['gtin_code']
        if is_gtin_valid(gtin) and not is_product_on_db(gtin, conn):
            logger.info(f'API call for get product for {gtin}...')
            product_data = product_api.get_data_for_gtin(gtin)
            # insert data related to product
            product_id = insert_product_json(gtin, product_data, conn)
            logger.info(f'Produto {product_id} inserido!')