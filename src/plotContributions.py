import utilityFunctions
import pandas as pd
import statistics
import matplotlib.pyplot as plt

def plotContributions(data,member):
    ### ANALYSE MESSAGES BY DATE ### 
    firstMonth = utilityFunctions.switchMonth(data[len(data)-1][7])
    firstDay = data[len(data)-1][8]
    firstYear = data[len(data)-1][9]

    endMonth = utilityFunctions.switchMonth(data[0][7])
    endDay = data[0][8]
    endYear = data[0][9]

    startDate = firstMonth+'/'+str(firstDay)+'/'+str(firstYear)
    endDate = endMonth+'/'+str(endDay)+'/'+str(endYear)

    dates = pd.date_range(start=startDate, end=endDate).tolist()

    dateList = list()
    for ts in dates:
        dateList.append(ts.strftime('%m-%d-%Y'))
        ts.strftime("")

    messageCount = [0] * len(dateList)

    totalMessages = 0
    for item in data:
        month = utilityFunctions.switchMonth(item[7])
        if month == 'Invalid':
            continue
        day = item[8]
        if len(day) == 1:
            day = '0'+day
        year = item[9]
        formattedEntry = month+'-'+str(day)+'-'+str(year)
        if member == "All" or item[1] == member:
            messageCount[dateList.index(formattedEntry)] = messageCount[dateList.index(formattedEntry)]+1
        totalMessages = totalMessages+1

    average = statistics.mean(messageCount)
    zeroDays = messageCount.count(0)
    daysSinceStart = len(dateList)
    oddsOn = (1 - (zeroDays/daysSinceStart)) *100

    textstr = '\n'.join((
        r'Days since start: %d' % (daysSinceStart, ),
        r'Total messages: %d' % (totalMessages, ),
        r'Average number of messages per day: %d' % (average, ),
        r'Days with no messages: %d' % (zeroDays, ),
        r'Chance of at least 1 message on any day: %d%%' % (oddsOn, ),
        ))

    # Print number of messages by date
    plt.figure(4) 
    plt.plot(messageCount,'r')

    if member == "All":
        plt.title("A measure of how lit this chat is", fontsize=18)
    else:
        plt.title("A measure of {}'s contributions to the chat".format(member), fontsize=18)

    locs, labels = plt.xticks()           # Get locations and labels
    plt.xticks([0,len(messageCount)], [startDate,endDate])  # Set locations and labels

    ax = plt.gca()
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Number of messages', fontsize=18)
    ax.annotate('Max: '+str(max(messageCount)), xy=(messageCount.index(max(messageCount)), max(messageCount)), xytext=(messageCount.index(max(messageCount))+(len(messageCount)/10), max(messageCount)),
        arrowprops=dict(arrowstyle="->", linewidth=1),
        fontsize = 18
        )

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.6, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    plt.show()