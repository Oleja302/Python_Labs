class Taggable(object):
    def tag(self):
        raise NotImplementedError


class Book(Taggable):
    id = 0

    def __init__(self, author, title):
        self.id = 0
        if not title:
            raise ValueError
        self.title = title
        self.author = author

    def __str__(self):
        return f'[{self.id}] {self.author} \'{self.title}\''

    def tag(self):
        return [word for word in self.title.split(' ') if word[0].isupper()]


class Library(object):
    i = 0

    def __init__(self, number, street):
        self.bookList = []
        self.number = number
        self.street = street

    def __iadd__(self, book):
        Book.id += 1
        book.id = Book.id
        self.bookList.append(book)
        return self

    def __iter__(self):
        return self

    def __next__(self):
        if Library.i < len(self.bookList):
            elem = self.bookList[Library.i]
            Library.i += 1
        else:
            Library.i = 0
            raise StopIteration
        return elem


lib = Library(1, '51 Some str., NY')
lib += Book('Leo Tolstoi', 'War and Peace')
lib += Book('Charles Dickens', 'David Copperfield')

for book in lib:
    # вывод в виде: [1] L.Tolstoi ‘War and Peace’
    print(book)
    # вывод в виде: [‘War’, ‘Peace’]
    print(book.tag())