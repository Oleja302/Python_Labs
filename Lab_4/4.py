import os
from pymongo import MongoClient
import tkinter.filedialog
from tkinter import *
import xml.etree.ElementTree as ET, json, hashlib
from pyparsing import *
from tkinter import messagebox as mb


def displayAuthorList():
    for author in db.authors.find():
        authorList.insert(authorList.size(),
                          author['name'] + ' ' + str(author['yearsBorn']) + '-' + str(author['yearsDead']))


def displayBookList():
    for book in db.books.find():
        bookList.insert(bookList.size(), book['name'] + ' ' + str(book['countPage']) + ' ' + str(book['year']))


def checkShowMainWindow():
    for user in db.users.find():
        if hashlib.md5(str.encode(password.get())).hexdigest() == user['password'] and login.get() == user['login']:
            window.deiconify()
            refAutWin.destroy()


def closeAuthorizeWindow():
    window.destroy()


def saveAuthorXML():
    i = 0
    author = None

    for a in db.authors.find():
        if i == int(authorList.curselection()[0]):
            author = a
            break
        i += 1

    root = ET.Element('author')
    ET.SubElement(root, 'name').text = author['name']
    ET.SubElement(root, 'country').text = author['country']

    years = ET.SubElement(root, 'years')
    years.set('born', str(author['yearsBorn']))
    years.set('dead', str(author['yearsDead']))

    tree = ET.ElementTree(root)
    tree.write('author.xml')


def saveAuthorJson():
    i = 0
    author = None

    db.authors.find()

    for a in db.authors.find():
        if i == int(authorList.curselection()[0]):
            author = a
            break
        i += 1

    dataToJson = {'name': author['name'], 'country': author['country'],
                  'years': [author['yearsBorn'], author['yearsDead']]}

    with open('author.json', 'w') as f:
        f.write(json.dumps(dataToJson))


def addAuthorInList():
    db.authors.insert_one(
        {"id": id.get(), "name": name.get(), "country": country.get(), "yearsBorn": int(yearBorn.get()),
         'yearsDead': int(yearDead.get())})
    authorList.delete(0, authorList.size() - 1)
    displayAuthorList()

    id.set('')
    name.set('')
    country.set('')
    yearBorn.set('')

    refAddAutWin.destroy()


def addBookInList():
    db.books.insert_one({"idAuthor": idAuthor.get(), "name": nameBook.get(), "countPage": int(countPage.get()),
                         "publishOffice": publishOffice.get(), 'year': int(yearOfIssue.get())})
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

    db.authors.insert_one(
        {"id": dataFromFile[0], "name": dataFromFile[1], "country": dataFromFile[2], "yearsBorn": int(dataFromFile[3]),
         'yearsDead': int(dataFromFile[4])})

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


def authorsFromRange(start=1829, end=2000):
    authors = db.authors.find({"$and": [{"yearsBorn": {"$gt": start}}, {"yearsDead": {"$lt": end}}]})
    mb.showinfo("Результат запроса", '\n'.join([a['name'] for a in authors]))


def booksFromRussia():
    books = [[b for b in db.books.find({"idAuthor": a["id"]})] for a in db.authors.find({"country": "Russia"})]
    books = sum(books, [])
    mb.showinfo("Результат запроса", '\n'.join([b['name'] for b in books]))


def booksCountPage(countPage=500):
    books = db.books.find({"countPage": {"$gt": countPage}})
    mb.showinfo("Результат запроса", '\n'.join([b['name'] for b in books]))


def authorsCountBooks(countBook=0):
    books = [a for a in db.authors.find() if db.books.count_documents({'idAuthor': a['id']}) > countBook]
    mb.showinfo("Результат запроса", '\n'.join([b['name'] for b in books]))


# MongoDB
with open('mongod.bat', 'w') as mongodBat:
    mongodBat.write(
        'start mongod ' + '--dbpath ' + os.path.abspath(os.curdir) + '\\mongodb')
os.startfile('mongod.bat')

client = MongoClient()
db = client.pycharm

# Test data
# db.users.insert_one({"login": "oleja",
#                      "password": hashlib.md5(str.encode('123')).hexdigest(),
#                      })
#
# db.books.insert_one(
#     {"idAuthor": 111, "name": "War and Peace", "countPage": 500, "publishOffice": 'Lambda', 'year': 1859})
# db.books.insert_one({"idAuthor": 122, "name": "Labutan", "countPage": 300, "publishOffice": 'Lambda', 'year': 1859})
# db.books.insert_one({"idAuthor": 133, "name": "Sanctum", "countPage": 450, "publishOffice": 'Lambda', 'year': 1859})
# db.books.insert_one({"idAuthor": 144, "name": "Peace Death", "countPage": 120, "publishOffice": 'Lambda', 'year': 1859})
# db.books.insert_one({"idAuthor": 155, "name": "Ctulhu", "countPage": 800, "publishOffice": 'Lambda', 'year': 1859})
# db.books.insert_one({"idAuthor": 155, "name": "Pokemon", "countPage": 550, "publishOffice": 'Lambda', 'year': 1859})
#
# db.authors.insert_one({"id": 111, "name": "L.N.Tolstoi", "country": "Russia", "yearsBorn": 1800, 'yearsDead': 1910})
# db.authors.insert_one({"id": 122, "name": "M.A.Lermontow", "country": "Russia", "yearsBorn": 1828, 'yearsDead': 1910})
# db.authors.insert_one({"id": 133, "name": "M.V.Lomonosov", "country": "Russia", "yearsBorn": 1830, 'yearsDead': 1910})
# db.authors.insert_one({"id": 144, "name": "G.G.Garrison", "country": "USA", "yearsBorn": 1818, 'yearsDead': 1910})
# db.authors.insert_one({"id": 155, "name": "G.H.Lavcraft", "country": "America", "yearsBorn": 1830, 'yearsDead': 1910})
# db.authors.insert_one(
#     {"id": 166, "name": "S.I.Shapavalow", "country": "Japanese", "yearsBorn": 1840, 'yearsDead': 1910})

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

queryMenu = Menu(window, tearoff=0)
queryMenu.add_command(label="Авторы, родившиеся в диапазоне", command=authorsFromRange)
queryMenu.add_command(label="Книга российских авторов", command=booksFromRussia)
queryMenu.add_command(label="Книги с количеством страниц", command=booksCountPage)
queryMenu.add_command(label="Авторы, с числом книг более", command=authorsCountBooks)

mainMenu = Menu(window)
mainMenu.add_cascade(label="Файл", menu=fileMenu)
mainMenu.add_cascade(label="Добавить", menu=addMenu)
mainMenu.add_cascade(label='Запросы', menu=queryMenu)
window.config(menu=mainMenu)

displayBookList()
displayAuthorList()
createAuthorizeWindow()
window.mainloop()
