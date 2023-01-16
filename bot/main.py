import discord
import botKey
import Attendance
import Firebase
import datetime
from pytz import timezone
intent = discord.Intents.default()
intent.members = True
intent.message_content = True
# The client variable is the connection to discord
client = discord.Client(intents=intent)
eventAttendance = Attendance.eventAttendance
gbmAttendance = Attendance.gbmAttendance
totalGBMs = Attendance.totalGBMs
discordUsers = Firebase.discordUsers
projectRoles = [817401253873188924,885288221402071070,947685975868473345,945153200544153710, 627954695113015346, 817400993884930129,
                778386405248073744,1029840200924413993]
# register an event. discord.py is an asynchronous library, so things are done with callbacks. but callbacks are
# functions that are called when something else happens.
@client.event
# This event is going to be called when the bot is ready to be used
async def on_ready():
    # the 0 gets replaced with the client
    print('We have logged in as {0.user}'.format(client))
    if len(Firebase.getRoomStatus()) == 0:
        await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Room closed :('))
    else:
        await client.change_presence(status=discord.Status.online, activity=discord.Game('Room open :D'))
@client.event
# These functions are directly from the discord.py library
async def on_message(message):
    #prevents an endless loop
    if message.author == client.user:
        return
    if message.content.startswith('$UR'):
        #Create Active Member Role via Role ID
        AMrole = message.guild.get_role(762059892319060009)
        #Reset Active Member Roles for the month
        for ucid in discordUsers:
            member = message.guild.get_member(discordUsers[ucid])
            if member is None:
                continue
            await member.remove_roles(AMrole, reason=None, atomic=True)
        #loop through membership attendance
        for ucid in gbmAttendance:
            if eventAttendance[ucid] > 0 and gbmAttendance[ucid] >= (totalGBMs - 2) and ucid in discordUsers:
                    member = message.guild.get_member(discordUsers[ucid])
                    roles = member.roles
                    for role in roles:
                        if role.id in projectRoles:
                            await member.add_roles(AMrole, reason=None, atomic=True)
        print("Completed run")

    if message.content.startswith('.in'):
        #Creates a list of Members with the cardHolder role
        cardHolderList = message.guild.get_role(937732380028981318).members
        eboardList = message.guild.get_role(402894531814621185).members
        #Checking if Member that sent the command is in the list
        if(message.author in cardHolderList):
            mentions = message.mentions
            if bool(mentions)==True:
                someMember = mentions[0]
                if(message.author in eboardList or mentions[0]==message.author):
                    timeIn = str(datetime.datetime.now(timezone('EST')))
                    logResult = Firebase.addLog(timeIn, 'none', someMember.id, someMember.display_name)
                    await client.change_presence(status=discord.Status.online, activity=discord.Game('Room open :D'))
                    if logResult:
                        await message.channel.send(someMember.display_name + ' has signed in!')
                    else:
                        await message.channel.send("Some error has occured. Please verify that " + someMember.display_name + ' is not already signed in.')
                    return
                else:
                    await message.channel.send(message.author.display_name + ' is not authorized for this command')
                    return
            timeIn = str(datetime.datetime.now(timezone('EST')))
            logResult = Firebase.addLog(timeIn, 'none', message.author.id, message.author.display_name)
            await client.change_presence(status=discord.Status.online, activity=discord.Game('Room open :D'))
            if logResult:
                await message.channel.send(message.author.display_name + ' has signed in!')
            else:
                await message.channel.send("Some error has occured. Please verify that " + message.author.display_name + ' is not already signed in.')
        #If the Member that sent the command does not have card holder role
        else:
            mentions = message.mentions
            if bool(mentions) == True:
                await message.channel.send(message.author.display_name + ' is not authorized for this command')
                return
            await message.channel.send(message.author.display_name + ' is not authorized to sign in.')

    if message.content.startswith('.out'):
        #Creates a list of Members with the cardHolder role
        cardHolderList = message.guild.get_role(937732380028981318).members
        #Creates a list of Members with the eboard role
        eboardList = message.guild.get_role(402894531814621185).members
        #Checking if Member that sent the command has cardholder
        if (message.author in cardHolderList):
            #Create a list of mentioned Members
            mentions = message.mentions
            #if a mention was made
            if bool(mentions) == True:
                someMember = mentions[0]
                #if Member that sent the command is in eboard or mentioned themselves
                if(message.author in eboardList or mentions[0]==message.author):
                        timeOut = str(datetime.datetime.now(timezone('EST')))
                        logResult = Firebase.updateLog(someMember.id, timeOut)
                        if len(Firebase.getRoomStatus()) == 0:
                            await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Room closed :('))
                        else:
                            await client.change_presence(status=discord.Status.online, activity=discord.Game('Room open :D'))
                        if logResult:
                            message.channel.send(someMember.display_name + ' has signed out!')
                        else:
                            await message.channel.send("Some error has occured. Please verify that " + someMember.display_name + ' is signed in.')
                        return
                else:
                    await message.channel.send(message.author.display_name + ' is not authorized for this command')
                    return
            timeOut = str(datetime.datetime.now(timezone('EST')))
            logResult = Firebase.updateLog(message.author.id, timeOut)
            if len(Firebase.getRoomStatus()) == 0:
                await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Room closed :('))
            else:
                await client.change_presence(status=discord.Status.online, activity=discord.Game('Room is open :D'))
            if logResult:
                await message.channel.send(message.author.display_name + ' has signed out!')
            else:
                await message.channel.send("Some error has occured. Please verify that " + message.author.display_name + ' is signed in.')
        # If the Member that sent the command does not have card holder role
        else:
            mentions = message.mentions
            if bool(mentions) == True:
                await message.channel.send(message.author.display_name + ' is not authorized for this command')
                return
            await message.channel.send(message.author.display_name + ' is not authorized to sign out.')

    if message.content.startswith('.list-logged-in'):
        # Creates a list of Members with the eboard role
        cardHolderList = message.guild.get_role(937732380028981318).members
        # Checking if Member that sent the command is in eboard
        if (message.author in cardHolderList):
            if(len(Firebase.getRoomStatus()) != 0):
                textList = list(map(lambda x: x[0] + ": Logged in since " + x[1], Firebase.getRoomStatus()))
                await message.channel.send("Currently logged in:\n" + "\n".join(textList))
            else:
                await message.channel.send('Nobody is in the room')
        # If the Member that sent the command does not have eboard role
        else:
            await message.channel.send(message.author.display_name + ' is not authorized to view list.')
# Line to run the bot
client.run(botKey.key)
