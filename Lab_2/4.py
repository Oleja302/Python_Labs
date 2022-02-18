import re

print("Введите название файла: ")
fileName = input()
template = re.compile(r"(\(\d{3}\)\d{3}\d{2}\d{2})|(\(\d{3}\)\d{3}-\d{2}-\d{2})")

with open(fileName, "r", encoding="utf8") as file:
    numbers = file.readlines()

for i in range(0, len(numbers)):
    result = re.search(template, numbers[i])
    if result != None:
        print("Строка {}, позиция {} : найдено {}".format(i, result.span()[0], result.group()))
