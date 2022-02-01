# -*- coding: cp1251 -*-

print("Введите сумму:", end=" ")
money = int(input())

atm = {1000: 5, 100: 3, 50: 1, 10: 2}

sum = 0
output = ""

for k in atm.keys():
    for i in range(1, atm[k] + 1):
        if sum == money:
            output += str(k) + "*" + str(i - 1)
            break
        elif i == atm[k]:
            output += str(k) + "*" + str(i)
        sum += k

    if sum == money:
        break
    output += " + "

if sum != money:
     print("Операция не может быть выполнена!")
     output = ""
else:
    print(output)
