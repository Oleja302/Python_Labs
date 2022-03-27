import tkinter.filedialog
from tkinter import *
import xml.etree.ElementTree as ET, json, hashlib
from pyparsing import *

from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import func
from tkinter import messagebox as mb
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'
    name = Column(String(50), primary_key=True)
    idAuthor = Column(String(15), ForeignKey('authors.id'), nullable=False)
    countPage = Column(Integer, nullable=False)
    publishOffice = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)


class Author(Base):
    __tablename__ = 'authors'
    id = Column(String(15), primary_key=True)
    name = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    yearsBorn = Column(Integer, nullable=False)
    yearsDead = Column(Integer, nullable=False)
    books = relationship("Book")


class User(Base):
    __tablename__ = 'users'
    login = Column(String(50), primary_key=True)
    password = Column(String(50), nullable=False)


def displayAuthorList():
    for author in sorted(session.query(Author).all(), key=lambda a: a.id):
        authorList.insert(authorList.size(), f'{author.name} {author.yearsBorn}-{author.yearsDead}')


def displayBookList():
    for book in sorted(session.query(Book).all(), key=lambda b: b.name):
        bookList.insert(bookList.size(), f'{book.name} {book.countPage} {book.year}')


def checkShowMainWindow():
    for user in session.query(User).all():
        if hashlib.md5(str.encode(password.get())).hexdigest() == user.password and login.get() == user.login:
            window.deiconify()
            refAutWin.destroy()


def closeAuthorizeWindow():
    window.destroy()


def saveAuthorXML():
    i = 0
    author = Author()

    for a in sorted(session.query(Author).all(), key=lambda a: a.id):
        if i == int(authorList.curselection()[0]):
            author = a
            break
        i += 1

    root = ET.Element('author')
    ET.SubElement(root, 'name').text = author.name
    ET.SubElement(root, 'country').text = author.country

    years = ET.SubElement(root, 'years')
    years.set('born', str(author.yearsBorn))
    years.set('dead', str(author.yearsDead))

    tree = ET.ElementTree(root)
    tree.write('author.xml')


def saveAuthorJson():
    i = 0
    author = None
    for a in sorted(session.query(Author).all(), key=lambda a: a.id):
        if i == int(authorList.curselection()[0]):
            author = a
            break
        i += 1

    dataToJson = {'name': f'{author.name}', 'country': f'{author.country}',
                  'years': [author.yearsBorn, author.yearsDead]}

    with open('author.json', 'w') as f:
        f.write(json.dumps(dataToJson))


def addAuthorInList():
    session.add(
        Author(id=id.get(), name=name.get(), country=country.get(), yearsBorn=int(yearBorn.get()),
               yearsDead=int(yearDead.get())))
    session.commit()
    authorList.delete(0, authorList.size() - 1)
    displayAuthorList()

    id.set('')
    name.set('')
    country.set('')
    yearBorn.set('')

    refAddAutWin.destroy()


def addBookInList():
    session.add(
        Book(idAuthor=idAuthor.get(), name=nameBook.get(), countPage=int(countPage.get()),
             publishOffice=publishOffice.get(),
             year=int(yearOfIssue.get())))
    session.commit()
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

    session.add(
        Author(id=dataFromFile[0], name=dataFromFile[1], country=dataFromFile[2], yearsBorn=int(dataFromFile[3]),
               yearsDead=int(dataFromFile[4])))
    session.commit()
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
    authors = session.query(Author).filter(start <= Author.yearsBorn, Author.yearsBorn <= end).all()
    mb.showinfo("Результат запроса", '\n'.join([a.name for a in authors]))


def booksFromRussia():
    authors = session.query(Author).filter(Author.country == 'Russia').all()
    books = sum([a.books for a in authors], [])
    mb.showinfo("Результат запроса", '\n'.join([b.name for b in books]))


def booksCountPage(countPage=500):
    books = session.query(Book).filter(Book.countPage > countPage).all()
    mb.showinfo("Результат запроса", '\n'.join([b.name for b in books]))


def authorsCountBooks(countBook=0):
    books = [a for a in session.query(Author).all() if len(a.books) > countBook]
    mb.showinfo("Результат запроса", '\n'.join([b.name for b in books]))


# SQLAlchemy
engine = create_engine("postgresql+psycopg2://postgres:1111@localhost/pycharm")

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
s = sessionmaker(bind=engine)
session = Session(bind=engine)

# Test data
#
# session.add(User(login='oleja', password=hashlib.md5(str.encode('123')).hexdigest()))
#
# session.add(Book(idAuthor=111, name='War and Peace', countPage='500', publishOffice='Lambda', year='1859'))
# session.add(Book(idAuthor=122, name='Labutan', countPage='300', publishOffice='Lambda', year='1859'))
# session.add(Book(idAuthor=133, name='Sanctum', countPage='450', publishOffice='Lambda', year='1859'))
# session.add(Book(idAuthor=144, name='Peace Death', countPage='120', publishOffice='Lambda', year='1859'))
# session.add(Book(idAuthor=155, name='Ctulhu', countPage='800', publishOffice='Lambda', year='1859'))
# session.add(Book(idAuthor=155, name='Pokemon', countPage='550', publishOffice='Lambda', year='1859'))
#
# session.add(Author(id=111, name='L.N.Tolstoi', country='Russia', yearsBorn=1800, yearsDead=1910))
# session.add(Author(id=122, name='M.A.Lermontow', country='Russia', yearsBorn=1828, yearsDead=1910))
# session.add(Author(id=133, name='M.V.Lomonosov', country='Russia', yearsBorn=1830, yearsDead=1910))
# session.add(Author(id=144, name='G.G.Garrison', country='USA', yearsBorn=1818, yearsDead=1910))
# session.add(Author(id=155, name='G.H.Lavcraft', country='America', yearsBorn=1830, yearsDead=1910))
# session.add(Author(id=166, name='S.I.Shapavalow', country='Japanese', yearsBorn=1840, yearsDead=1910))
#
# session.commit()

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
