def switchMonth(month):
    switcher = {
        "Jan": '01',
        "Feb": '02',
        "Mar": '03',
        "Apr": '04',
        "May": '05',
        "Jun": '06',
        "Jul": '07',
        "Aug": '08',
        "Sep": '09',
        "Oct": '10',
        "Nov": '11',
        "Dec": '12'
    }
    return switcher.get(month, "Invalid")


def switchDay(day):
    switcher = {
        "Monday": '0',
        "Tuesday": '1',
        "Wednesday": '2',
        "Thursday": '3',
        "Friday": '4',
        "Saturday": '5',
        "Sunday": '6'
    }
    return switcher.get(day, "Invalid")


def switchBackDay(number):
    switcher = {
        '0': "Monday",
        '1': "Tuesday",
        '2': "Wednesday",
        '3': "Thursday",
        '4': "Friday",
        '5': "Saturday",
        '6': "Sunday"
    }
    return switcher.get(number, "Invalid")
