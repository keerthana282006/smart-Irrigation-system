import requests

def get_ttn_data():

    try:

        url = "https://api.thingspeak.com/channels/9/feeds/last.json"

        response = requests.get(url, timeout=10, verify=False)

        data = response.json()

        return {

            "soil_moisture": float(data.get("field1", 0)),
            "temperature": float(data.get("field2", 0)),
            "humidity": float(data.get("field3", 0))  # safe now

        }

    except Exception as e:

        print("TTN Error:", e)

        return {

            "soil_moisture": "--",
            "temperature": "--",
            "humidity": "--"

        }


def start_ttn():
    pass