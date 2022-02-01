# -*- coding: cp1251 -*-

def non_empty(get_pages):
    def wrapper():

        pages = get_pages()

        for i in pages:
            if i == "" or i == None:
                pages.remove(i)

        return pages
    return wrapper


@non_empty
def get_pages():
    return ['chapter1', '', 'contents', '', 'line1']


print(get_pages())
