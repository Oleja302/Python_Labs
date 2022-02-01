import math

def frange(start, end, step):
    accuracy = 10 ** (abs(str(step).find('.') + 1 - len(str(step))))

    while start < end:
        if (int(start * accuracy) == int(start) * accuracy):
            yield int(start)
        else:
            yield int(start * accuracy) / accuracy
        start += step


for x in frange(1, 5, 0.1):
    print(x)
