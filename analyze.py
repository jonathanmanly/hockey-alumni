import numpy as np
import matplotlib.pyplot as plt
import copy
import time
import csv
import pickle




players=[]

'''
with open('players.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        players.append(row)
'''

allnhl=[]


with open(r"allnhl.pickle", "rb") as input_file:
    allnhl = pickle.load(input_file)


with open(r"players.pickle", "rb") as input_file:
    players = pickle.load(input_file)








currentTeams = {}

for p in players:
    currentTeams[p[2]]=p[1]



alumni={}


for team in allnhl:
    alumni[team]=[]


alumni_by_current={}


for team in allnhl:
    alumni_by_current[team]={}
    for team2 in allnhl:
        alumni_by_current[team][team2]=[]



print "add distinct team count"


for p in players:
    if len(p[3])>0:
        for t in p[3]:
            thisTeam = t.replace('_',' ')
            alumni[thisTeam].append(p[2])
            print p[1],thisTeam,p[2]
            alumni_by_current[thisTeam][p[1].replace('_',' ')].append(p[2])




print "Sabres alumni at large"
print alumni_by_current['Buffalo Sabres']


#teams with alumni

teams_with_alumni = []


for t in allnhl:
    i=0
    for o in allnhl:
        if len(alumni_by_current[t][o])>0:
            i+=1
    teams_with_alumni.append([t,i])



teams_with_alumni = sorted(teams_with_alumni,key=lambda x:x[1])




a_report = []

for a in alumni:
    a_report.append([ a, len(alumni[a])])


a_report = sorted(a_report,key=lambda x: x[1])


for a in a_report:
    print a


team_report = []



