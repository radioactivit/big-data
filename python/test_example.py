import pytest
from tools import fibonacci
from vector import NumericVector
from vector import Vector
from vector import StringVector


def test_fibonacci():
    assert callable(fibonacci)
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(2) == 1
    assert fibonacci(3) == 2
    assert fibonacci(10) == 55
    assert fibonacci(17) == 1597
    with pytest.raises(AssertionError):
        assert fibonacci("hello")
        assert fibonacci(12.3)
        assert fibonacci(list)


def test_NumericVector_initialization():
    someIterables = [range(0, 23), list(range(0, 18)),
                     (i + 4 for i in range(90, 104))]
    for anIterable in someIterables:
        anIterable = range(0, 23)
        anIterableAsList = list(anIterable)
        n1 = NumericVector(anIterable)
        assert isinstance(n1, Vector)
        assert n1.values == list(anIterableAsList)
    with pytest.raises(AssertionError):
        NumericVector("bonjour")
        NumericVector(False)


def test_NumericVector_add():
    anIterable = range(0, 23)
    n1 = NumericVector(anIterable)
    for i in range(0, 20):
        n2 = n1 + i
        assert isinstance(n2, NumericVector)
        assert n2.values == [element+i for element in anIterable]

    # attemps to add a NumericVector with strange things
    with pytest.raises(AssertionError):
        n1 + "x"
        n1 + list


def test_StringVector():
    someValues = [str(i) for i in range(0, 23)]
    someValues.append("Test")
    someValues.append("OupS")
    n1 = StringVector(someValues[:])
    assert n1.values == someValues

    with pytest.raises(AssertionError):
        StringVector(range(0, 10))

    n1.toLowerCase()

    assert n1.values[23] == "test"
    assert n1.values[24] == "oups"

    # Support indexing ?
    assert n1[23] == "test"

    with pytest.raises(IndexError):
        n1[43]

    n1.toUpperCase()

    assert n1.values[23] == "TEST"

    n3 = n1.toLowerCaseNewInstance()

    # n1 stayed exactly the same
    assert n1[23] == "TEST"
    assert n3[23] == "test"
