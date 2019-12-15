from random import *
from pandas import *

races = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/Races.csv')
classes = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/Classes.csv')
subs = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/Subs.csv')
items = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/MagicItems.csv')
vowels = ['A','E','I','O','U']

def getItem(n,r):
    item = []
    for i in range(n):
        item.append(items.iloc[randint(0,136),r])
    return item

def getInv(curvl):
    inv = []
    while len(curvl) >5:
        curvl.pop()
    for i in range(len(curvl)):
        inv.extend(getItem(curvl[i],i))
    return str(inv)

def statGen():
    stats = []
    for i in range(6):
        stat = [randint(1,6),randint(1,6),randint(1,6),randint(1,6)]
        stats.append(sum(stat)-min(stat))
    return stats        

def getRace():
    race = races.iloc[randint(0,81),0]
    return race

def getClass():
    clas = classes.iloc[randint(0,12),0]
    return clas

def getSub(n):
    sub = subs.loc[randint(0,17),n]
    while type(sub) == float:
        sub = subs.loc[randint(0,17),n]
    return sub

def makeCharacter(*args): # Input a list: [Amount of common items, Amount of uncommon items...]
    race = getRace()
    clas = getClass()
    sub = getSub(clas)
    stats = str(statGen())
    if len(args) == 0:
        if race[0] in vowels:
            print("You are an " + race + " " + sub + " " + clas 
                     + ". Your stats are: " + stats
                     + ". Happy Adventuring!")
        else:
            print("You are a " + race + " " + sub + " " + clas
                     + ". Your stats are: " + str(stats)
                     + ". Happy Adventuring!")
    else:
        inv = str(getInv(*args))
        if race[0] in vowels:
            print("You are an " + race + " " + sub + " " + clas
                     +". Your stats are " + stats
                     + ". You have the following magic items: " + inv
                     + ". Happy Adventuring!")
        else:
            print("You are a "  + race + " " + sub + " " + clas
                     +". Your stats are " + stats
                     + ". You have the following magic items: " + inv
                     + ". Happy Adventuring!")
    

def makeParty(n,*args):
    for i in range(n):
        makeCharacter(*args)
    
