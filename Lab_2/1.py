def readFile(fileName):
    textFromFile = None
    chars = {}
    listChars = ()

    with open(fileName, "r", encoding="utf8") as file:
        textFromFile = file.read()

    for symbol in textFromFile:
        if symbol.lower() in chars and symbol.lower().isalpha():
            chars[symbol.lower()] += 1
        elif symbol.lower().isalpha():
            chars[symbol.lower()] = 1

    listChars = list(chars.items())
    listChars.sort(key=lambda i: i[1])

    return listChars


print(readFile("text1ru.txt"))
print(readFile("text1en.txt"))
