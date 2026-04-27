def calculate_wue(yield_value, irrigation_water, rainfall):

    try:

        total_water = irrigation_water + rainfall

        if total_water == 0:
            return 0

        wue = yield_value / total_water

        return round(wue, 3)

    except Exception as e:

        print("WUE Error:", e)

        return 0