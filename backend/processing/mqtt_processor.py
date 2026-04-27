import paho.mqtt.client as mqtt

broker = "localhost"

client = mqtt.Client()

client.connect(broker)

def send_data(topic,data):

    client.publish(topic,str(data))