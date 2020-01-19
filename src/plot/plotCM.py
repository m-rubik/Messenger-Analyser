"""!
Plot the number of characters sent by each group member
"""

import matplotlib.pyplot as plt

def plotCM(data):
    x, y = zip(*data)
    plt.figure(2)
    ax = plt.gca()
    barplot = ax.bar(x, y)
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    ax.set_ylabel('Number of characters sent', fontsize=18)
    y_max = max(y)
    y_medTier = round(y_max*(2/3))
    for each_bar in barplot:
        if each_bar._y1 == y_max:
            each_bar.set_color('yellow')
        elif each_bar._y1 >= y_medTier:
            each_bar.set_color('orange')
        else:
            each_bar.set_color("red")
    plt.title('Number of characters sent by group member', fontsize=18)
    plt.show()
