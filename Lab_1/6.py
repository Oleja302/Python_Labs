# -*- coding: cp1251 -*-

print("������� �����:", end=" ")
text = input()
newText = ""

i = 0
while i < len(text):
    if text.find(text[i], 0, i) == -1:
        print(text[i], end=" ")
    i += 1

print()