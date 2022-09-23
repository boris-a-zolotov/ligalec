import random
import numpy as np
import math

# Size of the network and the array it is stored in
networksize = 10000
edgeArray = [[0 for p in range(networksize)] for q in range(networksize)]
degrees = [0 for p in range(networksize)]


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
    a = sample(p)
    b = sample(q)
    if a == 0 and b == 0:  # yield=0, go=1
        return -1, -1
    elif a == 0 and b == 1:
        return 1, 2
    elif a == 1 and b == 0:
        return 2, 1
    elif a == 0 and b == 0:
        return -8, -8


def main():
    barabalbert(networksize)

    dmax = max(t, 1) - min(0, -0.1)  # constant in the denominator
    neighbors = [[0 for p in range(networksize)] for q in range(networksize)]
    players = [random.randint(0, 1) for q in range(networksize)]
    payoffs = [0 for p in range(networksize)]  # NEW: total payoffs of all players

    for i in range(networksize):  # compress list of neighbors so it's linear size
        k = 0
        for j in range(networksize):
            if edgeArray[i][j] == 1:
                neighbors[i][k] = j
                k += 1  # in the end k==degrees[i]

    # initialize description of system progress
    saveddose = 2
    dose = 1
    steps = 0
    totalsteps = 0

    # make sure the system does not change AND stays in this state for long enough
    while (abs(saveddose - dose) > stabdose) or (steps < 25):
        totalsteps += 1
        saveddose = dose

        for i in range(networksize):
            payoffs[i] = sum([game(players[i], players[neighbors[i][j]])[0]
                              for j in range(degrees[i])])
            # payoff is the sum, important: neighbor

            if degrees[i] != 0:  # there can be empty vertices, then the randomizer fails
                j = random.randint(0, degrees[i] - 1)
                jindex = neighbors[i][j]
                if edgeArray[i][jindex] == 0:
                    print("fubar")
                probij = (payoffs[jindex] - payoffs[i]) / (dmax * max(degrees[i], degrees[jindex]))
                # formula from the assignment
                isample = sample(probij)
                if isample == 1:
                    savedplay = players[i]
                    players[i] = 1 - players[i]

        dose = sum(players) / networksize  # calculations regarding the stability of the system
        if saveddose - dose <= stabdose:
            steps += 1
        else:
            steps = 0
        # print(saveddose, dose, steps)
    print(totalsteps, dose)


main()
