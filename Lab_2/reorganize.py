import os
import argparse

# py reorganize.py --source "D:\Programming\Python\Python_Labs\Lab_2\directory6" --days 2 --size 4096

parser = argparse.ArgumentParser()
parser.add_argument('--source', '-source')
parser.add_argument('--days', '-days')
parser.add_argument('--size', '-size')
namespace = parser.parse_args()

direcrory = os.walk("directory6")

for dir, folder, file in direcrory:
    for i in range(0, len(file)):
        if os.path.getsize(os.path.abspath(dir + '\\' + file[i])) < int(namespace.size):
            if os.path.exists(namespace.source + '\\Small\\'):
                os.replace(dir + "\\" + file[i], namespace.source + '\\Small\\' + file[i])

            else:
                os.mkdir(namespace.source + '\\Small')
                os.replace(dir + "\\" + file[i], namespace.source + '\\Small\\' + file[i])

            print("Добавлен {} в папку Small".format(file[i]))
            continue

        if os.path.getmtime(os.path.abspath(dir + '\\' + file[i])) > int(namespace.days):
            if os.path.exists(namespace.source + '\\Archive\\'):
                os.replace(dir + "\\" + file[i], namespace.source + '\\Archive\\' + file[i])

            else:
                os.mkdir(namespace.source + '\\Archive')
                os.replace(dir + "\\" + file[i], namespace.source + '\\Archive\\' + file[i])

            print("Добавлен {} в папку Archive".format(file[i]))
