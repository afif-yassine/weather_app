from typing import Dict, Any
import urllib.request, urllib.parse, json
from fastapi import FastAPI, HTTPException

app = FastAPI()

BASE_URL = "http://api.weatherapi.com/v1/history.json"  # changed to history endpoint

def fetch_forecast_by_date(city: str, date: str, api_key: str = "07d788f681c0410aa5c132944252110") -> Dict[str, Any]:
    """
    Fetch weather data for a given city and date (format: YYYY-MM-DD)
    """
    params = {"q": city, "dt": date, "key": api_key}
    url = BASE_URL + "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                raise RuntimeError(f"HTTP {resp.status} when fetching {url}")
            data = json.loads(resp.read())

            # Return simplified structure
            return {
                "location": {
                    "name": data["location"]["name"],
                    "region": data["location"]["region"],
                    "country": data["location"]["country"],
                    "localtime": data["location"]["localtime"]
                },
                "forecast": [
                    {
                        "date": day["date"],
                        "maxtemp_c": day["day"]["maxtemp_c"],
                        "mintemp_c": day["day"]["mintemp_c"],
                        "avgtemp_c": day["day"]["avgtemp_c"],
                        "condition": day["day"]["condition"]["text"],
                        "chance_of_rain": day["day"].get("daily_chance_of_rain")
                    }
                    for day in data["forecast"]["forecastday"]
                ]
            }
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTPError: {e.code} - {e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"URLError: {e.reason}") from e