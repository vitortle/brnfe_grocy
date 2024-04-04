import fastapi
from fastapi.responses import JSONResponse
import services


"""
API endpoints and return examples:
1- GET .../bestprice/<gtin_number>
    {
        "gtin": "7896065810592",
        "description": "AGUA MINERAL S GAS MINALBA 5L",
        "purchases": [
            {
                "place_name": "TENDA ATACADO SA",
                "unit_price": 5.00,
                "date": "2023-04-14 19:50:05+00"
            },
            {
                "place_name": "SUPER MERCADO SAO ROQUE LTDA",
                "unit_price": 4.50,
                "date": "2023-04-16 10:53:05+00"
            },
            {
                "place_name": "COOP COOPERATIVA DE CONSUMO"
                "unit_price": 5.50,
                "date": "2023-04-10 15:09:05+00"
            }
        ]
    }
"""

app = fastapi.FastAPI(debug=True)

@app.get('/get_last_price/{gtin}')
async def get_last_price(gtin:str):
    data = services.get_last_prices(gtin)
    return JSONResponse(content=data)
