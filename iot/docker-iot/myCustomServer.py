from flask import Flask
from flask import request
import paho.mqtt.client as mqtt

app = Flask(__name__)

@app.route('/sigfoxEvent', methods=['POST'])
def newEvent():
    receivedData = request.get_data().decode('utf-8')
    client = mqtt.Client("myClient")
    client.connect("mqtt-server")
    print("Publish",client.publish("all/events",receivedData))
    print(receivedData)
    return "hello"