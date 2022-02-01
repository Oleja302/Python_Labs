def pre_process(a):
    def decorator(plot_signal):
        def wrap(s):
            for i in range(0, len(s)):
                s[i] = round(s[i] - a * s[i - 1], 3)
            plot_signal(s)

        return wrap
    return decorator


@pre_process(a=0.97)
def plot_signal(s):
    for sample in s:
        print(sample)


s = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
plot_signal(s)
