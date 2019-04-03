import time

N = 20000000
aRange = range(0, N)
aList = list(aRange)
aSet = set(aList)
aDict = {i: True for i in aRange}
listOfIterables = [aRange, aList, aSet, aDict]
print("Everything ready")
listOfAnswers = ["54" in iterable for iterable in listOfIterables]
print(listOfAnswers)


def timeToCheckIfInIterable(anIterable, aValue):
    start = time.time()
    aBoolean = aValue in anIterable
    end = time.time()
    diff = end - start
    return {"timeDifference": diff, "inIterable": aBoolean, "humanDuration": "{0:.2f}".format(round(diff, 2))}


listOfAnswersWithTime = [timeToCheckIfInIterable(iterable, 10000000)
                         for iterable in listOfIterables]
print(listOfAnswersWithTime)
