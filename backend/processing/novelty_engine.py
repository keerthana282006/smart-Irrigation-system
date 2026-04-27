import random

def smart_novelty_system(soil, rainfall, temp):

    result = {}

    # Irrigation Decision
    if soil < 40 and rainfall < 5:
        result["decision"] = "Irrigation ON"
        water_used = 20
    else:
        result["decision"] = "Irrigation OFF"
        water_used = 5

    # Water Saving %
    saving = random.randint(15, 30)

    # Yield Prediction
    yield_value = random.randint(2200, 3000)

    # Water Use Efficiency
    wue = yield_value / (water_used + rainfall + 1)

    # Crop Health
    if soil > 50:
        health = "Healthy"
    else:
        health = "Need Attention"

    result["water_saved"] = str(saving) + "%"
    result["yield"] = yield_value
    result["wue"] = round(wue, 2)
    result["crop_health"] = health

    return result