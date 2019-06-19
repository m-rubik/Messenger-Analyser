#################################################################################
## Plots the usage of each reaction
################################################################################# 

import matplotlib.pyplot as plt
import matplotlib

def plotReactTotal(data):
    x, y = zip(*data)
    plt.figure(5) 
    ax = plt.gca()
    ax.bar(x,y)
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    ax.set_ylabel('Number of times sent', fontsize=18)
    plt.title('Which reacts are used?', fontsize=18)
    plt.show()