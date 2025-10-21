from typing import Dict, Any
import urllib.request, urllib.parse, json

BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

def fetch_forecast(location: str = "paris", days: int = 5, api_key: str = "07d788f681c0410aa5c132944252110") -> Dict[str, Any]:
    params = {"q": location, "days": str(days), "key": api_key}
    url = BASE_URL + "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                raise RuntimeError(f"HTTP {resp.status} when fetching {url}")
            data = json.loads(resp.read())
            
            # Return only necessary info
            return {
                "location": {
                    "name": data["location"]["name"],
                    "region": data["location"]["region"],
                    "country": data["location"]["country"],
                    "localtime": data["location"]["localtime"]
                },
                "current": {
                    "temp_c": data["current"]["temp_c"],
                    "condition": data["current"]["condition"]["text"],
                    "icon": data["current"]["condition"]["icon"],
                    "humidity": data["current"]["humidity"],
                    "wind_kph": data["current"]["wind_kph"]
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