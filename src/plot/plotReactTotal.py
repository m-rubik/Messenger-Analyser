"""!
Plots the usage of reaction emojis
"""


import matplotlib.pyplot as plt

def plotReactTotal(data):
    x, y = zip(*data)
    plt.figure(5)
    ax = plt.gca()
    ax.bar(x, y)
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    ax.set_ylabel('Number of times sent', fontsize=18)
    plt.title('Which reacts are used?', fontsize=18)
    plt.show()
