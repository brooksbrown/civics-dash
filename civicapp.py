from pprint import pprint
import os, inspect, sys
from flask import Flask, render_template, Markup, request, url_for
import jinja2
import urllib2
import simplejson

#serverside libraries setup
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"libs/python")))
if cmd_subfolder not in sys.path:
  sys.path.insert(0, cmd_subfolder)

  
import sunlight
import RTC

RTC.apikey = sunlight.config.API_KEY = "73f79f89f833428da8ecb39952166f78"
googleapikey = "AIzaSyDQbFnzKRPgFdydHvZTbzbkNAIS7UBn7E4"




app = Flask(__name__)


# Helper Functions

MEDIA_CSS = [
  {'path':'/static/css/main.css', 'type':'text/css', 'media':'screen'},
  {'path':'/static/css/1140.css'},
  {'path':'/static/css/ie.css', 'conditional':'if lte IE 9'},
]


MEDIA_JS = [
  {'path':'https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js'},
  {'path':'http://maps.googleapis.com/maps/api/js?key='+googleapikey+'&sensor=false'},
  {'path':'/static/js/libs/underscore/underscore.js'},
  {'path':'/static/js/libs/backbone/backbone.js'},
  {'path':'/static/js/civicapp/civicapp.js'}
]


def get_css_media():
  media_string = ""
  for media in MEDIA_CSS:
    path = media['path'] if 'path' in media else "" 
    media_output = media['media'] if 'media' in media else "screen"
    if 'conditional' in media:
      media_string += '<!--['+media['conditional']+']>'
    media_string += '<link rel="stylesheet" href="'+path+'" type="text/css" media="'+media_output+'">'
    if 'conditional' in media:
      media_string += '<![endif]-->'
  return media_string

def get_js_media():
  media_string = ''
  for media in MEDIA_JS:
    path = media['path'] if 'path' in media else ""
    media_string += '<script type="text/javascript" src="'+path+'"></script>\n'
  return media_string

def get_global_context():
  return {
    'css':jinja2.Markup(get_css_media()),
    'js':jinja2.Markup(get_js_media())
  }

#API Helper
def RTSCongressQuery(queryType, query):
  url = "http://api.realtimecongress.org/api/v1/"
  req = urllib2.Request(url + queryType + ".json?" + query + "&apikey=73f79f89f833428da8ecb39952166f78")
  opener = urllib2.build_opener()
  f = opener.open(req)
  jsonObj = simplejson.load(f)
  return jsonObj




@app.route("/")
def hello():
  floor_updates_data = RTSCongressQuery("floor_updates","page=1&per_page=5")
  for floor_update in floor_updates_data['floor_updates']:
    bill = RTSCongressQuery("bills","bill_id=" + floor_update['bill_ids'][0])
    floor_update['bill_title'] = bill['bills'][0]['official_title']
  return render_template('index.html', floor_updates=floor_updates_data, global_context=get_global_context())









@app.route("/votes")
def votes():
  state = request.args.get('state', '', type=str)
  chamber = request.args.get('chamber', '', type=str)
  votes = []
  votes_data = RTSCongressQuery("votes","chamber="+chamber+"&order=voted_at&page=1&per_page=15")
  for vote in votes_data['votes']:
    imgdir = "/static/images/congressimages/40x50/"
    
    #collect sponsor info
    sponsor = sunlight.congress.legislators(bioguide_id=vote['bill']['sponsor_id'])[0]
    sponsor['sponsor_pic'] = imgdir+vote['bill']['sponsor_id']+".jpg"
    vote['sponsor'] = sponsor
    
    #collect votes
    yea = []
    nay = []
    
    for voter in vote['voters']:
      if vote['voters'][voter]['voter']['state'] == state:
        border = ""
        if vote['voters'][voter]['voter']['party'] == "R":
          border = "2px solid red"
        else: 
          border = "2px solid blue"

        thumb_markup = Markup("<img src='" + imgdir + voter + ".jpg' width='20' height='25' style='border:"+border+";'>")
        if vote['voters'][voter]['vote'] == "Yea":
          yea.append(thumb_markup)
        elif vote['voters'][voter]['vote'] == "Nay":
          nay.append(thumb_markup)
    vote['yea_thumbs'] = yea
    vote['nay_thumbs'] = nay

    voted_at = vote['voted_at'].split("T")
    votes.append(Markup(render_template('vote.html', vote=vote)))
  return render_template('votes.html', votes=votes, global_context=get_global_context()) 






