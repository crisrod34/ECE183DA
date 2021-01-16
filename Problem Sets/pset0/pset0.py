import numpy as np
import matplotlib.pyplot as plt

def seqSim(biased, numFlips):
    seq = []
    pHeads = 0
    if biased:
        pHeads = 0.25
    else:
        pHeads = 0.75

    pBiased = 0
    flips = 0
    biasProbs = []
    while (numFlips > 0):
        r = np.random.rand()
        if r <= pHeads:
            seq.append("H")
        else:
            seq.append("T")
        flips += 1

        numH = seq.count("H")
        numT = seq.count("T")

        pBiased = (np.power(0.75, numT) * np.power(0.25, numH) * 0.25)/((np.power(0.75, numT) * np.power(0.25, numH) + np.power(0.5, flips))/2)
        biasProbs.append(pBiased)
        numFlips -= 1

    return(biasProbs)


fairSim1 = seqSim(False, 100)
fairSim2 = seqSim(False, 100)
fairSim3 = seqSim(False, 100)
fairSim4 = seqSim(False, 100)
fairSim5 = seqSim(False, 100)

biasSim1 = seqSim(True, 100)
biasSim2 = seqSim(True, 100)
biasSim3 = seqSim(True, 100)
biasSim4 = seqSim(True, 100)
biasSim5 = seqSim(True, 100)

x = range(100)
plt.figure()
plt.plot(x, fairSim1)
plt.plot(x, fairSim2)
plt.plot(x, fairSim3)
plt.plot(x, fairSim4)
plt.plot(x, fairSim5)
plt.xlabel('Number of Flips')
plt.ylabel('Probability of Biased Coin Picked')
plt.title('Probability of Biased Coin Picked using a Fair Coin')
plt.show()

plt.figure()
plt.plot(x, biasSim1)
plt.plot(x, biasSim2)
plt.plot(x, biasSim3)
plt.plot(x, biasSim4)
plt.plot(x, biasSim5)
plt.xlabel('Number of Flips')
plt.ylabel('Probability of Biased Coin Picked')
plt.title('Probability of Biased Coin Picked using a Biased Coin')
plt.show()