from typing import Union

from fastapi import FastAPI, HTTPException

from services.weatherApi import fetch_forecast

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/forecast/{city}")
def get_forecast(city: str, days: int = 5):
    try:
        result = fetch_forecast(location=city, days=days)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

