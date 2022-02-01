# -*- coding: cp1251 -*-
print("Введите число:", end=" ")
money = float(input())

try:
    if money < 0:
        raise TypeError
    else:
        rub = int(money // 1)
        cop = int(money % 1 * 100)

        print(rub, "руб.", cop, "коп.")

except TypeError:
    print("Некорректный формат!")
