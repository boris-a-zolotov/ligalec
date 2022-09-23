import random
import numpy as np
import math


def aredistinct(x: list) -> bool:
    f = True
    for p in range(len(x)):
        for q in range(p + 1, len(x)):
            if x[p] == x[q]:
                f = False
    return f


def findinlist(arr: list, n: int) -> int:
    i = 0
    while n > arr[i]:
        n -= arr[i]
        i += 1
    return i


def main():
    networksize = 10000
    edgar = [[0 for p in range(networksize)] for q in range(networksize)]
    degrees = [0 for p in range(networksize)]

    for i in range(4):  # start with a complete graph on 4 vertices
        for j in range(i):
            edgar[i][j] = 1
            edgar[j][i] = 1
        degrees[i] = 3

    for i in range(4, networksize):
        idegrees = degrees[0:i]
        isum = 8 * i - 20
        chosenvert = [0 for p in range(4)]
        changedvert = [0 for p in range(4)]
        while not (aredistinct(changedvert)):  # check there are no double connections
            for p in range(4):
                chosenvert[p] = random.randint(1, isum)  # sample a number
                changedvert[p] = findinlist(idegrees, chosenvert[p])  # convert it into index
        degrees[i] += 4
        for p in range(4):
            edgar[i][changedvert[p]] = 1
            edgar[changedvert[p]][i] = 1
            degrees[changedvert[p]] += 1

    networkmean = np.mean(degrees)
    networkdevia = np.std(degrees)

    print(networkmean, networkdevia)

    histogram = [0 for q in range(networksize)]

    for q in range(networksize):
        histogram[degrees[q]] += 1

    histogram = histogram[4:networksize]  # crop zeros from histogram

    cycl = 0

    # determine where there are significant number of vertices,
    # we don't want to plot 10000 points
    while histogram[cycl] > 4 and histogram[cycl + 1] > 4:
        print("(", cycl, " * 0.33 cm,", histogram[cycl], "* 0.002 cm) --", end=' ')
        cycl += 1

    loghistogram = [math.log(histogram[p]) for p in range(cycl)]  # log points
    logscale = [math.log(p + 4) for p in range(cycl)]  # shifted log scale

    print(" ")

    # plot logged points in tikz
    for i in range(cycl):
        print("(", logscale[i], ",", loghistogram[i], ") --", end=' ')

    fitted = np.polyfit(logscale, loghistogram, 1)

    print(" ")

    # plot fitted line in tikz
    print("\\draw[domain =", logscale[0], ":", logscale[cycl - 1], ", smooth, variable = \\x]",
          "plot({\\x}, {", fitted[0], "* \\x +", fitted[1], "});")


main()
