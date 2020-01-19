"""!
Plots the number of messages sent by each member
"""


import matplotlib.pyplot as plt

def plotMM(data):
    x, y = zip(*data)
    plt.figure(1)
    ax = plt.gca()
    ax.bar(x, y)
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    ax.set_ylabel('Number of messages sent', fontsize=18)
    plt.title('Number of messages sent by each group member', fontsize=18)
    plt.show()
