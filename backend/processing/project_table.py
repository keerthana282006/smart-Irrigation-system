import matplotlib.pyplot as plt
import os

def generate_project_table():

    # Create folder
    if not os.path.exists("static"):
        os.makedirs("static")

    fig, ax = plt.subplots(figsize=(8,10))
    ax.axis('off')

    # ---------------- TITLE 1 ----------------
    ax.text(0.5, 0.95, "TABLE I",
            ha='center', fontsize=16, fontweight='bold')

    ax.text(0.5, 0.91,
            "LIVE SENSOR VALUES OF SMART IRRIGATION SYSTEM",
            ha='center', fontsize=12)

    # Table 1 Data
    sensor_data = [
        ["Soil Moisture", "45 %"],
        ["Temperature", "31 °C"],
        ["Humidity", "72 %"],
        ["Rainfall", "5 mm"],
        ["Water Flow", "18 L/min"]
    ]

    table1 = ax.table(
        cellText=sensor_data,
        colLabels=["Sensor Name", "Current Value"],
        cellLoc='center',
        colLoc='center',
        bbox=[0.15, 0.58, 0.70, 0.25]
    )

    table1.auto_set_font_size(False)
    table1.set_fontsize(12)

    # ---------------- TITLE 2 ----------------
    ax.text(0.5, 0.48, "TABLE II",
            ha='center', fontsize=16, fontweight='bold')

    ax.text(0.5, 0.44,
            "IRRIGATION DECISION STATUS",
            ha='center', fontsize=12)

    # Table 2 Data
    status_data = [
        ["Motor Status", "ON"],
        ["Valve Status", "OPEN"],
        ["Water Needed", "YES"],
        ["Weather Condition", "Cloudy"],
        ["System Mode", "Automatic"]
    ]

    table2 = ax.table(
        cellText=status_data,
        colLabels=["Parameter", "Status"],
        cellLoc='center',
        colLoc='center',
        bbox=[0.15, 0.08, 0.70, 0.25]
    )

    table2.auto_set_font_size(False)
    table2.set_fontsize(12)

    plt.savefig("static/project_table.png", dpi=300, bbox_inches='tight')
    plt.close()

generate_project_table()
print("Table Generated Successfully")