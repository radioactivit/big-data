class Vector:
    def __init__(self, anIterable):
        self.values = list(anIterable)


def assertt(boolean, text=None):
    if text is None:
        assert boolean
        return 0
    assert boolean, text


def isFloatOrInteger(aValue):
    return isinstance(aValue, int) or isinstance(aValue, float)


class NumericVector(Vector):
    def __init__(self, anIterable):
        for element in anIterable:
            assert(isFloatOrInteger(element))
        super().__init__(anIterable)

    def __add__(self, aNumberOrNumericVector):
        if isFloatOrInteger(aNumberOrNumericVector):
            return NumericVector([value + aNumberOrNumericVector for value in self.values])
        if isinstance(aNumberOrNumericVector, NumericVector):
            assert len(aNumberOrNumericVector.values) == len(
                self.values), "Numeric vectors should have same size !!!"
            newValues = [value + aNumberOrNumericVector.values[index]
                         for index, value in enumerate(self.values)]
            return NumericVector(newValues)

    def __sub__(self, aNumberOrNumericVector):
        return self.__add__(-aNumberOrNumericVector)

    def __eq__(self, anotherNumericVector):
        assert isinstance(anotherNumericVector, NumericVector)
        assert len(anotherNumericVector) == len(self)
        return True

    def __len__(self):
        return len(self.values)


n1 = NumericVector(range(0, 10))
n2 = n1 + 4
print(n2.values)
n3 = n2 + n1
print(n3.values)

print((n1 + n2).values)

#n1 + NumericVector(range(0, 100))
n8 = n1
print(n1 == NumericVector(range(0, 10)))
print(n1 == n8)
