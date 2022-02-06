import os
import argparse
import ffmpeg

#py trackmix.py -s "D:\Programming\Python\Python_Labs\Lab_2\tracklist" -d "result.mp3" -c 3 -f 10 -l -e

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', required=True)
parser.add_argument('-d', '--destination')
parser.add_argument('-c', '--count')
parser.add_argument('-f', '--frame')
parser.add_argument('-l', '--log', action='store_const', const=True, default=False)
parser.add_argument('-e', '--extended', action='store_const', const=True, default=False)
namespace = parser.parse_args()

dirTrack = os.walk(namespace.source)
listCutTrack = []
j = 0

for dir, folder, musics in dirTrack:
    if namespace.count != None:
        if j == int(namespace.count): break

    for i in range(0, len(musics)):

        if namespace.log: print("processing file:" + musics[i])

        if namespace.frame != None:
            listCutTrack.append(
                ffmpeg.input(os.path.abspath(dir + '\\' + musics[i])).audio.filter('atrim', duration=namespace.frame))
        else:
            listCutTrack.append(
                ffmpeg.input(os.path.abspath(dir + '\\' + musics[i])).audio.filter('atrim', duration=10))

        if namespace.count != None:
            j += 1
            if j == int(namespace.count): break

if len(listCutTrack) > 1:
    concatted = listCutTrack[0]
    for i in range(1, len(listCutTrack)):
        concatted = ffmpeg.concat(concatted, listCutTrack[i], a=1, v=0)

    if namespace.extended:
        ffmpeg.output(concatted, 'intermediated.mp3').run()
        probe = ffmpeg.probe('intermediated.mp3')
        os.remove('intermediated.mp3')
        track = next(stream for stream in probe['streams'])
        concatted = concatted.filter('afade', type='in', start_time=0, duration=10).filter('afade', type='out', start_time=float(track['duration']) - 10, duration=10)

    if namespace.destination != None:
        ffmpeg.output(concatted, namespace.destination).run()
    else:
        ffmpeg.output(concatted, 'mix.mp3').run()