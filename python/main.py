import random
import numpy as np
import math

# Size of the network and the array it is stored in
networksize = 100
maximumDegree = 0

edgeArray = np.zeros((networksize, networksize), dtype=int)
neighbors = np.zeros((networksize, networksize), dtype=int)
degrees = np.zeros(networksize, dtype=int)
payoffs = np.zeros(networksize, dtype=int)
players = [random.random() for q in range(networksize)]


# Check that the elements of a given array are distinct
def aredistinct(x: list) -> bool:
    f = True
    for p in range(len(x)):
        for q in range(p + 1, len(x)):
            if x[p] == x[q]:
                f = False
    return f


# Sample an array index, where array elements are probabilities
def findinlist(arr: list, n: int) -> int:
    i = 0
    while n > arr[i]:
        n -= arr[i]
        i += 1
    return i


# Generate a Barabasi—Albert graph
def barabalbert(size: int):
    for i in range(4):  # start with a complete graph on 4 vertices
        for j in range(i):
            edgeArray[i][j] = 1
            edgeArray[j][i] = 1
        degrees[i] = 3

    for i in range(4, size):  # add the following vertices
        idegrees = degrees[0:i]  # array of the degrees of all the previous vertices
        isum = 8 * i - 20  # sum of degrees of existing vertices (math!..)
        chosenvert = [0 for p in range(4)]
        changedvert = [0 for p in range(4)]
        while not (aredistinct(changedvert)):  # check there are no double connections
            for p in range(4):
                chosenvert[p] = random.randint(1, isum)  # sample a number
                changedvert[p] = \
                    findinlist(idegrees, chosenvert[p])  # convert it into index
        degrees[i] += 4
        for p in range(4):
            edgeArray[i][changedvert[p]] = 1
            edgeArray[changedvert[p]][i] = 1
            degrees[changedvert[p]] += 1


# Return 0 with probability p
def sample(p: float) -> int:
    x = random.random()
    if x <= p:
        return 0
    else:
        return 1


# Yield—go game
def game(p, q: float) -> tuple:
    allgames += 1
    a = sample(p)
    b = sample(q)
    if a == 0 and b == 0:  # yield=0, go=1
        yields += 1
        return -1, -1
    elif a == 0 and b == 1:
        yields += 1
        return 1, 2
    elif a == 1 and b == 0:
        yields += 1
        return 2, 1
    elif a == 0 and b == 0:
        return -8, -8


# Compress list of neighbors, so it's linear size:
# Convert 1's for edges to the list of the numbers of adjacent vertices
def compressneighbors():
    for i in range(networksize):
        k = 0
        for j in range(networksize):
            if edgeArray[i][j] == 1:
                neighbors[i][k] = j
                k += 1  # in the end k==degrees[i]


def main():
    print("draw (0,4) -- (12,4)")

    barabalbert(networksize)

    compressneighbors()

    steps = 0

    # make sure the system does not change AND stays in this state for long enough
    while (steps < 300):
        allgames = 0
        yields = 0

        for i in range(networksize):
            payoffs[i] = sum([game(players[i], players[neighbors[i][j]])[0]
                              for j in range(degrees[i])])

            if degrees[i] != 0:  # there can be empty vertices, then the randomizer fails
                j = random.randint(0, degrees[i] - 1)
                jindex = neighbors[i][j]
                if edgeArray[i][jindex] == 0:
                    print("fubar")
                if payoffs[jindex] > payoffs[i]:
                    players[i] += (players[jindex] - players[i]) * \
                                  (payoffs[jindex] - payoffs[i]) / \
                                  (max(degrees[i], degrees[jindex]))

        yieldDose = yields / allgames
        print("-- (0.016 * ", steps, " cm, 4 * ", yieldDose, " cm)")

    print(";")


main()
