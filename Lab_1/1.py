# -*- coding: cp1251 -*-
print("������� �����:", end=" ")
money = float(input())

try:
    if money < 0:
        raise TypeError
    else:
        rub = int(money // 1)
        cop = int(money % 1 * 100)

        print(rub, "���.", cop, "���.")

except TypeError:
    print("������������ ������!")
