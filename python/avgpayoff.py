avgpayoffi = payoffs[i] / degrees[i]
avgpayoffj = payoffs[j] / degrees[j]
if avgpayoffj > avgpayoffi:
    players[i] += (players[jindex] - players[i]) * \
                  (avgpayoffj - avgpayoffi) / \
                  (damage + 2)
