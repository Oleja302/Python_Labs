from PyQt5 import QtWidgets, uic
import re, datetime, os, sys


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('finder strings.ui', self)

        self.checkLog()
        self.action.triggered.connect(self.selectFile)
        self.action_6.triggered.connect(self.exportInFile)
        self.action_7.triggered.connect(self.addInLog)
        self.action_8.triggered.connect(self.readLog)

        self.actionInfo = QtWidgets.QLabel()
        self.sizeFile = QtWidgets.QLabel()

        self.actionInfo.setFixedWidth(int(self.geometry().width() * 60 / 100 - 15))
        self.sizeFile.setFixedWidth(int(self.geometry().width() * 40 / 100 - 15))

        self.statusBar.addWidget(self.actionInfo)
        self.statusBar.addWidget(self.sizeFile)

    def checkLog(self):
        if not os.path.exists('script18.log'):
            msgLog = QtWidgets.QMessageBox()
            msgLog.setIcon(QtWidgets.QMessageBox.Information)
            msgLog.setWindowTitle("Информация")
            msgLog.setText("Файл лога не найден.\nФайл будет создан автоматически")
            msgLog.show()
            msgLog.exec()

            open('script18.log', 'tw')

    def findPhoneNumber(self, fileName):
        template = re.compile(r"(\(\d{3}\)\d{3}\d{2}\d{2})|(\(\d{3}\)\d{3}-\d{2}-\d{2})")

        now = datetime.datetime.now()
        fileDate = QtWidgets.QListWidgetItem(
            "Файл {} был обработан {}\n".format(fileName, now.strftime("%d.%m.%Y %H:%M:%S")))
        self.listWidget.addItem(fileDate)

        with open(fileName, "r", encoding="utf8") as file:
            numbers = file.readlines()

        for i in range(0, len(numbers)):
            result = re.search(template, numbers[i])
            if result is not None:
                item = QtWidgets.QListWidgetItem(
                    "Строка {}, позиция {} : найдено {}".format(i, result.span()[0], result.group()))
                self.listWidget.addItem(item)

        self.listWidget.show()
        self.addInStatusBar('Обработан файл ' + fileName, os.path.getsize(fileName))

    def addInStatusBar(self, fileName, size):

        formatSize = []
        strSize = str(size)

        while strSize:
            formatSize.insert(0, strSize[-3:])
            strSize = strSize[:-3]

        self.actionInfo.setText(fileName)
        self.sizeFile.setText(' '.join(formatSize) + " байт")

    def exportInFile(self):
        itemsTextList = [str(self.listWidget.item(i).text()).replace('\n', '') for i in range(self.listWidget.count())]
        itemsTextList[0] += '\n'

        id = QtWidgets.QInputDialog()
        text, ok = id.getText(self.listWidget, 'Экспорт файла', 'Введите название файла:')
        id.show()

        if ok:
            with open(text, 'w', encoding='utf-8') as file:
                for item in itemsTextList:
                    file.write(item + '\n')

    def selectFile(self):
        self.findPhoneNumber(QtWidgets.QFileDialog.getOpenFileName()[0])

    def addInLog(self):
        itemsTextList = [str(self.listWidget.item(i).text()).replace('\n', '') for i in range(self.listWidget.count())]
        itemsTextList[0] += '\n'

        with open('script18.log', 'a', encoding='utf-8') as file:
            for item in itemsTextList:
                file.write(item + '\n')

    def readLog(self):
        readerLog = QtWidgets.QMessageBox()
        readerLog.setIcon(QtWidgets.QMessageBox.Warning)
        readerLog.setText("Вы действительно хотите открыть лог? \nДанные последних поисков будут потеряны!")
        readerLog.setWindowTitle("Предупреждение")
        readerLog.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No)
        readerLog.show()
        result = readerLog.exec()

        if result == QtWidgets.QMessageBox.Ok:
            self.listWidget.clear()

            with open('script18.log', 'r', encoding='utf-8') as file:
                line = file.readline()
                while line:
                    self.listWidget.addItem(line.replace('\n', '', 1))
                    line = file.readline()

            self.listWidget.show()

        self.addInStatusBar('Открыт лог', os.path.getsize('script18.log'))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    mainWindow = Main()
    mainWindow.show()

    sys.exit(app.exec_())
