# -*- coding: cp1251 -*-

print("Введите текст:", end=" ")
text = input()
newText = ""

i = 0
flag = False

while i != len(text):
    if text[i].isupper() and text[i].isalpha():
        flag = True

    if flag and text[i].isalpha():
        newText += text[i].upper()
    elif flag and not text[i].isalpha():
        newText += text[i]
        flag = False
    else:
        newText += text[i]

    i += 1

print(newText)
