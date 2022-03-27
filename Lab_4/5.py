import time
import os
import tkinter
from tkinter import ttk
import requests
from tkinter import *
import threading
from matplotlib import ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# https://mathus.ru/phys/book.pdf
# https://mf.bmstu.ru/info/faculty/kf/caf/k6/lit/docs/uchebnik/Trofimova_Kurs_fiziki.pdf
# http://rl.odessa.ua/media/_For_Liceistu/Physics/Myakishev_Phys-10.pdf


def windowResult():
    resWin = Toplevel(window)
    f = Figure(figsize=(5, 5), dpi=100)

    # Bar
    ax1 = f.add_subplot(121)
    ax1.bar(timeDownload.keys(), timeDownload.values())

    ax1.grid(color='green', linestyle='dotted')
    ax1.set_ylabel('Download time')
    ax1.set_title("Download time plot")
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(1))

    for i, rect in enumerate(ax1.patches):
        height = rect.get_height()
        label = f'{int(timeDownload[list(timeDownload.keys())[i]])}s {int(timeDownload[list(timeDownload.keys())[i]] % 1 * 1000)}ms'
        ax1.text(rect.get_x() + rect.get_width() / 2, height, label, ha='center', va='bottom')

    # Pie
    ax2 = f.add_subplot(122)
    ax2.pie(sizeDownload.values(), labels=sizeDownload.keys())
    ax2.set_title("File size")

    canvas = FigureCanvasTkAgg(f, resWin)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)


def downloadFile(url, progressBar, lab):
    if url:
        filename = url.split('/')[-1]
        r = requests.get(url, allow_redirects=True)
        with open(filename, "wb") as file:
            startTime = time.time()
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    file.write(chunk)
                    progressBar['value'] += 100 / (len(r.content) / len(chunk))
                    lab['text'] = int(progressBar['value']), '%'
            timeDownload[filename] = time.time() - startTime
            size = float('{:.2f}'.format(len(r.content) / 1e+6))
            sizeDownload[filename + f'\n[{size}mb]'] = size
        lab['text'] = '100%'

        if threading.active_count() == 2:
            windowResult()


def startThreads():
    threadUrl1 = threading.Thread(target=downloadFile, args=(url1.get(), progressBar1, lab1), daemon=True)
    threadUrl2 = threading.Thread(target=downloadFile, args=(url2.get(), progressBar2, lab2), daemon=True)
    threadUrl3 = threading.Thread(target=downloadFile, args=(url3.get(), progressBar3, lab3), daemon=True)

    threadUrl1.start()
    threadUrl2.start()
    threadUrl3.start()


# Main window
window = Tk()
window.title("Скачиватель3000")
window.geometry('300x400')

timeDownload = {}
sizeDownload = {}
downloadFolder = os.path.abspath(os.curdir)
url1 = StringVar()
url1.set('https://mathus.ru/phys/book.pdf')
url2 = StringVar()
url2.set('https://mf.bmstu.ru/info/faculty/kf/caf/k6/lit/docs/uchebnik/Trofimova_Kurs_fiziki.pdf')
url3 = StringVar()
url3.set('http://rl.odessa.ua/media/_For_Liceistu/Physics/Myakishev_Phys-10.pdf')

# Entry
entryURL1 = Entry(textvariable=url1, width=30)
entryURL1.place(relx=0.9, rely=0.15, anchor="e")

entryURL2 = Entry(textvariable=url2, width=30)
entryURL2.place(relx=0.9, rely=0.35, anchor="e")

entryURL3 = Entry(textvariable=url3, width=30)
entryURL3.place(relx=0.9, rely=0.55, anchor="e")

# Button
b = Button(text="Start downloading!", command=startThreads)
b.place(relx=0.5, rely=0.8, height=40, width=130, anchor="center")

# Label
lab1 = Label(text='0%')
lab1.place(relx=0.75, rely=0.22, anchor="e")

lab2 = Label(text='0%')
lab2.place(relx=0.75, rely=0.42, anchor="e")

lab3 = Label(text='0%')
lab3.place(relx=0.75, rely=0.62, anchor="e")

# Progress bar
progressBar1 = ttk.Progressbar(window, orient="horizontal", mode="determinate", maximum=100, value=0, length=150)
progressBar1.place(relx=0.6, rely=0.22, anchor="e")

progressBar2 = ttk.Progressbar(window, orient="horizontal", mode="determinate", maximum=100, value=0, length=150)
progressBar2.place(relx=0.6, rely=0.42, anchor="e")

progressBar3 = ttk.Progressbar(window, orient="horizontal", mode="determinate", maximum=100, value=0, length=150)
progressBar3.place(relx=0.6, rely=0.62, anchor="e")

window.mainloop()
