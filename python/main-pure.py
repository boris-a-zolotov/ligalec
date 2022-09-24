import random
import numpy as np
import math

# Size of the network and the array it is stored in
networksize = 6400
maximumDegree = 0
allgames = 0
yields = 0
totalsteps = 500
steps = 0
damage = 11
noiseprob = 1 / 160

edgeArray = np.full((networksize, networksize), False, dtype=bool)
neighbors = np.zeros((networksize, networksize), dtype=int)
degrees = np.zeros(networksize, dtype=int)
players = [random.random() for q in range(networksize)]


# Check that the elements of a given array are distinct
def aredistinct(x: np.ndarray) -> bool:
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
            edgeArray[i][j] = True
            edgeArray[j][i] = True
        degrees[i] = 3

    for i in range(4, size):  # add the following vertices
        idegrees = degrees[0:i]  # array of the degrees of all the previous vertices
        isum = 8 * i - 20  # sum of degrees of existing vertices (math!..)
        chosenvert = np.zeros(4, dtype=int)
        changedvert = np.zeros(4, dtype=int)
        while not (aredistinct(changedvert)):  # check there are no double connections
            for p in range(4):
                chosenvert[p] = random.randint(1, isum)  # sample a number
                changedvert[p] = \
                    findinlist(idegrees, chosenvert[p])  # convert it into index
        degrees[i] += 4
        for p in range(4):
            edgeArray[i][changedvert[p]] = True
            edgeArray[changedvert[p]][i] = True
            degrees[changedvert[p]] += 1


# Return 0 with probability p
def sample(p: float) -> int:
    x = random.random()
    if x <= p:
        return 0
    else:
        return 1


# Compress list of neighbors, so it's linear size:
# Convert 1's for edges to the list of the numbers of adjacent vertices
def compressneighbors():
    for i in range(networksize):
        k = 0
        for j in range(networksize):
            if edgeArray[i][j]:
                neighbors[i][k] = j
                k += 1  # in the end k==degrees[i]


def locate(query, owner: int):
    global neighbors
    for p in range(degrees[owner]):
        if neighbors[owner][p] == query:
            return p


# Yield—go game
def game(p, q: float) -> tuple:
    global allgames
    global yields

    allgames += 2
    a = sample(p)
    b = sample(q)

    if a == 0 and b == 0:  # yield=0, go=1
        yields += 2
        return -1, -1
    elif a == 0 and b == 1:
        yields += 1
        return 1, 2
    elif a == 1 and b == 0:
        yields += 1
        return 2, 1
    elif a == 1 and b == 1:
        return -damage, -damage


def histogram(arr: list, cols: int):
    hists = np.zeros(cols, dtype=int)

    for p in range(len(arr)):
        hists[math.floor(arr[p] * cols)] += 1

    hmax = np.max(hists)
    xstep = 12 / cols

    print("\n\\begin{tikzpicture}")
    for p in range(cols):
        xhcoord = 12 / cols * p
        yhcoord = 4 * hists[p] / hmax
        print("\\fill[red] (", xhcoord, ", 0) rectangle ++(", xstep, ", ", yhcoord, "); ", sep="", end="")
    print("\n\\end{tikzpicture}\n")


def main():
    global allgames
    global yields
    global totalsteps
    global steps

    barabalbert(networksize)

    compressneighbors()

    projectednash = (damage + 1) / (damage + 4)

    ydstring = "\n\\begin{tikzpicture}\n\\draw (0,4) -- (12,4) (12,4 * %f) -- (0,4 * %f) (12,0) -- (0,0)" % (
        projectednash, projectednash)

    # make sure the system does not change AND stays in this state for long enough
    while steps < totalsteps:
        allgames = 0
        yields = 0

        haveplayedarray = np.full((networksize, networksize), False, dtype=bool)
        payoffs = np.zeros(networksize)

        for i in range(networksize):
            for j in range(degrees[i]):
                if not haveplayedarray[i][j]:
                    jindex = neighbors[i][j]
                    ijplay = game(players[i], players[jindex])
                    payoffs[i] += ijplay[0]
                    payoffs[jindex] += ijplay[1]
                    haveplayedarray[i][j] = True
                    haveplayedarray[jindex][locate(i, jindex)] = True

        for i in range(networksize):
            if degrees[i] != 0:  # there can be empty vertices, then the randomizer fails
                j = random.randint(0, degrees[i] - 1)
                jindex = neighbors[i][j]
                if sample(noiseprob) == 0:
                    players[i] = projectednash + 0.4 * (random.random() - 0.5)
                else:
                    if payoffs[jindex] > payoffs[i]:
                        players[i] += (players[jindex] - players[i]) * \
                                      (payoffs[jindex] - payoffs[i]) / \
                                      (max(degrees[i], degrees[jindex])) / \
                                      (damage + 2)
                        if players[i] > 1 or players[i] < 0:
                            print("FAIL", payoffs[i], payoffs[jindex], degrees[i], degrees[jindex])

        yielddose = yields / allgames
        xcoord = 12 / totalsteps * steps
        ycoord = 4 * yielddose

        ydstring += "-- (%f, %f) " % (xcoord, ycoord)

        if steps % (totalsteps // 5) == 0:
            histogram(players, 263)

        steps += 1

    ydstring += ";\n\\end{tikzpicture}\n"

    print(ydstring)
    print("")


main()
