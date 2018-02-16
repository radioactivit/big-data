import time
import paho.mqtt.client as paho
import requests

#define callback
def on_message(client, userdata, message):
    text = str(message.payload.decode("utf-8"))
    response = requests.request("POST", "http://elasticsearch:9200/iot/message", data=text)
    print("received message =",text,response.text)

client= paho.Client("client-001")

client.on_message=on_message

client.connect("mqtt-server")

client.loop_start()
client.subscribe("all/events")

time.sleep(100)