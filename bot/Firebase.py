import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import botKey
cred = credentials.Certificate(botKey.FIREBASEFILE)
firebase_admin.initialize_app(cred,{'databaseURL': botKey.databaseUrl} )
ref = db.reference('users')
discordUsers = {}
usersDictionary = ref.get()
for user in usersDictionary:
    ucid = usersDictionary[user]['email']
    endIndex = ucid.index('@')
    if('discord' not in usersDictionary[user]):
        continue
    discUsers = usersDictionary[user]['discord']
    discordUsers[ucid[0:endIndex]]=int(discUsers)

def addLog(timeIn, timeOut, userId, userName):
    ref = db.reference('active_attendance_logs')
    logDictionary = ref.get()
    entry = {}
    present = False
    if logDictionary:
        for log in logDictionary:
            entry = ref.child(log).get()
            if entry['user_ID'] == userId:
                present = True
    if not present:
        data = {'in': timeIn, 'out': timeOut, 'user_ID':userId, 'userName':userName}
        ref = db.reference('active_attendance_logs')
        ref.push(data)
        return True
    return False

def updateLog(userId, timeOut):
    ref = db.reference('active_attendance_logs')
    logDictionary = ref.get()
    entry = {}
    present = False
    if logDictionary:
        for log in logDictionary:
            entry = ref.child(log).get()
            if entry['user_ID'] == userId:
                present = True
                ref.child(log).delete()
    if present:
        entry['out'] = timeOut
        db.reference('archive_attendance_logs').push(entry)
        return True
    return False
    
def getRoomStatus():
    ref = db.reference('active_attendance_logs')
    logDictionary = ref.get()
    loggedInList = []
    if logDictionary:
        for log in logDictionary:
            logContent = ref.child(log).get()
            if "none" == logContent['out']:
                loggedInList.append((logContent['userName'], logContent['in']))
    return loggedInList
