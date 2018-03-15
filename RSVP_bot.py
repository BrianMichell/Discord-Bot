import discord
import asyncio
import API_Testing

client=discord.Client()

evts={}

@client.event
async def on_ready():
    print('Logged in as {} {}'.format(client.user.name,client.user.id))
    
@client.event
async def on_message(message):
    
    if message.content==('!help'):
        await client.send_message(message.channel, 'Commands are !new, !remove, !register, !unregister, !list(developer command), !who')
        await client.send_message(message.channel, 'Use !help format to learn about formatting commands')
        await client.send_message(message.channel, 'Use !help (command) for specific command formats and info')
    elif message.content==('!help format'):
        await client.send_message(message.channel, 'Commands use commas (,) to seperate all fields with a space seperating the command word and the first field')
        await client.send_message(message.channel, 'For example !new lets eat pizza,2018,1,2,11,30')
    elif message.content=='!help new':
        await client.send_message(message.channel, '*!new Name(can include spaces),yyyy,mm,dd,hh,mm')
        await client.send_message(message.channel, 'Creates a new event with a name and date formatted as year,month,day,hour,minute')
    elif message.content=='!help remove':
        await client.send_message(message.channel, '*!remove Name(can include spaces)')
        await client.send_message(message.channel, 'Deletes the specified event')
    elif message.content=='!help register':
        await client.send_message(message.channel, '*!register Name(can include spaces),Origin address,Destination address')
        await client.send_message(message.channel, 'Registers you for the event and tells you how long until you need to leave to reach the event in time')
    elif message.content=='!help unregister':
        await client.send_message(message.channel, '*!unregister Name(can include spaces)')
        await client.send_message(message.channel, 'Removes your name from the event attendee list')
    elif message.content=='!help list':
        await client.send_message(message.channel, 'List is a developer tool used to debug the bot. It will dump all event info into the chat.')
    elif message.content=='!help who':
        await client.send_message(message.channel, '*!who Name(can include spaces)')
        await client.send_message(message.channel, 'Will display the users Discord username and ID number that are registered for the event')
    
    elif message.content.startswith('!new'):
        #Message must be !new eventName,yyyy,mm,dd,hh,mm,...
        #such that ... are people who will be there.
        #... is optional but will be appended to the event when a user uses the !register command
        print('Creating a new event')
        await client.send_message(message.channel, 'Creating a new event')
        msg=message.content.replace('!new ','')
        msg=msg.split(',')
        for i in range(1,6):
            msg[i]=int(msg[i])
        evts.update({msg[0].lower():msg[1:]})
        await client.send_message(message.channel,'Event created!')
        print('Event created!')
        
    elif message.content.startswith('!remove'):
        #Message must be !remove eventName
        print('Removing an event')
        await client.send_message(message.channel,'Removing an event')
        msg=message.content.replace('!remove ','')
        try:
            evts.pop(msg)
            await client.send_message(message.channel,'Event was successfully removed')
            print('Event was successfully removed')
        except:
            print('Event {} could not be removed'.format(msg))
            await client.send_message(message.channel,'Event {} could not be removed'.format(msg))
            print('Valid events are',evts.keys())
            
    elif message.content.startswith('!register'):
        #Message must be !register eventName,origin,destination
        msg=message.content.split(',')
        msg[0]=msg[0].replace('!register ','')
        print('Registering you for that event')
        await client.send_message(message.channel,'Registering you for that event')
        await client.send_message(message.channel, API_Testing.getTransitTimes(msg[1],msg[2],evts[msg[0]][:5]))
        evts[msg[0]].append(str(message.author))
        
    elif message.content.startswith('!unregister'):
        key=message.content.replace('!unregister ','')
        for i in range(len(evts[key])):
            if str(message.author)==evts[key][i]:
                evts[key].pop(i)
                break
        print('You are no longer registered for that event')
        await client.send_message(message.channel,'You are no longer registered for that event')
        
    elif message.content.startswith('!list'):
        await client.send_message(message.channel,evts)
        print(evts)
        
    elif message.content.startswith('!who'):
        try:
            await client.send_message(message.channel, 'Users going to that event are {}'.format(evts[message.content.replace('!who ','')][5:]))
            print('Users going to that event are {}'.format(evts[message.content.replace('!who ','')][5:]))
        except:
            await client.send_message(message.channel, 'No users are registered or that event is invalid!')
            print('No users are registered or that event is invalid!')
        
        
def remove(evt):
    for i in range(len(evts)):
        if evts[i]==evt:
            evts.pop(i)
            return True
    return False
        
client.run('Mzk3NDQ2MjUwMTkyMDQ0MDQy.DSwGQw.JWjcW54aBTyb_tEzd5Q5WDhURSc')