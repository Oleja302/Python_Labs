# -*- coding: cp1251 -*-

print("������� ����� �����:", end=" ")
card = input()

hiddenCard = card.replace(card[4:12], "********")
print(hiddenCard)
