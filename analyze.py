import numpy as np
import matplotlib.pyplot as plt
import copy
import time
import csv
import pickle


# This assumes that hockey.py has already been run to cache the analysis data

players=[]


allnhl=[]


with open(r"allnhl.pickle", "rb") as input_file:
    allnhl = pickle.load(input_file)


with open(r"players.pickle", "rb") as input_file:
    players = pickle.load(input_file)



# Create a dictionary where you can look up current NHL team by player name

currentTeams = {}

for p in players:
    currentTeams[p[2]]=p[1]


# For each team, create a list of active alumni playing on other teams

alumni={}


for team in allnhl:
    alumni[team]=[]


alumni_by_current={}


# Initialize an empty data structure

for team in allnhl:
    alumni_by_current[team]={}
    for team2 in allnhl:
        alumni_by_current[team][team2]=[]


# Iterate through the players.  Load the player's name under the NHL team for each former team for the player
for p in players:
    if len(p[3])>0:
        for t in p[3]:
            thisTeam = t.replace('_',' ')
            alumni[thisTeam].append(p[2])
            alumni_by_current[thisTeam][p[1].replace('_',' ')].append(p[2])



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



def playersAtLarge(team,alumni_by_current):
    allTeams =sorted(list(allnhl))
    for t in allTeams:
        if len(alumni_by_current[team][t])>0:
            print t,":",alumni_by_current[team][t]



playersAtLarge('Buffalo Sabres',alumni_by_current)


