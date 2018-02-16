from flask import Flask
from flask import request
import sigfoxparser
import requests
import json

app = Flask(__name__)

#Schema definition and extraction
doorSchema = "on::bool canBeUnlocked::bool canBeUnlockedByBluetooth::bool numberOfUnlocksCurrentDay::uint:10"
temperatureSchema = "on::bool temperature::uint:10 pressure::uint:20"

database = {
    "abcdeeee": {"schema":doorSchema,"url":"http://custom-server/sigfoxEvent"},
    "eujuejjee": {"schema":doorSchema,"url":"http://custom-server/sigfoxEvent"},
    "plzllzzz": {"schema":temperatureSchema,"url":"http://custom-server/sigfoxEvent"},
    "12hhyhhee": {"schema":temperatureSchema,"url":"http://custom-server/sigfoxEvent"}
}

def getSchemaFromDeviceId(deviceId):
    return database[deviceId]["schema"]

def getUrlFromDeviceId(deviceId):
    return database[deviceId]["url"]

@app.route("/")
def hello():
    return "Hello World!"

def extractDeviceId(anInput):
    lines = anInput.split("\n")
    linesSplitted = [line.split(":") for line in lines]
    treated = {element[0]:element[1][1:] for element in linesSplitted}
    return treated["deviceId"]

@app.route('/newEvent', methods=['POST'])
def newEvent():
    receivedData = request.get_data().decode('utf-8')
    receivedData = receivedData.replace("\r\n","\n")
    print("Here is the received data",receivedData)
    print("\n")

    deviceId = extractDeviceId(receivedData)
    schema = getSchemaFromDeviceId(deviceId)
    url = getUrlFromDeviceId(deviceId)
    ## We should guess the good schema ! Here just a fake one !
    transformed = sigfoxparser.fromDeviceInputToDict(receivedData,schema)

    jsonTransformed = json.dumps(transformed)
    print(jsonTransformed)
    
    #Write to Slack
    writeOnSlack(jsonTransformed)

    #send to custom server
    sendToCustomServer(jsonTransformed,url)

    print("\n\n\n\n")
    return json.dumps(transformed)

def writeOnSlack(text):
    url = "https://hooks.slack.com/services/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"

    payload = json.dumps({
        "text": text
    })

    headers = {
        'Content-type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "7b7441a1-03e7-590b-9157-c1f53f420d64"
    }

    #response = requests.request("POST", url, data=payload, headers=headers)

def sendToCustomServer(text,url):
    response = requests.request("POST", url, data=text)