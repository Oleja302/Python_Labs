import sys
from PyQt5 import QtWidgets, uic


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


class Main(QtWidgets.QMainWindow):
    def __init__(self, sf):
        super(Main, self).__init__()
        uic.loadUi('string formatter.ui', self)

        self.stringFormatter = sf

        self.flagDel = False
        self.flagRep = False
        self.flagIns = False
        self.flagSor = False
        self.flagSortSize = False

        self.pushButton.clicked.connect(self.format)
        self.checkBox.stateChanged.connect(self.setFlagDel)
        self.checkBox_2.stateChanged.connect(self.setFlagRep)
        self.checkBox_3.stateChanged.connect(self.setFlagIns)
        self.checkBox_4.stateChanged.connect(self.setFlagSor)
        self.radioButton.toggled.connect(self.setFlagSortSize)

    def format(self):
        string = self.lineEdit.text()

        if len(string) != 0:
            if self.flagDel:
                string = self.stringFormatter.deleteLenWords(string, self.spinBox.value())
            if self.flagRep:
                string = self.stringFormatter.replaceDigit(string)
            if self.flagIns:
                string = self.stringFormatter.insertSpace(string)
            if self.flagSor:
                if self.flagSortSize:
                    string = self.stringFormatter.sortLenWords(string)
                else:
                    string = self.stringFormatter.sortAlphabet(string)

        self.lineEdit_2.setText(string)

    def setFlagDel(self):
        if self.checkBox.isChecked():
            self.flagDel = True
        else:
            self.flagDel = False

    def setFlagRep(self):
        if self.checkBox_2.isChecked():
            self.flagRep = True
        else:
            self.flagRep = False

    def setFlagIns(self):
        if self.checkBox_3.isChecked():
            self.flagIns = True
        else:
            self.flagIns = False

    def setFlagSor(self):
        if self.checkBox_4.isChecked():
            self.flagSor = True
            self.radioButton.setEnabled(True)
            self.radioButton_2.setEnabled(True)
        else:
            self.flagSor = False
            self.radioButton.setEnabled(False)
            self.radioButton_2.setEnabled(False)

    def setFlagSortSize(self):
        if self.flagSor:
            if self.radioButton.isChecked():
                self.flagSortSize = True
            else:
                self.flagSortSize = False


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    sf = StringFormatter()

    mainWindow = Main(sf)
    mainWindow.show()

    sys.exit(app.exec_())
