def irrigation_decision(soil, weather):

    try:

        if soil < 30:
            status = "Irrigation ON"

        elif soil < 50:
            status = "Moderate Irrigation"

        else:
            status = "No Irrigation"

        return {
            "status": status
        }

    except:

        return {
            "status": "Unknown"
        }