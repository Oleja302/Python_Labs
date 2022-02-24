class StringFormatter(object):
    separator = ' '

    def deleteLenWords(self, string, n):
        formatString = string.split(self.separator)
        formatString = [w for w in formatString if len(w) >= n]
        return self.separator.join(formatString)

    def replaceDigit(self, string):
        formatString = [w if not w.isdigit() else '*' for w in string]
        formatString = ''.join(formatString)
        return formatString

    def insertSpace(self, string):
        return ' '.join(string)

    def sortLenWords(self, string):
        listWords = string.split(self.separator)
        listWords.sort(key=lambda w: len(w))
        return self.separator.join(listWords)

    def sortAlphabet(self, string):
        listWords = string.split(self.separator)
        listWords.sort()
        return self.separator.join(listWords)


sf = StringFormatter()

string = 'hell hello aa 123 b c h he hel'

string = sf.deleteLenWords(string, 3)
string = sf.replaceDigit(string)
string = sf.replaceDigit(string)
string = sf.sortLenWords(string)
string = sf.insertSpace(string)

print(string)
