import requests

def get_weather():

    try:

        url = "https://api.open-meteo.com/v1/forecast?latitude=11.1271&longitude=78.6569&current_weather=true"

        response = requests.get(
            url,
            timeout=10,
            verify=False   # IMPORTANT FIX
        )

        data = response.json()

        current = data.get("current_weather")

        return {
            "temperature": current.get("temperature"),
            "wind": current.get("windspeed")
        }

    except Exception as e:

        print("Weather Error:", e)

        return {
            "temperature": "--",
            "wind": "--"
        }