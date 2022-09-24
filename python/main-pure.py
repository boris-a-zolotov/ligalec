import random
import numpy as np

# Size of the network and the array it is stored in
networksize = 800
maximumDegree = 0
totalsteps = 1100
gamerepetitions = 13

damage = 11
noiseprob = 1 / 160

edgeArray = np.full((networksize, networksize), False, dtype=bool)
neighbors = np.zeros((networksize, networksize), dtype=int)
degrees = np.zeros(networksize, dtype=int)
gameres = np.zeros((totalsteps, gamerepetitions))


# Check that the elements of a given array are distinct
def aredistinct(x: np.ndarray) -> bool:
    return len(set(x)) == len(x)


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
def game(p, q: int) -> tuple:
    if p == 0 and q == 0:  # yield=0, go=1
        return -1, -1
    elif p == 0 and q == 1:
        return 1, 2
    elif p == 1 and q == 0:
        return 2, 1
    elif p == 1 and q == 1:
        return -damage, -damage


def main():
    global totalsteps

    barabalbert(networksize)

    compressneighbors()

    projectednash = (damage + 1) / (damage + 4)

    for repet in range(gamerepetitions):
        print(repet, end=" ")
        steps = 0
        players = [random.randint(0, 1) for q in range(networksize)]

        while steps < totalsteps:
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
                    if payoffs[jindex] > payoffs[i]:
                        switchprob = (payoffs[jindex] - payoffs[i]) / \
                                     (max(degrees[i], degrees[jindex])) / \
                                     (damage + 2)
                        if sample(switchprob) == 0:
                            players[i] = players[jindex]

            gameres[steps][repet] = 1 - sum(players) / networksize

            steps += 1

    ydstring = "\n\n\\begin{tikzpicture}\n\\draw (0,4) -- (12,4) (12,4 * %f) -- (0,4 * %f) (12,0) -- (0,0)" % (
        projectednash, projectednash)

    for s in range(totalsteps):
        xcoord = 12 / totalsteps * s
        ycoord = 4 * np.average(gameres[s])
        ydstring += "-- (%f, %f) " % (xcoord, ycoord)

    ydstring += ";\n\\end{tikzpicture}\n"

    print(ydstring)
    print("")


main()
