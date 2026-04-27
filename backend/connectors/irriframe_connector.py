def get_irriframe_data(soil):

    try:

        if soil < 30:

            return {
                "water": 25,
                "duration": 20
            }

        elif soil < 50:

            return {
                "water": 15,
                "duration": 10
            }

        else:

            return {
                "water": 5,
                "duration": 5
            }

    except:

        return {
            "water": "--",
            "duration": "--"
        }