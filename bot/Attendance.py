import csv
import os
import Firebase
gbmAttendance = {}
eventAttendance = {}
totalGBMs = 0
# Already collected UCIDs in Firebase.py, so using that, will assign 0s to GBM and attendance
for user in Firebase.discordUsers:
    gbmAttendance[user]=0
    eventAttendance[user]=0
def updateEventAttendance(filename):
    f = open(filename, 'r')
    reader = csv.reader(f)
    csvList = list(reader)
    usefulList = csvList[6:len(csvList)]
    for aList in usefulList:
        ucid = aList[2]
        endIndex = ucid.index('@')
        if ucid[0:endIndex] in eventAttendance:
            eventAttendance[ucid[0:endIndex]] += 1
    f.close()
    return
def updateGBMAttendance(filename):
    global totalGBMs
    totalGBMs +=1
    f = open(filename, 'r')
    reader = csv.reader(f)
    csvList = list(reader)
    usefulList = csvList[6:len(csvList)]
    for aList in usefulList:
        ucid = aList[2]
        endIndex = ucid.index('@')
        if ucid[0:endIndex] in eventAttendance:
            gbmAttendance[ucid[0:endIndex]] += 1
    f.close()
    return
path = os.path.join(".", "October2022Attendance")
files = os.listdir(path)
for file in files:
    if file.startswith("GBM"):
        updateGBMAttendance(os.path.join(path, file))
    else:
        updateEventAttendance(os.path.join(path, file))
