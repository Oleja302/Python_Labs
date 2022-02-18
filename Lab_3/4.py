import itertools


class StringFormatter(object):
    separator = None

    def deleteLenWords(self, string, n):
        if StringFormatter.separator == None:
            StringFormatter.separator = ' '

        for sep in StringFormatter.separator:
            formatString = string.split(sep)
            formatString = [w for w in itertools.chain(formatString)]

        formatString = [w for w in formatString if len(w) >= n]

        return formatString

    def replaceDigit(self, string):
        formatString = [w if not w.isdigit() else '*' for w in string]
        return formatString


sf = StringFormatter()
StringFormatter.separator = ',. '

string = 'h he hel hell hello 123'
string = sf.deleteLenWords(string, 3)

print(string)
