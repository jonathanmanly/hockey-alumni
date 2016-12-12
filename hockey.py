from bs4 import BeautifulSoup
import urllib2
import copy
import time
import csv
import pickle



def check():
    for p in playerTeamHistory:
        print p

try:
    with open(r"hockey_memcache.pickle", "rb") as input_file:
        memcache = pickle.load(input_file)
except:
    memcache={}

# Uncomment the below if you want to run with all new data from Wikipedia

#memcache={}


rosterurls =['https://en.wikipedia.org/wiki/List_of_current_NHL_Eastern_Conference_team_rosters'
,'https://en.wikipedia.org/wiki/List_of_current_NHL_Western_Conference_team_rosters']


allnhl=set([])
roster = []
for easturl in rosterurls:
    i=0
    if easturl in memcache:
        page = copy.deepcopy(memcache[easturl])
    else:
        resp = urllib2.urlopen(easturl)
        time.sleep(1)
        pageorig = resp.read()
        page = copy.deepcopy(pageorig)
        memcache[easturl]=copy.deepcopy(pageorig)
    while i<2000:
        teamx = page.find('mw-headline" id="')
        playerx = page.find('</span><span class="vcard"><span class="fn"><a href="')
        if teamx<playerx:
            x=teamx
            y=page[x:].find('">')
            team= page[x+17:x+y]
            page=page[17+x+y:]
            if 'Division' in team:
                division = team
            else:
                allnhl.add(team.replace('_',' '))
        else:
            x=page.find('</span><span class="vcard"><span class="fn"><a href="')
            y = page[x+53:].find('" title=')
            link = page[x+53:x+53+y]
            link=link.split('"')[0]
            page=page[x+y+53:]
            x=8
            y=page[x:].find('">')
            name = page[1+x:x+y]
            page=page[1+x+y:]
            if len(link)>0 and len(link)<80 and link[:5]=='/wiki':
                roster.append([division,team,name,link])
        i+=1


# Clean out some non-player links that make it through this far

finalroster = []
for r in roster:
    if 'Articles' not in r[2] and 'Upload' not in r[2] and 'project' not in r[2]:
        finalroster.append(r)


roster=finalroster


# Save out the roster to local drive

myfile = open("roster.csv", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
for row in roster:
    wr.writerow(row)



#Cleanup

errors = []
playerTeamHistory=[]


for r in roster[:1000]:
    p=r[0]+r[1]
    thisone = 'https://en.wikipedia.org'+r[3]
    if thisone in memcache:
        page = copy.deepcopy(memcache[thisone])
        s = BeautifulSoup(page,"html.parser").get_text()
    else:
        time.sleep(1)
        try:
            resp = urllib2.urlopen(thisone)
            page = resp.read()
            s = BeautifulSoup(page,"html.parser").get_text()
            memcache[thisone]=copy.deepcopy(s)
        except:
            s=' '
            print "error on",thisone
            errors.append(thisone)
    startpos = s.find("Former teams")
    endpos = s[startpos:].find("\n\n")
    playerTeamHistory.append([r[0],r[1],r[2],s[startpos:startpos+endpos].split("\n")[1:]])






with open(r"hockey_memcache.pickle", "wb") as output_file:
    pickle.dump(memcache, output_file)



# Run through the accumulated player/team history and ensure only NHL teams are retained
# Also update for some of the relevant recent team name changes

for i in range(len(playerTeamHistory)):
    p = playerTeamHistory[i]
    if p[3] is not None and len(p[3])>0:
        current = p[1].replace('_',' ')
        goodlist=[]
        for q in p[3]:
            if current != q and q in allnhl:
                goodlist.append(q)
            elif q=='Atlanta Thrashers' and current != 'Winnipeg Jets':
                goodlist.append('Winnipeg Jets')
            elif q=='Phoenix Coyotes' and current != 'Arizona Coyotes':
                goodlist.append('Arizona Coyotes')
            elif q=='Mighty Ducks of Anaheim' and current !='Anaheim Ducks':
                goodlist.append('Anaheim Ducks')
        playerTeamHistory[i]=[p[0],p[1],p[2],goodlist]



#check()

# Save images of the lists for analyses

with open(r"players.pickle", "wb") as output_file:
    pickle.dump(playerTeamHistory, output_file)


with open(r"allnhl.pickle", "wb") as output_file:
    pickle.dump(allnhl, output_file)











