from datetime import datetime

def from01ToUint(s):
   assert len(s) >=2
   return int(s, 2)
def from01ToInt(s):
   assert len(s) >= 2
   return (-1 if s[0] == "1" else 1) *from01ToUint(s[1:])
def from01ToBoolean(s):
   assert len(s) == 1
   return s == "1"

def fromBitsToDict(s,schema):
    variables = schema.split(" ")
    answer = {}
    theFunctions = {"bool": from01ToBoolean,"uint": from01ToUint,"int": from01ToInt}
    for variable in variables:
        variableName,variableTypeToSplit = variable.split("::")
        variableTypeSplitted = variableTypeToSplit.split(":")
        theSize = 1
        if len(variableTypeSplitted) >=2:
            theSize = int(variableTypeSplitted[1])
        answer[variableName] = theFunctions[variableTypeSplitted[0]](s[0:theSize])
        s = s[theSize:]
            
    return answer

def fromDeviceInputToDict(allData,schema):
    lines = allData.split("\n")
    linesSplitted = [line.split(":") for line in lines]
    #1: pour prendre tout sauf le premier caractère. On pourrait aussi utiliser .strip pour "trimmer" la chaîne, cad retirer les espaces avant et après
    treated = {element[0]:element[1][1:] for element in linesSplitted}
    treatedWithoutDataAndTimeStamp = {x:y for x,y in treated.items() if x not in ["data","timestamp"]}
    dataTimestampDict = {"datetimeUtc": str(datetime.utcfromtimestamp(int(treated["timestamp"]))),"data": fromBitsToDict(treated["data"],schema)}
    treatedWithoutDataAndTimeStamp.update(dataTimestampDict)
    return treatedWithoutDataAndTimeStamp