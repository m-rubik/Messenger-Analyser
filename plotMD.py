import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"

def plotMD(data):
    x, y = zip(*data)
    plt.figure(3) 
    ax = plt.gca()
    ax.bar(x,y)
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    ax.set_ylabel('Number of messages sent', fontsize=18)
    plt.title('Number of messages sent by day of the week', fontsize=18)
    plt.show()