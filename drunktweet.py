# drunktweet.py
'''
Print out possible drunk tweets from anywhere in the world.

Usage: ./drunktweet.py London, UK
'''

import regex
import requests
import json
import simplejson, urllib
import sys

def geosearch(query):
    args = {
        'address': query,
        'sensor': 'false',
    }
    googurl = "http://maps.googleapis.com/maps/api/geocode/json?" + urllib.urlencode(args)
    result = simplejson.load(urllib.urlopen(googurl))

    #{'lat': 21.6345879, 'lng': -160.0860288}
    sw=[str(result['results'][0]['geometry']['viewport']['southwest']['lng']),str(result['results'][0]['geometry']['viewport']['southwest']['lat'])]
    ne=[str(result['results'][0]['geometry']['viewport']['northeast']['lng']),str(result['results'][0]['geometry']['viewport']['northeast']['lat'])]

    return [sw,ne]

# Terms for being "wasted"
terms = { 'drunk','wasted','buzzed','hammered','plastered' }

# A fuzzy regex for people who can't type
pat = regex.compile(r"(?:\L<terms>){i,d,s,e<=2}$", regex.I, terms=terms)

# Connect to the Twitter streaming API
url   = "https://stream.twitter.com/1/statuses/filter.json"
location=geosearch(" ".join(sys.argv[1:]))
parms = {
    'locations' : location[0][0]+","+location[0][1]+","+location[1][0]+","+location[1][1]
    }
auth  = ('diffra','Tnwb0@mTw')
r = requests.post(url, data=parms, auth=auth)

# Print possible candidates
for line in r.iter_lines():
    if line:
        tweet = json.loads(line)
        status = tweet.get('text',u'')
        words = status.split()
        if any(pat.match(word) for word in words):
           print(tweet['user']['screen_name'], status)
