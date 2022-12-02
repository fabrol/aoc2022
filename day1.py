import numpy as np
with open('day1.in') as fp:
    res = fp.read().split("\n\n")
    cals = np.array(
        list(map(lambda x: sum(list(map(int, x.split('\n')))), res)))
    # print(cals[cals.argmax()])
    print(sum(sorted(cals, reverse=True)[0:3]))
