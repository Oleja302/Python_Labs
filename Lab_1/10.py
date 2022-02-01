# -*- coding: cp1251 -*-

print("Введите пароль:", end=" ")
password = input()

flagNum = False
flagAlf = False
flagPunc = False
flagLen = False
countFlag = 0

if (len(password) >= 6):
    flagLen = True
    countFlag += 1

for i in range(len(password)):
    if password[i].isnumeric() and not flagNum:
        flagNum = True
        countFlag += 1
    elif password[i].isalpha() and not flagAlf:
        flagAlf = True
        countFlag += 1
    elif password[i] in ".?/!-_+#@^%*$,)" and not flagPunc:
        flagPunc = True
        countFlag += 1

match countFlag:
    case 4:
        print("Надежный")
    case 3:
        print("Хороший")
    case 2:
        print("Средний")
    case 1:
        print("Плохой")
    case 0:
        print("Безнадежный")
