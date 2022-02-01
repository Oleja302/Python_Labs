# -*- coding: cp1251 -*-

print("Введите номер карты:", end=" ")
card = input()

hiddenCard = card.replace(card[4:12], "********")
print(hiddenCard)
