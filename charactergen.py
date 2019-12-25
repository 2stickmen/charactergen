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

def dN(N): #roll an n sided dice
    dN = randint(1,N)
    return dN

def AdN(A,N): #sum a roll of a n-sided dice 
    out = 0
    for a in range(A):
        out += dN(N)
    return out

def getItem(n,r): # gets a random item from the list
    item = []
    for i in range(n):
        gen = randint(0,items.shape[0]-1)
        while type(items.iloc[gen,r]) == float:
            gen = randint(0,items.shape[0]-1)
        item.append(items.iloc[gen,r])
    return item

def getInv(curvl): # generates an inventory given a list in order [amount of common items, amount of uncommon items..., amount of legendary items]
    inv = []
    while len(curvl) >5:
        curvl.pop()
    for i in range(len(curvl)):
        inv.extend(getItem(curvl[i],i))
    return str(inv)

def statGen(): # generates stats using 4d6 drop lowest
    stats = []
    for i in range(6):
        stat = [randint(1,6),randint(1,6),randint(1,6),randint(1,6)]
        stats.append(sum(stat)-min(stat))
    return stats      

def statCheck(stats):
    for i in range(len(stats)):
        if stats[i] > 20:
            stats[i] = 20
    return stats

def getRace():
    race = races.iloc[randint(0,races.shape[0]-1),0]
    return race

def getHeight(race):
    raceInfo = races.loc[races['racename'] == race]
    baseH = raceInfo.iloc[0,1]
    addH = AdN(raceInfo.iloc[0,2],raceInfo.iloc[0,3])
    footH = (baseH + addH) // 12
    inchH =  (baseH + addH) - footH*12
    return [footH,inchH]

def statAdj(race,clas):
    raceInfo = races.loc[races['racename'] == race]
    adjustment = []
    for i in range(4,10):
         adjustment.append(raceInfo.iloc[0,i])
    if raceInfo.iloc[0,10] != 0:
        i = 0
        nonspecamount = raceInfo.iloc[0,10]
        classInfo = classes.loc[classes['Class:']==clas]
        classPrio = classInfo.iloc[0,1]
        prio = [int(classPrio[2*n+1]) for n in range(0,6)]
        while nonspecamount > 0:  
            if adjustment[prio[i]] == 0:
                    adjustment[prio[i]] = 1
                    nonspecamount -= 1
            else:
                i+=1
                    
    return adjustment
     
def statOptimise(stats,clas):
    classInfo = classes.loc[classes['Class:']==clas]
    classPrio = classInfo.iloc[0,1]
    prio = [int(classPrio[2*n+1]) for n in range(0,6)]
    statEnd = [0,0,0,0,0,0]
    stats.sort()
    for i in prio:
        statEnd[i] = max(stats)
        stats.pop()
    
    return statEnd
    

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
    ft = getHeight(race)[0]
    inch = getHeight(race)[1]
    preStats = statOptimise(statGen(),clas)
    adjStats = statAdj(race,clas)
    stats = str(statCheck([m + n for m,n in zip(preStats,adjStats)]))
    gend = choices(gender,[0.45,0.45,0.1])[0]
    alignment = choices(alignments,[5/36,5/36,5/36,5/36,5/36,5/36,2/36,2/36,2/36])[0]
    bg = getBG()
    
    if len(args) == 0:
            output = "You are a {} {} {} {} who is also {}. Your stats are: {}. You are {} feet, {} inches tall. Your alignment is {}. Happy Adventuring!".format(gend, race, sub, clas, bg, stats,ft,inch, alignment)
    else:
        inv = str(getInv(*args))
        output = "You are a {} {} {} {} who is  also {}. Your stats are: {}. You are {} feet, {} inches tall. Your alignment is {}. You have the following magic items {}. Happy Adventuring!".format(gend, race, sub, clas, bg , stats,ft,inch, alignment ,inv)
    return output

def makeParty(n,*args):
    for i in range(n):
        print("Character " + str(i+1) + " is " + makeCharacter(*args))
    
    
