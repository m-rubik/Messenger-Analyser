###############################################################################
## This loads message.txt data, parses through it and plots various information
###############################################################################

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
import plotContributions

import plotReactTotal
import emoji

if __name__ == "__main__":

    plt.rcParams["font.family"] = "Times New Roman"

    expectedFormat = re.compile(r"([A-z]+)\s([0-9]+),\s([0-9]{4})",re.MULTILINE)
    masterCheck = re.compile(r'(<div class="_3-96 _2pio _2lek _2lel">)(.*?)(<\/div><div class="_3-96 _2let"><div><div><\/div><div>)(.*?)(<\/div>)(.*?)(<div class="_3-94 _2lem">)(.*?)(<\/div>)',re.MULTILINE)
    # newMaster = re.compile(r'(<div class="_3-96 _2pio _2lek _2lel">)(.*?)(<\/div><div class="_3-96 _2let"><div><div><\/div><div>)(.*?)(<\/div>)(.*?)(<div class="_3-94 _2lem">)([A-z]+)\s([0-9]+),\s([0-9]{4})\s([0-9]+):([0-9]+)([a-z]{2})(<\/div>)',re.MULTILINE)
    newMaster = re.compile(r'(<div class=\"_3-96 _2pio _2lek _2lel\">)(.*?)(<\/div><div class=\"_3-96 _2let\"><div><div><\/div><div>)(.*?)(<\/div>)(.*?)(<div class=\"_3-94 _2lem\">)([A-z]+)\s([0-9]+),\s([0-9]{4}),\s([0-9]+):([0-9]+)\s([A-z]{2})(<\/div>)',re.MULTILINE)
    reactCheck = re.compile(r'(<li>)(.*?)([A-z]+.*?)(<\/li>)',re.MULTILINE)

    ## Read the messages file
    text = ''
    for line in open("..\\FacebookData\\message.txt", "r", encoding='utf-8'):
        text += line
    print("Messages loaded.")

    ## Regex to find individual messages
    masterData = masterCheck.findall(text)
    print("Found master data.")
    data = newMaster.findall(text)
    print("Found new master data.")
    reacts = reactCheck.findall(text)
    print("Found all react data.")

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
        datetime_object = datetime.datetime.strptime(entry[7], '%b %d, %Y, %I:%M %p')
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

    ## Plot number of messages sent by each member
    plotMM.plotMM(sortedMsgNames)

    ## Plot number of characters sent by each member
    plotCM.plotCM(sortedCharNames)

    ## Plot number of messages sent by day of the week
    plotMD.plotMD(switchBackDays)

    ## Plot contributions made by a certain group member, or by "All"
    plotContributions.plotContributions(data,"Gabriel Risbud-Vincent")
