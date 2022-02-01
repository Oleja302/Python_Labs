import math
import random

n = random.randint(1, 10000)
list = [random.randint(1, 10000) for i in range(n)] + [0] * (2 ** math.ceil(math.log2(n)) - n)
print(list)