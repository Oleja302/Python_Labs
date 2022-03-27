import tkinter.filedialog
from tkinter import *
import xml.etree.ElementTree as ET, json, hashlib
from pyparsing import *


class Book:
    def __init__(self, idAuthor, name, countPage, publishOffice, year):
        self.idAuthor = idAuthor
        self.name = name
        self.countPage = countPage
        self.publishOffice = publishOffice
        self.year = year


class Author:
    def __init__(self, id, name, country, yearBorn, yearsDead):
        self.id = id
        self.name = name
        self.country = country
        self.yearsBorn = yearBorn
        self.yearsDead = yearsDead


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = hashlib.md5(str.encode(password)).hexdigest()


class DataBaseLibrary:
    def __init__(self):
        self.users = []
        self.authors = []
        self.books = []

    def addBook(self, book):
        self.books.append(book)

    def addAuthor(self, author):
        self.authors.append(author)

    def addUser(self, user):
        self.users.append(user)


def displayAuthorList():
    for author in db.authors:
        authorList.insert(0, f'{author.name} {author.yearsBorn}-{author.yearsDead}')


def displayBookList():
    for book in db.books:
        bookList.insert(0, f'{book.name} {book.countPage} {book.year}')


def checkShowMainWindow():
    for user in db.users:
        if hashlib.md5(str.encode(password.get())).hexdigest() == user.password and login.get() == user.login:
            window.deiconify()
            refAutWin.destroy()


def closeAuthorizeWindow():
    window.destroy()


def saveAuthorXML():
    author = db.authors[int(authorList.curselection()[0])]
    root = ET.Element('author')
    ET.SubElement(root, 'name').text = author.name
    ET.SubElement(root, 'country').text = author.country

    years = ET.SubElement(root, 'years')
    years.set('born', str(author.yearsBorn))
    years.set('dead', str(author.yearsDead))

    tree = ET.ElementTree(root)
    tree.write('author.xml')


def saveAuthorJson():
    author = db.authors[int(authorList.curselection()[0])]
    dataToJson = {'name': f'{author.name}', 'country': f'{author.country}',
                  'years': [author.yearsBorn, author.yearsDead]}

    with open('author.json', 'w') as f:
        f.write(json.dumps(dataToJson))


def addAuthorInList():
    db.addAuthor(Author(id.get(), name.get(), country.get(), yearBorn.get(), yearDead.get()))
    authorList.delete(0, authorList.size() - 1)
    displayAuthorList()

    id.set('')
    name.set('')
    country.set('')
    yearBorn.set('')

    refAddAutWin.destroy()


def addBookInList():
    db.addBook(Book(idAuthor.get(), nameBook.get(), countPage.get(), publishOffice.get(), yearOfIssue.get()))
    bookList.delete(0, bookList.size() - 1)
    displayBookList()

    idAuthor.set('')
    nameBook.set('')
    countPage.set('')
    publishOffice.set('')
    yearOfIssue.set('')

    refAddBookWin.destroy()


def parseAuthorFile():
    authorFile = tkinter.filedialog.askopenfilename(title='Выбор файла')

    parseID = Suppress('id:') + Word(nums)
    parseName = Suppress('name:') + Word(alphas)
    parseCountry = Suppress('country:') + Word(alphas)
    parseYear = Suppress('year:') + Word(nums, exact=4) + Optional(Suppress('-') + Word(nums, exact=4))

    parser = parseID + parseName + parseCountry + parseYear
    dataFromFile = parser.parseFile(authorFile)

    db.addAuthor(Author(dataFromFile[0], dataFromFile[1], dataFromFile[2], dataFromFile[3], dataFromFile[4]))
    authorList.delete(0, authorList.size() - 1)
    displayAuthorList()


def showAddAuthorWindow():
    addAuthorWindow = Toplevel(window)
    addAuthorWindow.title("Добавление автора")
    addAuthorWindow.geometry('300x250')

    global refAddAutWin
    refAddAutWin = addAuthorWindow

    name_label = Label(addAuthorWindow, text="Id: ")
    name_label.grid(row=0, column=0)

    name_label = Label(addAuthorWindow, text="Имя: ")
    name_label.grid(row=1, column=0)

    name_label = Label(addAuthorWindow, text="Страна: ")
    name_label.grid(row=2, column=0)

    name_label = Label(addAuthorWindow, text="Год рождения: ")
    name_label.grid(row=3, column=0)

    name_label = Label(addAuthorWindow, text="Год смерти: ")
    name_label.grid(row=4, column=0)

    entryId = Entry(addAuthorWindow, textvariable=id)
    entryId.grid(row=0, column=1, padx=20, pady=5)

    entryName = Entry(addAuthorWindow, textvariable=name)
    entryName.grid(row=1, column=1, padx=20, pady=5)

    entryCountry = Entry(addAuthorWindow, textvariable=country)
    entryCountry.grid(row=2, column=1, padx=20, pady=5)

    entryYearBorn = Entry(addAuthorWindow, textvariable=yearBorn)
    entryYearBorn.grid(row=3, column=1, padx=20, pady=5)

    entryYearDead = Entry(addAuthorWindow, textvariable=yearDead)
    entryYearDead.grid(row=4, column=1, padx=20, pady=5)

    b = Button(addAuthorWindow, text="Добавить", command=addAuthorInList)
    b.place(relx=0.5, rely=0.8, height=40, width=130, anchor="center")


def showAddBookWindow():
    addBookWindow = Toplevel(window)
    addBookWindow.title("Добавление книги")
    addBookWindow.geometry('350x250')

    global refAddBookWin
    refAddBookWin = addBookWindow

    name_label = Label(addBookWindow, text="Id автора: ")
    name_label.grid(row=0, column=0)

    name_label = Label(addBookWindow, text="Название: ")
    name_label.grid(row=1, column=0)

    name_label = Label(addBookWindow, text="Количество страниц: ")
    name_label.grid(row=2, column=0)

    name_label = Label(addBookWindow, text="Издательство: ")
    name_label.grid(row=3, column=0)

    name_label = Label(addBookWindow, text="Год: ")
    name_label.grid(row=4, column=0)

    entryId = Entry(addBookWindow, textvariable=idAuthor)
    entryId.grid(row=0, column=1, padx=20, pady=5)

    entryName = Entry(addBookWindow, textvariable=nameBook)
    entryName.grid(row=1, column=1, padx=20, pady=5)

    entryCountry = Entry(addBookWindow, textvariable=countPage)
    entryCountry.grid(row=2, column=1, padx=20, pady=5)

    entryYear = Entry(addBookWindow, textvariable=publishOffice)
    entryYear.grid(row=3, column=1, padx=20, pady=5)

    entryYear = Entry(addBookWindow, textvariable=yearOfIssue)
    entryYear.grid(row=4, column=1, padx=20, pady=5)

    b = Button(addBookWindow, text="Добавить", command=addBookInList)
    b.place(relx=0.5, rely=0.85, height=40, width=130, anchor="center")


def createAuthorizeWindow():
    authorizeWindow = Toplevel(window)
    authorizeWindow.title("Авторизация")
    authorizeWindow.geometry('400x200')

    global refAutWin
    refAutWin = authorizeWindow

    # Label
    name_label = Label(authorizeWindow, text="Введите логин:")
    surname_label = Label(authorizeWindow, text="Введите пароль:")

    name_label.place(relx=0.1, rely=0.15, anchor="w")
    surname_label.place(relx=0.1, rely=0.3, anchor="w")

    # Entry
    entryLogin = Entry(authorizeWindow, textvariable=login)
    entryLogin.place(relx=0.8, rely=0.15, anchor="e")

    entryPassword = Entry(authorizeWindow, textvariable=password)
    entryPassword.place(relx=0.8, rely=0.3, anchor="e")

    b = Button(authorizeWindow, text="Войти", command=checkShowMainWindow)
    b.place(relx=0.5, rely=0.65, height=40, width=130, anchor="center")

    authorizeWindow.protocol('WM_DELETE_WINDOW', closeAuthorizeWindow)


db = DataBaseLibrary()

# Test
db.addUser(User('oleja', '123'))

db.addBook(Book(123, 'War and Peace', '100200', 'Lambda', '1859'))
db.addBook(Book(123, 'War and Peace', '100200', 'Lambda', '1859'))
db.addBook(Book(123, 'War and Peace', '100200', 'Lambda', '1859'))
db.addBook(Book(123, 'War and Peace', '100200', 'Lambda', '1859'))
db.addBook(Book(123, 'War and Peace', '100200', 'Lambda', '1859'))

db.addAuthor(Author(123, 'L.N.Tolstoi', 'Russia', 1828, 1910))
db.addAuthor(Author(123, 'L.N.Tolstoi', 'Russia', 1828, 1910))
db.addAuthor(Author(123, 'L.N.Tolstoi', 'Russia', 1828, 1910))
db.addAuthor(Author(123, 'L.N.Tolstoi', 'Russia', 1828, 1910))
db.addAuthor(Author(123, 'L.N.Tolstoi', 'Russia', 1828, 1910))

# Main window
window = Tk()
window.withdraw()
window.title("БД библиотеки")
window.geometry('750x600')

login = StringVar()
password = StringVar()

id = StringVar()
name = StringVar()
country = StringVar()
yearBorn = StringVar()
yearDead = StringVar()

idAuthor = StringVar()
nameBook = StringVar()
countPage = StringVar()
publishOffice = StringVar()
yearOfIssue = StringVar()

refAutWin = None
refAddAutWin = None
refAddBookWin = None

# Lists
bookList = Listbox(window, width=40, height=28)
bookList.grid(column=0, row=0, padx=20)
authorList = Listbox(window, width=40, height=28)
authorList.grid(column=1, row=0, padx=20)

# Menu
saveMenu = Menu(window, tearoff=0)
saveMenu.add_command(label="json", command=saveAuthorJson)
saveMenu.add_command(label="XML", command=saveAuthorXML)

fileMenu = Menu(window, tearoff=0)
fileMenu.add_cascade(label="Сохранить автора", menu=saveMenu)

addMenu = Menu(window, tearoff=0)
addMenu.add_command(label="Автора", command=showAddAuthorWindow)
addMenu.add_command(label="Автора через файл", command=parseAuthorFile)
addMenu.add_command(label="Книгу", command=showAddBookWindow)

mainMenu = Menu(window)
mainMenu.add_cascade(label="Файл", menu=fileMenu)
mainMenu.add_cascade(label="Добавить", menu=addMenu)
window.config(menu=mainMenu)

# сразу после вызова mainloop начинают отрисовываться все виджеты и окна(даже если они созданы во время его работы)
# по умолчанию при запуске mainloop все виджеты отрисовываются на главном окне. Если их два, то они отрисовываются на том,
# что появилось раньше. Нужно указывать, к какому окну они принадлежат

displayBookList()
displayAuthorList()
createAuthorizeWindow()
window.mainloop()
