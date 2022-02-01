# -*- coding: cp1251 -*-

print("Введите текст:", end=" ")
text = input()

splittedText = text.split(" ")
words = [[], [], []]

for word in splittedText:
    if len(word) > 7:
        words[0].append(word)
    elif len(word) >= 4 and len(word) <= 7:
        words[1].append(word)
    else:
        words[2].append(word)

print(words[0])
print(words[1])
print(words[2])
