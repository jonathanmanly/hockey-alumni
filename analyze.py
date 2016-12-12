import numpy as np
import matplotlib.pyplot as plt
import copy
import time
import csv
import pickle
import pandas as pd
import itertools
from matplotlib_venn import venn3, venn3_circles

# This assumes that hockey.py has already been run to cache the analysis data

matchups = pd.read_csv('nhl_schedule.csv')
#from Hockey-Reference.com

players=[]
allnhl=[]


with open(r"allnhl.pickle", "rb") as input_file:
    allnhl = pickle.load(input_file)


with open(r"players.pickle", "rb") as input_file:
    players = pickle.load(input_file)


divisions={}

for p in players:
    if p[0] not in divisions:
        divisions[p[0]]=set([])
    divisions[p[0]].add(p[1].replace("_"," "))



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


num_alumni.sort_values('Num_total_alumni',inplace=True)
num_alumni.reset_index(inplace=True)

# Output graphs

fig, ax = plt.subplots()
fig.set_size_inches(18.5, 10.5)

index = np.arange(len(num_alumni))
bar_width = 0.35
opacity = 1.
legend = ax.legend(loc=2, shadow=True)

rects1 = plt.barh(index, num_alumni['Num_total_alumni'], bar_width,
                 alpha=opacity,
                 color='b',
                 label='Players')

rects2 = plt.barh(index + bar_width, num_alumni['Num_opposing_teams_alumni'], bar_width,
                 alpha=opacity,
                 color='y',
                 label='Teams')

plt.title('NHL Alumni, Players and Distinct Teams')
plt.yticks(np.arange(len(num_alumni)), num_alumni['Team'],rotation=10,va='center')
plt.xlabel('Teams with Alumni Players')
plt.legend(loc='lower right')

fig.savefig('active_alum_by_team_players_and_teams.png')
plt.close()


fig, ax = plt.subplots()
fig.set_size_inches(18.5, 10.5)

index = np.arange(len(num_alumni))
bar_width = 0.7
opacity = 1.
legend = ax.legend(loc=2, shadow=True)

rects1 = plt.barh(index, num_alumni['Num_total_alumni'], bar_width,
                 alpha=opacity,
                 color='b',
                 label='Players')


plt.title('NHL Alumni, Players')
plt.yticks(np.arange(len(num_alumni)), num_alumni['Team'],rotation=10,va='center')
plt.xlabel('Teams with Alumni Players')
plt.legend(loc='lower right')

fig.savefig('active_alum_by_team_players.png')
plt.close()



num_alumni.sort_values('Num_opposing_teams_alumni',inplace=True)
num_alumni.reset_index(inplace=True)

fig, ax = plt.subplots()
fig.set_size_inches(18.5, 10.5)

index = np.arange(len(num_alumni))
bar_width = 0.7
opacity = 1.
legend = ax.legend(loc=2, shadow=True)

rects1 = plt.barh(index, num_alumni['Num_opposing_teams_alumni'], bar_width,
                 alpha=opacity,
                 color='y',
                 label='Players')


plt.title('NHL Alumni, Distinct Teams')
plt.yticks(np.arange(len(num_alumni)), num_alumni['Team'],rotation=10,va='center')
plt.xlabel('Teams with Alumni Players')
plt.legend(loc='lower right')

fig.savefig('active_alum_by_team_distinct_teams.png')
plt.close()



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


def makeHeatMap(matrix,teamsindex,divname):
    column_labels = teamsindex
    row_labels = teamsindex
    fig, ax = plt.subplots()
    fig=plt.pcolor(matrix,cmap=plt.cm.Reds)
    ax.set_yticks(np.arange(matrix.shape[0])+0.5,)
    ax.set_xticks(np.arange(matrix.shape[1])+0.5)
    ax.set_xticklabels(row_labels,rotation=90)
    ax.set_yticklabels(column_labels)
    plt.title(divname)
    plt.subplots_adjust(left=.3, right=.98, top=.9, bottom=.3)
    fig.figure.savefig('heat_map_'+divname+'.png')
    plt.close()



for d in divisions:
    teamsToMap = sorted(list(divisions[d]))
    thisDiv = df1.ix[teamsToMap][teamsToMap]
    makeHeatMap(thisDiv,teamsToMap,d)



# Track the effective proportion of games with an alumni

games_with=[]

for h in allnhl:
    z=0
    q=0
    for i in range(len(matchups)):
        vis = matchups.ix[i]['Visitor']
        home = matchups.ix[i]['Home']
        if home==h or vis==h:
            bi=1*((df1.ix[home][vis]+df1.ix[vis][home])>0)
            al = 1*((df1.ix[home][vis])>0)
            #print home,vis,bi
            z=z+bi
            q=q+al
    games_with.append([h,z,q])



games_with_df = pd.DataFrame(games_with)
games_with_df.columns = ['Team','Games_Bidirectional','Games_Alumni']



#print games_with_df



games_with_df.sort_values('Games_Bidirectional',inplace=True)
games_with_df.reset_index(inplace=True)

fig, ax = plt.subplots()
fig.set_size_inches(18.5, 10.5)

index = np.arange(len(games_with_df))
bar_width = 0.7
opacity = 1.
legend = ax.legend(loc=2, shadow=True)

rects1 = plt.barh(index, games_with_df['Games_Bidirectional'], bar_width,
                 alpha=opacity,
                 color='y',
                 label='Players')


plt.title('NHL Alumni Regular Season Proportion, Bidirectional')
axes = plt.gca()
axes.set_xlim([0,82])
plt.yticks(np.arange(len(games_with_df)), np.array(games_with_df['Team']),rotation=10,va='center')
plt.xlabel('Games with Alumni Players')
plt.legend(loc='lower right')

plt.savefig("schedule_weighted_proportion_bidirectional.png")
plt.close()



#-----------------------------

games_with_df.sort_values('Games_Alumni',inplace=True)
games_with_df.reset_index(inplace=True)

fig, ax = plt.subplots()
fig.set_size_inches(18.5, 10.5)

index = np.arange(len(games_with_df))
bar_width = .7
opacity = 1.
legend = ax.legend(loc=2, shadow=True)

rects1 = plt.barh(index, games_with_df['Games_Alumni'], bar_width,
                 alpha=opacity,
                 color='y',
                 label='Players')


plt.title('NHL Alumni Regular Season Proportion, Unidirectional')
axes = plt.gca()
axes.set_xlim([0,82])
plt.yticks(np.arange(len(games_with_df)), np.array(games_with_df['Team']),rotation=10,va='center')
plt.xlabel('Games with Alumni Players')
plt.legend(loc='lower right')

plt.savefig("schedule_weighted_proportion_unidirectional.png")
plt.close()



def playersAtLarge(team,alumni_by_current):
    allTeams =sorted(list(allnhl))
    for t in allTeams:
        if len(alumni_by_current[team][t])>0:
            print t,":",alumni_by_current[team][t]




playersAtLarge('Buffalo Sabres',alumni_by_current)


team_to_team_sets = {}

for team1 in alumni_by_current.keys():
    destinations = []
    for team2 in alumni_by_current[team1]:
        if len(alumni_by_current[team1][team2])>0:
            destinations.append(team2)
    team_to_team_sets[team1]=set(destinations)




for k in range(2,3):
    print k
    groups = itertools.combinations(list(allnhl),k)
    for g in groups:
        total_cover=set([])
        for t in g:
            total_cover=total_cover.union(team_to_team_sets[t])
            cover_and_orig = set(g).union(total_cover)
            if len(cover_and_orig)>=28 :#and 'Buffalo Sabres' in g
                print "WINNER",g
                print set(allnhl).difference(total_cover)
                print




#Make venn chart for Sabres and Pens
set1 = set(allnhl)
set2 = set(team_to_team_sets['Buffalo Sabres'])
set2.add("Buffalo Sabres")
set2.add("Dallas Stars")
set3 = set(team_to_team_sets['Pittsburgh Penguins'])
set3.add("Pittsburgh Penguins")
subset_list = [set3,set2,set1]





v = venn3(subsets=subset_list, set_labels = ('NHL', 'Buffalo Sabres', 'Pittsburgh Penguins'))
for i in range(len(v.set_labels)):
    text = v.set_labels[i]
    if i==0:
        text.set_text("")
    elif i==1:
        print text
        text.set_position((text.get_position()[0]+.25,.1))
    elif i==2:
        print text
        text.set_position((text.get_position()[0]-.85,0))


for i in range(len(v.subset_labels)):
    text = v.subset_labels[i]
    if i==3:
        text.set_position((text.get_position()[0],text.get_position()[1]-.1))
    elif i==4:
        text.set_position((text.get_position()[0]-.1,text.get_position()[1]))
    elif i==5:
        text.set_position((text.get_position()[0]+.05,text.get_position()[1]))

v.patches[3].set_color('grey')
v.patches[4].set_color('black')
v.patches[5].set_color('blue')
v.patches[6].set_color('green')

plt.title("NHL Teams with Sabres or Penguins")
plt.savefig("venn_sabres_pens_nhl.png")
plt.close()




