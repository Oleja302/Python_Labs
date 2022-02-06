import os
import pathlib

directory = os.walk("music")
musicFromFile = None

with open("music/music.txt", "r", encoding="utf8") as file:
    musicFromFile = [i.rstrip('\n') for i in file.readlines() if not i.endswith(".txt")]

for dir, folders, files in directory:
    for music in files:
        if not music.endswith(".txt") and music[:music.find('.')] in "".join(musicFromFile):
            rightMusic = [s for s in musicFromFile if music[:music.find('.')] in s]
            if len(rightMusic): os.rename("music/" + music, "music/" + rightMusic[0] + pathlib.Path("music/" + music).suffix)
