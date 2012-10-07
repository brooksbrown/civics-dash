from pprint import pprint
import os, inspect, sys



from flask import Flask, render_template, Markup, request, url_for
import jinja2

#serverside libraries setup
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"libs/python")))
if cmd_subfolder not in sys.path:
  sys.path.insert(0, cmd_subfolder)



import api

app = Flask(__name__)

# Helper Functions

MEDIA_CSS = [
  {'path':'/static/css/main.css', 'type':'text/css', 'media':'screen'},
  {'path':'/static/css/1140.css'},
  {'path':'/static/css/ie.css', 'conditional':'if lte IE 9'},
]


MEDIA_JS = [
  {'path':'https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js'},
  {'path':'http://maps.googleapis.com/maps/api/js?key='+api.keys.getKey('googleapi')+'&sensor=false'},
  {'path':'/static/js/libs/underscore/underscore.js'},
  {'path':'/static/js/libs/backbone/backbone.js'},
  {'path':'id/static/js/civicapp/civicapp.js'}
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


@app.route("/bill")
def bill():
  bill_object = api.getBill("house","3962","111")['objects'][0]
  vote_objects = api.getBillVotes("house","3962","111")['objects']
  
  return render_template('bill.html', bill=bill_object, votes=vote_objects, global_context=get_global_context())


@app.route("/")
def hello():
 return render_template('index.html', global_context=get_global_context())









@app.route("/votes")
def votes():
  state = request.args.get('state', '', type=str)
  chamber = request.args.get('chamber', '', type=str)
  votes = []
  votes_data = RTSCongressQuery("votes","chamber="+chamber+"&order=voted_at&page=1&per_page=5")
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
      pprint(vote['voters'][voter]['vote'])
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





#if __name__ == "__main__":
#      app.run()
