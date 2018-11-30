# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 21:44:53 2018
"""
import re
import matplotlib.pyplot as plt
import pandas as pd
import statistics
import operator
import datetime
import utilityFunctions
import plotMM
import plotCM
import plotMD
import plotReactTotal
import emoji

plt.rcParams["font.family"] = "Times New Roman"

expectedFormat = re.compile(r"([A-z]+)\s([0-9]+),\s([0-9]{4})",re.MULTILINE)
masterCheck = re.compile(r'(<div class="_3-96 _2pio _2lek _2lel">)(.*?)(<\/div><div class="_3-96 _2let"><div><div><\/div><div>)(.*?)(<\/div>)(.*?)(<div class="_3-94 _2lem">)(.*?)(<\/div>)',re.MULTILINE)
newMaster = re.compile(r'(<div class="_3-96 _2pio _2lek _2lel">)(.*?)(<\/div><div class="_3-96 _2let"><div><div><\/div><div>)(.*?)(<\/div>)(.*?)(<div class="_3-94 _2lem">)([A-z]+)\s([0-9]+),\s([0-9]{4})\s([0-9]+):([0-9]+)([a-z]{2})(<\/div>)',re.MULTILINE)
reactCheck = re.compile(r'(<li>)(.*?)([A-z]+.*?)(<\/li>)',re.MULTILINE)


# Read the file
text = ''
for line in open("..\\FacebookData\\message.txt", "r", encoding='utf-8'):
    text += line


masterData = masterCheck.findall(text)
data = newMaster.findall(text)
reacts = reactCheck.findall(text)

emojis = {}
for entry in reacts:
    new = emoji.demojize(entry[1])
    if emojis.get(new) == None:
        emojis[new] = 1 
    else:
        emojis[new] = emojis[new]+1

sortedEmoji = sorted(emojis.items(), key=operator.itemgetter(1))    
plotReactTotal.plotReactTotal(sortedEmoji)

# Loop through masterData
MsgNames = {}
Days = {}
CharNames = {}
for entry in masterData:
    datetime_object = datetime.datetime.strptime(entry[7], '%b %d, %Y %I:%M%p')
    dayOfWeek = datetime_object.strftime("%A")
    if MsgNames.get(entry[1]) == None:
        MsgNames[entry[1]] = 1
    else:
        MsgNames[entry[1]] = MsgNames[entry[1]]+1
    if Days.get(dayOfWeek) == None:
        Days[dayOfWeek] = 1
    else:
        Days[dayOfWeek] = Days[dayOfWeek]+1
    # 
    if CharNames.get(entry[1]) == None:
        CharNames[entry[1]] = len(entry[3])
    else:
        CharNames[entry[1]] = CharNames[entry[1]]+len(entry[3])

sortedMsgNames = sorted(MsgNames.items(), key=operator.itemgetter(1))
sortedCharNames = sorted(CharNames.items(), key=operator.itemgetter(1))

newDays={}
for k, v in Days.items():
    number = utilityFunctions.switchDay(k)
    newDays[number] = v

sortedDays = sorted(newDays.items(), key=operator.itemgetter(0))

switchBackDays=list()
n = 0
for k in sortedDays:
    switchBackDays.append([utilityFunctions.switchBackDay(k[0]),k[1]])
    n = n+1

# Print number of messages sent by each member
plotMM.plotMM(sortedMsgNames)

# Print number of characters sent by each member
plotCM.plotCM(sortedCharNames)

# Print number of messages sent by day of the week
plotMD.plotMD(switchBackDays)

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
    year = item[9]
    formattedEntry = month+'-'+str(day)+'-'+str(year)

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
plt.title("A measure of ??????'s contributions to the chat", fontsize=18)

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
