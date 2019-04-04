import time

def cache(aNumber):
    theCache = {}

    def theDecorator(aFunction):
        def wrapper(*args, **kwargs):
            if not (args[0] in theCache) or time.time() - theCache[args[0]]["time"] >= aNumber:
                theCache[args[0]] = {
                    "time": time.time(), "value": aFunction(*args, **kwargs)}
            return theCache[args[0]]["value"]
        return wrapper
    return theDecorator

@cache(100000)
def fibonacci(anInput):
    assert isinstance(anInput, int)
    if anInput == 0:
        return 0
    if anInput == 1:
        return 1
    return fibonacci(anInput-1) + fibonacci(anInput-2)

def fibonacciSansCache(anInput):
    assert isinstance(anInput, int)
    if anInput == 0:
        return 0
    if anInput == 1:
        return 1
    return fibonacciSansCache(anInput-1) + fibonacciSansCache(anInput-2)