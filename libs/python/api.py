import os, inspect, sys

import urllib2
import simplejson


#serverside libraries setup
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"libs/python")))
if cmd_subfolder not in sys.path:
  sys.path.insert(0, cmd_subfolder)



import keys
import sunlight
import RTC

RTC.apikey = sunlight.config.API_KEY = keys.getKey('sunlight')













#def RTSCongressQuery(queryType, query):
#  url = "http://api.realtimecongress.org/api/v1/"
#  req = urllib2.Request(url + queryType + ".json?" + query + "&apikey=" + keys.getKeys('sunlight'))
#  opener = urllib2.build_opener()
#  f = opener.open(req)
#  jsonObj = simplejson.load(f)
#  return jsonObj

def NYTCongressBillQuery(congressNumber, billID):
  version = "v3"
  url = "http://api.nytimes.com/svc/politics/"
  url = url + version + "/us/legislative/congress/"
  url = url + congressNumber + "/bills/" + billID +".json?"
  url = url + "api-key=" + keys.getKey('nytcongress')
  req = urllib2.Request(url)
  opener = urllib2.build_opener()
  f = opener.open(req)
  jsonObj = simplejson.load(f)
  return jsonObj

def GovTrackQuery(objectType, queryObject):
    url = "http://www.govtrack.us/api/v1/"
    url = url + objectType + "/?"
    for query in queryObject:
      url = url + query + "=" + queryObject[query] + "&"
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    jsonObj = simplejson.load(f)
    return jsonObj















#Connectors so we can switch out apis without changing syntax

def getBill(chamber, number, congress):
  return GovTrackQuery("bill",{"bill_type":chamber+"_bill","number":number,"congress":congress})


def getBillVotes(chamber, number, congress):
  return GovTrackQuery("vote",{"related_bill__congress":congress,"related_bill__number":number,"chamber":chamber})

def getBillVoteVoters(voteid):
  return GovTrackQuery("vote_voter",{"vote" : voteid})
