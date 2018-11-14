import urllib.request
import json
import datetime
import sys


def _createDT(year,month,day,hour,min,inc=0):
    '''Return a correctly formatted datetime object'''
    try:
        if inc==0:
            return datetime.datetime(year,month,day,hour,min)
        if inc==1:
            return datetime.datetime(year,month+1,1,hour,min)
        return datetime.datetime(year+1,1,1,hour,min)
    except ValueError:
        return _createDT(year,month,day,hour,min,inc=inc+1)

def getTransitTimes(origin,dest,when):
    #Setting up constants used
    gmaps_endpoint='https://maps.googleapis.com/maps/api/directions/json?'
    geonames_endpoint='http://api.geonames.org/timezoneJSON?formatted=true&lat={}&lng={}&username=ecwhodie'
    gmaps_api_key='API_KEY_HERE'
    
    #Where and when the user is going and where they are coming from
    #eventTime=datetime.datetime(2018,1,1,0,0)
    eventTime=datetime.datetime(when[0],when[1],when[2],when[3],when[4])
    
    #Request, recieve, and process the estimated time in transit
    nav_request='origin={}&destination={}&key={}'.format(origin.replace(' ','+'),dest.replace(' ','+'),gmaps_api_key)
    request=gmaps_endpoint+nav_request
    response=urllib.request.urlopen(request).read()
    directions=json.loads(response)
    if directions['status']=='ZERO_RESULTS':
        print('Sorry, we could not calculate that...')
        sys.exit()
    routes=directions['routes']
    legs=routes[0]['legs']
    duration=legs[0]['duration']['text']
    print('The total time it will take for you to travel from {} to {} is {}'.format(origin,dest,duration))
    
    #Convert the duration string to usable numbers
    #Duration will appear as [day,hour,minute] when complete
    duration=duration.split()
    for i in range(len(duration)-1,-1,-1):
        try:
            duration[i]=int(duration[i])
        except:
            duration.pop(i)    
    while len(duration)<3:
        duration.insert(0,0)
    
    #Get the clients geo-location
    client_cords=legs[0]['start_location']
    lat=client_cords['lat']
    lng=client_cords['lng']
    
    #Request, recieve, and process the clients local time
    location_request=geonames_endpoint.format(lat,lng)
    geonames_request=urllib.request.urlopen(location_request).read()
    geonames_request=str(geonames_request)
    geonames_request=geonames_request[2:-1] #Hardcoded strip of the leading b and trailing \n
    replacement=['\\n','{','}','"'] #Chars that need replacing
    for elem in replacement:
        geonames_request=geonames_request.replace(elem,'')
    sliced=geonames_request.split(',') #can't cast as dictionary because of format. Prepares key and values as one list
    diction={}
    for elem in sliced:
        sp=elem.split(':', maxsplit=1) #Seperates the key from the values element 0 is key. Values become a list below based on spaces
        diction.update({sp[0].lstrip():sp[1].lstrip().split(' ')})
    dateTime=diction['time']
    
    #Get the clients local time and date
    military_time_str=dateTime[1]
    time=military_time_str.split(':') #List of [hour,minute] as a string
    date_=dateTime[0].split('-') #List of [year,month,day] as a string
    for i in range(len(time)): time[i]=int(time[i]) #Convert time to integer
    for i in range(len(date_)): date_[i]=int(date_[i]) #Convert date to integer
    year=date_[0]
    month=date_[1]
    day=date_[2]+duration[0]
    hour=time[0]+duration[1]
    min=time[1]+duration[2]
    if min>59:
        hour+=1
        min=min%60
    if hour>23:
        day+=1
        hour=hour%24
    dateTime=_createDT(year,month,day,hour,min)
    
    #Let the client know how long until they have to leave
    delta=eventTime-dateTime
    mins=delta.total_seconds()/60
    hrs=round(mins/60,2)
    if hrs<0.5 and hrs>0:
        print('You need to leave in {} minutes'.format(int(round(mins))))
        return('You need to leave in {} minutes'.format(int(round(mins))))
    elif hrs<0:
        print('You should have left {} minutes ago!'.format(int(abs(mins))))
        return('You should have left {} minutes ago!'.format(int(abs(mins))))
    else:
        print('You need to leave in {} hours'.format(hrs))
        return('You need to leave in {} hours'.format(hrs))


