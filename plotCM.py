import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"

def plotCM(data):
    x, y = zip(*data)
    plt.figure(2) 
    ax = plt.gca()
    barplot = ax.bar(x,y)
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    ax.set_ylabel('Number of characters sent', fontsize=18)
    barplot[9].set_color('y')
    barplot[8].set_color('g')
    barplot[7].set_color('b')
    barplot[4].set_color('r')
    barplot[3].set_color('r')
    barplot[2].set_color('r')
    barplot[1].set_color('r')
    barplot[0].set_color('r')
    plt.title('Number of characters sent by group member', fontsize=18)
    plt.show()