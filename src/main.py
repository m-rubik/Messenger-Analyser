"""!
Contains functions required for loading facebook messenger data from message.txt.
message.txt is essentially the .txt version of the html provided by facebook for a certain messenger conversation.
"""

import os
import re
import operator
import datetime
import emoji
import src.utilities as utilities
import plot.plotMM as plotMM
import plot.plotCM as plotCM
import plot.plotMD as plotMD
import plot.plotContributions as plotContributions
import plot.plotReactTotal as plotReactTotal
import matplotlib.pyplot as plt


plt.rcParams["font.family"] = "Times New Roman"
plt.style.use('ggplot')


def load_data():
    '''This functions loads all the messages from the provided file'''

    master_check = re.compile(
        r'(<div class=\"_3-96 _2pio _2lek _2lel\">)(.*?)(<\/div><div class=\"_3-96 _2let\"><div><div><\/div><div>)(.*?)(<\/div>)(.*?)(<div class=\"_3-94 _2lem\">)([A-z]+)\s([0-9]+),\s([0-9]{4}),\s([0-9]+):([0-9]+)\s([A-z]{2})(<\/div>)', re.MULTILINE)
    react_check = re.compile(r'(<li>)(.*?)([A-z]+.*?)(<\/li>)', re.MULTILINE)

    # Read the messages file
    text = ''
    for line in open(os.path.join(os.path.realpath('.'), "src", "data", "message.txt"), "r", encoding='utf-8'):
        text = text.join(line)
    print("Messages loaded.")

    # Regex to find individual messages
    found_data = master_check.findall(text)
    print("Found new master data.")
    found_reacts = react_check.findall(text)
    print("Found all react data.")

    return found_data, found_reacts


def parse_data(input_data, input_reacts):

    emojis = {}
    for entry in input_reacts:
        new = emoji.demojize(entry[1])
        if emojis.get(new) is None:
            emojis[new] = 1
        else:
            emojis[new] = emojis[new]+1

    sortedEmoji = sorted(emojis.items(), key=operator.itemgetter(1))
    plotReactTotal.plotReactTotal(sortedEmoji)

    # Loop through masterData
    MsgNames = {}
    Days = {}
    CharNames = {}
    for entry in input_data:
        datetime_string = "{0} {1}, {2}, {3}:{4} {5}".format(
            entry[7], entry[8], entry[9], entry[10], entry[11], entry[12])
        datetime_object = datetime.datetime.strptime(
            datetime_string, '%b %d, %Y, %I:%M %p')
        dayOfWeek = datetime_object.strftime("%A")
        if MsgNames.get(entry[1]) is None:
            MsgNames[entry[1]] = 1
        else:
            MsgNames[entry[1]] = MsgNames[entry[1]]+1
        if Days.get(dayOfWeek) is None:
            Days[dayOfWeek] = 1
        else:
            Days[dayOfWeek] = Days[dayOfWeek]+1
        if CharNames.get(entry[1]) is None:
            CharNames[entry[1]] = len(entry[3])
        else:
            CharNames[entry[1]] = CharNames[entry[1]]+len(entry[3])

    sortedMsgNames = sorted(MsgNames.items(), key=operator.itemgetter(1))
    sortedCharNames = sorted(CharNames.items(), key=operator.itemgetter(1))

    newDays = {}
    for k, v in Days.items():
        number = utilities.switchDay(k)
        newDays[number] = v

    sortedDays = sorted(newDays.items(), key=operator.itemgetter(0))

    switchBackDays = list()
    n = 0
    for k in sortedDays:
        switchBackDays.append([utilities.switchBackDay(k[0]), k[1]])
        n = n+1

    return sortedMsgNames, sortedCharNames, switchBackDays


if __name__ == "__main__":

    data, reacts = load_data()

    SORTED_MESSAGES_BY_NAME, SORTED_CHARACTERS_BY_NAME, SWITCHBACK_DAYS = parse_data(
        data, reacts)

    ## Plot number of messages sent by each member
    plotMM.plotMM(SORTED_MESSAGES_BY_NAME)

    ## Plot number of characters sent by each member
    plotCM.plotCM(SORTED_CHARACTERS_BY_NAME)

    ## Plot number of messages sent by day of the week
    plotMD.plotMD(SWITCHBACK_DAYS)

    ## Plot contributions made by a group member's name, or by "All"
    plotContributions.plotContributions(data, "All")
