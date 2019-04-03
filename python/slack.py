import requests
import json


def writeToSlack(someText, url="https://hooks.slack.com/services/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"):
    # payload = "{\"text\":\"%s\"}" % (someText) PAS BON SI L'INPUT A DES GUILLEMETS !
    payloadDict = {}
    payloadDict["text"] = someText
    payload = json.dumps(payloadDict)

    headers = {}

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)


writeToSlack("salut")
writeToSlack("la")
writeToSlack('Salut "Monsieur" le président !')
