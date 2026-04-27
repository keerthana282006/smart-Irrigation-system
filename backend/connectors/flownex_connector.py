import pandas as pd

def get_flownex_data():

    try:

        url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-min-temperatures.csv"

        df = pd.read_csv(url)

        pressure = float(df.iloc[-1]["Temp"])

        flow_rate = pressure * 0.75

        return {

            "pressure": pressure,
            "flow_rate": flow_rate

        }

    except Exception as e:

        print("Flow Error:", e)

        return {

            "pressure": "--",
            "flow_rate": "--"

        }