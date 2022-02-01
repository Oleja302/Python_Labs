def extra_enumerate(x):
    sumAll = sum(x)
    sumCurrent = 0
    frac = 0

    for i in range(0, len(x)):
        sumCurrent += x[i]
        frac = sumCurrent / sumAll
        yield i, x[i], sumCurrent, frac


x = [1, 3, 4, 2]

for i, elem, sum, frac in extra_enumerate(x):
    print(elem, sum, frac)
