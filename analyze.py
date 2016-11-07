import numpy as np
import matplotlib.pyplot as plt
import copy
import time
import csv
import pickle
import pandas as pd


# This assumes that hockey.py has already been run to cache the analysis data

players=[]


allnhl=[]


with open(r"allnhl.pickle", "rb") as input_file:
    allnhl = pickle.load(input_file)


with open(r"players.pickle", "rb") as input_file:
    players = pickle.load(input_file)


divisions={}

for p in players:
    if p[1] not in divisions:
        divisions[p[1]]=p[0]



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

teams_with_alumni = {}


for t in allnhl:
    i=0
    for o in allnhl:
        if len(alumni_by_current[t][o])>0:
            i+=1
    teams_with_alumni[t]=i





num_alumni_players = []

for a in allnhl:
    num_alumni_players.append([ a, len(alumni[a]),teams_with_alumni[a]])


num_alumni_players = sorted(num_alumni_players,key=lambda x: x[1])

num_alumni = pd.DataFrame(num_alumni_players)


num_alumni.columns = ['Team','Num_total_alumni','Num_opposing_teams_alumni']


'''

plt.barh(np.arange(len(num_alumni)),num_alumni['Num_total_alumni'])

plt.yticks(np.arange(len(num_alumni)), num_alumni['Team'])
plt.xlabel('Alumni Players')
plt.title('Alumni Players by Current Team')

plt.show()


plt.barh(np.arange(len(num_alumni)),num_alumni['Num_opposing_teams_alumni'])
plt.subplots_adjust(left=2., right=0.9, top=0.9, bottom=0.1)
plt.yticks(np.arange(len(num_alumni)), num_alumni['Team'])
plt.xlabel('Teams with Alumni Players')
plt.title('Teams with Alumni Player by Current Team')

plt.show()

'''
#https://pythonspot.com/en/matplotlib-bar-chart/


num_alumni.sort_values('Num_total_alumni',inplace=True)

fig, ax = plt.subplots()
fig.set_size_inches(18.5, 10.5)

index = np.arange(len(num_alumni))
bar_width = 0.35
opacity = 1.
#plt.subplots_adjust(left=2., right=0.9, top=0.9, bottom=0.1)
legend = ax.legend(loc=2, shadow=True)

rects1 = plt.barh(index, num_alumni['Num_total_alumni'], bar_width,
                 alpha=opacity,
                 color='b',
                 label='Players')

rects2 = plt.barh(index + bar_width, num_alumni['Num_opposing_teams_alumni'], bar_width,
                 alpha=opacity,
                 color='y',
                 label='Teams')


#plt.ylabel('Scores')
#ax.tick_params(direction='up', pad=15)
plt.title('NHL Alumni')
plt.yticks(np.arange(len(num_alumni)), num_alumni['Team'],rotation=10,va='center')
plt.xlabel('Teams with Alumni Players')
plt.legend(loc='lower right')

plt.show()
#plt.clf()

#fig.savefig('test2png.png', dpi=100)


fig, ax = plt.subplots()
fig.set_size_inches(18.5, 10.5)

index = np.arange(len(num_alumni))
bar_width = 0.7
opacity = 1.
#plt.subplots_adjust(left=1., right=0.9, top=0.9, bottom=0.1)
legend = ax.legend(loc=2, shadow=True)

rects1 = plt.barh(index, num_alumni['Num_total_alumni'], bar_width,
                 alpha=opacity,
                 color='b',
                 label='Players')


#plt.ylabel('Scores')
#ax.tick_params(direction='up', pad=15)
plt.title('NHL Alumni')
plt.yticks(np.arange(len(num_alumni)), num_alumni['Team'],rotation=10,va='center')
plt.xlabel('Teams with Alumni Players')
plt.legend(loc='lower right')

plt.show()
#plt.clf()



num_alumni.sort_values('Num_opposing_teams_alumni',inplace=True)

fig, ax = plt.subplots()
fig.set_size_inches(18.5, 10.5)

index = np.arange(len(num_alumni))
bar_width = 0.7
opacity = 1.
#plt.subplots_adjust(left=1., right=0.9, top=0.9, bottom=0.1)
legend = ax.legend(loc=2, shadow=True)

rects1 = plt.barh(index, num_alumni['Num_opposing_teams_alumni'], bar_width,
                 alpha=opacity,
                 color='y',
                 label='Players')


#plt.ylabel('Scores')
#ax.tick_params(direction='up', pad=15)
plt.title('NHL Alumni')
plt.yticks(np.arange(len(num_alumni)), num_alumni['Team'],rotation=10,va='center')
plt.xlabel('Teams with Alumni Players')
plt.legend(loc='lower right')

plt.show()





def playersAtLarge(team,alumni_by_current):
    allTeams =sorted(list(allnhl))
    for t in allTeams:
        if len(alumni_by_current[team][t])>0:
            print t,":",alumni_by_current[team][t]



playersAtLarge('Winnipeg Jets',alumni_by_current)

playersAtLarge('Ottawa Senators',alumni_by_current)


teamsindex = np.array(sorted(list(allnhl)))
for t in teamsindex:
    t=t.replace("_"," ")



df1 = pd.DataFrame(index=teamsindex)

for t in teamsindex:
    df1[t]=0


for p in players:
    if len(p[3])>0:
        for t in p[3]:
            z=df1[p[1].replace("_"," ")][t]
            df1=df1.set_value(p[1].replace("_"," "),t,1+z)


a=df1
column_labels = teamsindex
row_labels = teamsindex
fig, ax = plt.subplots()
fig=plt.pcolor(a,cmap=plt.cm.Reds)
ax.set_yticks(np.arange(a.shape[0])+0.5,)
ax.set_xticks(np.arange(a.shape[1])+0.5)
ax.set_xticklabels(row_labels,rotation=90)
ax.set_yticklabels(column_labels)
plt.subplots_adjust(left=.3, right=.98, top=.98, bottom=.3)

plt.show()
plt.close()


print "do this for each of the conferences and divisions... whats the odds youll play an alumni?"