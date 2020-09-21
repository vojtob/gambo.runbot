import json

import numpy as np
import pandas as pd
import cv2 as cv2

import requests
from bs4 import BeautifulSoup

import simpleTime as st
import time

def getRaceOTKD2019():
    results = pd.read_csv('gambo.visualization/otkd/results2019.txt', '\t')
    results.dropna(subset=['Výsledný čas tímu'], inplace=True)
    # print(results.count())

    teams = []
    for index, row in results.iterrows():
        team = {}
        team['ID'] = row['#']
        team['name'] = row['Názov tímu']
        team['startTime'] = row['Čas štartu'][10:] + ':00'
        team['startTimeNumber'] = st.timeToSec(team['startTime'])
        team['duration'] = row['Výsledný čas tímu']
        team['durationNumber'] = st.timeToSec(team['duration'])
        teams.append(team)

    teams.sort(key=lambda elem: elem['startTimeNumber'])

    return teams

def scrapRaceVltava2019():
    teams = []
    r = requests.get('https://vltavarun.cz/live/watch-handover/cil')
    vltavaResults = BeautifulSoup(r.text, 'html.parser')
    for divTeams in vltavaResults.find_all('div', id='teams', limit=1):
        for aTeam in divTeams.find_all('a'):
            team = {}
            team['id'] = aTeam['href'].split('/')[-1]
            team['name'] = aTeam.string[aTeam.string.find('.')+2:]
            # print('*************')
            print('Team:', team['name'])
            team['results'] = []
            teams.append(team)
            teamRequest = requests.get('https://vltavarun.cz'+aTeam['href'])
            teamResults = BeautifulSoup(teamRequest.text, 'html.parser')
            for teamTable in teamResults.find_all('table', id='predavky', limit=1):
                for teamLegResult in teamTable.find_all('tr'):
                    # find the third row with time
                    counter = 0
                    for teamLegItem  in teamLegResult.find_all('td'):
                        if counter==2:
                            if(teamLegItem.string):
                                # print('    ', teamLegItem.string)
                                # this is the problem, because the first and last entry for each team without the space, 
                                # causing incorrect starting and ending time for all teams with times 1X:XX having just X:xx
                                team['results'].append(teamLegItem.string[8:].strip())
                            else:
                                team['results'].append('--')
                            break
                        counter += 1

    race = {}
    race['teams'] = teams
    with open('gambo.visualization/vltava/results2019.json', 'w', encoding='utf-8') as outfile:
        json.dump(race, outfile, ensure_ascii=False, indent=4)

def scrapRaceVltava2020():
    teams = []
    r = requests.get('https://mega.vltavarun.cz/live/watch-handover/cil')
    vltavaResults = BeautifulSoup(r.text, 'html.parser')
    for divTeams in vltavaResults.find_all('div', id='teams', limit=1):
        for aTeam in divTeams.find_all('a'):
            team = {}
            team['id'] = aTeam['href'].split('/')[-1]
            team['name'] = aTeam.string[aTeam.string.find('.')+2:]
            # print('*************')
            print('Team:', team['name'])
            team['results'] = []
            teams.append(team)
            try:
                teamRequest = requests.get('https://mega.vltavarun.cz'+aTeam['href'])
            except:
                print("---> Something went from when reading team {} with ID: {}".format(team['name'], team['id']))
                time.sleep(5)
                teamRequest = requests.get('https://mega.vltavarun.cz'+aTeam['href'])

            teamResults = BeautifulSoup(teamRequest.text, 'html.parser')
            for teamTable in teamResults.find_all('table', id='predavky', limit=1):
                for teamLegResult in teamTable.find_all('tr'):
                    # find the third row with time
                    counter = 0
                    for teamLegItem  in teamLegResult.find_all('td'):
                        if counter==2:
                            if(teamLegItem.string):
                                # print('    ', teamLegItem.string)
                                # fixed method of getting the time from the 'td' string - "just the last string"
                                team['results'].append(teamLegItem.string.rstrip().rsplit(' ')[-1])
                            else:
                                team['results'].append('--')
                            break
                        counter += 1

    race = {}
    race['teams'] = teams
    with open('gambo.visualization/vltava/results2020.json', 'w', encoding='utf-8') as outfile:
        json.dump(race, outfile, ensure_ascii=False, indent=4)


def getRaceVltava2019():
    with open('gambo.visualization/vltava/results2019.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        teamsData = data['teams']

    teams = []
    for teamData in teamsData:
        # print('process team', teamData)
        team = {}
        team['ID'] = teamData['id']
        team['name'] = teamData['name']
        if(team['name'] == 'Láďa a Míša testovací tým'):
            continue
        team['startTime'] = teamData['results'][0] + ':00'
        team['startTimeNumber'] = st.timeToSec(team['startTime'])
        endTime = teamData['results'][-2] + ':00'
        endTime = st.timeToSec(endTime)
        # result time is time in a day a we want to have a duration of race
        # it is running time in the first dat (seconds in day minus start time in seconds)
        # and running time in the second day
        team['durationNumber'] = (24*60*60) - team['startTimeNumber'] + endTime
        team['duration'] = st.secToString(team['durationNumber'], 1)
        teams.append(team)
    teams.sort(key=lambda elem: elem['startTimeNumber'])
    return teams


def getRaceVltava2020():
    with open('gambo.visualization/vltava/results2020.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        teamsData = data['teams']

    teams = []
    for teamData in teamsData:
        # print('process team', teamData)
        team = {}
        team['ID'] = teamData['id']
        team['name'] = teamData['name']
        if(team['name'] == 'Láďa a Míša testovací tým'):
            continue
        team['startTime'] = teamData['results'][0] + ':00'
        team['startTimeNumber'] = st.timeToSec(team['startTime'])
        endTime = teamData['results'][-2] + ':00'
        endTime = st.timeToSec(endTime)
        # result time is time in a day a we want to have a duration of race
        # it is running time in the first dat (seconds in day minus start time in seconds)
        # and running time in the second day
        team['durationNumber'] = (24*60*60) - team['startTimeNumber'] + endTime
        team['duration'] = st.secToString(team['durationNumber'], 1)
        teams.append(team)
    teams.sort(key=lambda elem: elem['startTimeNumber'])
    return teams

def getTeam(raceName):
    if(raceName == 'otkd2019'):
        return getRaceOTKD2019()
    elif(raceName == 'vltava2020'):
        return getRaceVltava2020()
    elif(raceName == 'vltava2019'):
        return getRaceVltava2019()
    elif(raceName == 'vltava2018'):
        return getRaceVltava2018()
    else:
        print('Poznam iba otkd2019, vltava2019, vltava2018')
        print(raceName, 'nepoznam')
        return None

def getFileName(raceName, videoDuration):
    if(raceName == 'otkd2019'):
        return './gambo.visualization/otkd/otkd2019_'+str(videoDuration)+'.avi'
    elif(raceName == 'vltava2020'):
        return './gambo.visualization/vltava/vltava2020_'+str(videoDuration)+'.avi'
    elif(raceName == 'vltava2019'):
        return './gambo.visualization/vltava/vltava2019_'+str(videoDuration)+'.avi'
    elif(raceName == 'vltava2018'):
        return './gambo.visualization/vltava/vltava2018_'+str(videoDuration)+'.avi'
    else:
        print('Poznam iba otkd2019, vltava2019, vltava2018, 2020...')
        print(raceName, 'nepoznam')
        return 'xxx.avi'


if __name__ == "__main__":  
    # execute only if run as a script
    # scrapRaceVltava2019()
    #scrapRaceVltava2018()
    scrapRaceVltava2020()
    # teams = getRaceVltava2019()
    print('DONE read data')
