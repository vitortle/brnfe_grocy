
import logging
from psycopg2 import sql
import sys
import os
import psycopg2

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(os.path.join(BASE_PATH, 'database'))
print(sys.path)
import db_adapters

logger = logging.getLogger(__name__)
db = db_adapters.PostgresDatabase().db

def get_last_prices(search_term:str) -> dict:
    """
    {
        "produto": {
            "gtin":"7896066301778",
            "item":"PÃO DE FORMA INTEGRAL WICKBOLD VIVA INTEGRALMENTE PREMIUM PACOTE 450G",
            "imagem":"https://cdn-cosmos.bluesoft.com.br/products/7896066301778",
        },
        "compras": [{
            "local":"COOP COOPERATIVA DE CONSUMO",
            "preço_unid":10.79,
            "data_compra":"2023-10-14T09:59:40+00:00"
        },]
    }

    """
    with psycopg2.connect(db) as conn:
        cursor = conn.cursor()
    query = """
        select place_name, gtin_code, description, thumbnail, unit_price, purchase_date
        from public.last_price
        where gtin_code = %s;
    """
    safe_query = sql.SQL(query)
    try:
        cursor.execute(safe_query, (search_term,))
    except Exception as ex:
        logger.error(ex)
        return ''
    responses = cursor.fetchall()

    compras = []
    gtin = responses[0][1]
    item = responses[0][2]
    imagem = responses[0][3]
    produto = dict(gtin=gtin, item=item, imagem=imagem)

    for response in responses:
        local = response[0]
        preço_unid = float(response[4])
        data_compra = response[5].isoformat()
        compras.append(dict(local=local, preço_unid=preço_unid, data_compra=data_compra))

    return dict(produto=produto, compras=compras)


