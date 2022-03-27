import struct
import argparse
import os

# py 1.py -s "D:\Programming\Python\Python_Labs\Lab_4\"

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', required=True)
parser.add_argument('-d', '--demp', action='store_const', const=True, default=False)
parser.add_argument('-g', '--genre')
namespace = parser.parse_args()

number = 1
for address, dirs, files in os.walk(namespace.source):
    for music in files:

        if '.mp3' in music:
            musAddress = address + '\\' + music

            with open(musAddress, "rb") as fileRead:
                # Read last 3 byte
                fileRead.seek(-3, 2)
                zeroByte = int.from_bytes(fileRead.read(1), 'big')
                fileRead.read(1)
                genreByte = int.from_bytes(fileRead.read(1), 'big')
                fileRead.seek(0)
                dataAllFile = fileRead.read()

                # Write data
                with open(musAddress, "wb") as fileWrite:
                    fileWrite.write(dataAllFile)

                    # Set number
                    if zeroByte != 0:
                        fileWrite.seek(-3, 2)
                        fileWrite.write(b'\x00')
                        fileWrite.write(struct.pack('B', number))
                        number += 1

                    # Set genre
                    if namespace.genre != None and genreByte == 255:
                        fileWrite.seek(-1, 2)
                        fileWrite.write(struct.pack('B', int(namespace.genre)))

                # Read 128 byte tag
                fileRead.seek(-128, 2)
                dataTag = fileRead.read(128)

            # Decode and print tag
            unpacked = struct.unpack('3s 30s 30s 30s 4s 28s B B B', dataTag)

            result = ''
            for i in range(1, 4):
                result += '[' + unpacked[i].decode().replace('\0', '') + ']'
                if i != 3:
                    result += ' - '

            print(result)

            # Print demp tag
            if namespace.demp:
                for tag in unpacked:
                    print(tag)
