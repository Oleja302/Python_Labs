def get_frames(signal, size, overlap):
    for i in range(0, len(signal), int(size * overlap)):
        yield signal[i: i + size]


signal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for frame in get_frames(signal, 4, 0.5):
    print(frame)
