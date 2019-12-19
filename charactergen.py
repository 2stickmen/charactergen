from random import *
from pandas import *


races = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/Races.csv')
classes = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/Classes.csv')
subs = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/Subs.csv')
items = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/MagicItems.csv')
backgrounds = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/Backgrounds.csv')
vowels = ['A','E','I','O','U']
gender = ['Male', 'Female', 'Non-Binary']
alignments = ['Lawful Good', 'Neutral Good', 'Chaotic Good',
              'Lawful Neutral', 'True Neutral', 'Chaotic Neutral',
              'Lawful Evil', 'Neutral Evil', 'Chaotic Evil']

def getItem(n,r):
    item = []
    for i in range(n):
        gen = randint(0,items.shape[0]-1)
        while type(items.iloc[gen,r]) == float:
            gen = randint(0,items.shape[0]-1)
        item.append(items.iloc[gen,r])
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
    race = races.iloc[randint(0,races.shape[0]-1),0]
    return race

def getClass():
    clas = classes.iloc[randint(0,classes.shape[0]-1,),0]
    return clas

def getSub(n):
    sub = subs.loc[randint(0,subs.shape[0]-1),n]
    while type(sub) == float:
        sub = subs.loc[randint(0,subs.shape[0]-1),n]
    return sub

def getBG():
    bg = backgrounds.iloc[randint(0,backgrounds.shape[0]-1),0]
    return bg

def makeCharacter(*args): # Input a list: [Amount of common items, Amount of uncommon items...]
    race = getRace()
    clas = getClass()
    sub = getSub(clas)
    stats = str(statGen())
    gend = choice(gender)
    alignment = choice(alignments)
    bg = getBG()
    
    if len(args) == 0:
            print("You are a {} {} {} {} who is also {}. Your stats are: {}. Your alignment is {}. Happy Adventuring!").format(gend, race, sub, clas, bg, stats, alignment)
    else:
        inv = str(getInv(*args))
        print("You are a {} {} {} {} who is  also {}. Your stats are: {}. Your alignment is {}. You have the following magic items {}. Happy Adventuring!").format(gend, race, sub, clas, bg , stats, alignment ,inv)
    

def makeParty(n,*args):
    for i in range(n):
        print("Character " + str(i+1) + " is ")
        makeCharacter(*args)
    
