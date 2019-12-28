import os
import pdfrw
from random import *
from pandas import *
from math import ceil

races = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/Races.csv')
classes = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/Classes.csv')
subs = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/Subs.csv')
items = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/MagicItems.csv')
backgrounds = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/Backgrounds.csv')
profs = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/Profs.csv')
raceprofs = read_csv('https://raw.githubusercontent.com/2stickmen/charactergen/master/RacialProfs.csv')


vowels = ['A','E','I','O','U']
gender = ['Male', 'Female', 'Non-Binary']
alignments = ['Lawful Good', 'Neutral Good', 'Chaotic Good',
              'Lawful Neutral', 'True Neutral', 'Chaotic Neutral',
              'Lawful Evil', 'Neutral Evil', 'Chaotic Evil']
strSkills = ['Athletics']
dexSkills = ['Acrobatics', 'Sleight of Hand','Stealth']
intSkills = ['Arcana', 'History', 'Investigation', 'Nature', 'Religion']
wisSkills = ['Animal Handling', 'Insight', 'Medicine', 'Perception','Survival']
chaSkills = ['Deception', 'Intimidation', 'Performance', 'Persuasion']

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

def getPBonus(level):
    profBonus = ceil(level/4) +1
    return profBonus

def statBonus(stat):
    bonus = (stat-10)//2
    return bonus

def getHealth(CON, clas, level):
    classInfo = classes.loc[classes['Class:']==clas]
    con = statBonus(CON)
    hd = classInfo.iloc[0,3]
    baseHP = hd
    rolledHP = AdN(level-1,hd)
    conHP = con * (level-1)
    if con < 0:
        return baseHP + rolledHP
    return baseHP + rolledHP + conHP

def getRaceProfs(race):
    raceInfo = races.loc[races['racename'] == race]
    profAm = raceInfo.iloc[0,11]
    profs = []
    if profAm > 0:
        while len(profs) < profAm:
            r = randint(0,15)
            priors = []
            if r not in priors and type(raceprofs.loc[r,race]) != float and raceprofs.loc[r,race] not in profs:
                profs.append(raceprofs.loc[r,race])
            else:
                priors.append(r)
    return profs

def getProfs(level, stats, clas, race):
    strProfs = [statBonus(stats[0])]
    dexProfs = [statBonus(stats[1]),statBonus(stats[1]),statBonus(stats[1])]
    intProfs = [statBonus(stats[3]),statBonus(stats[3]),statBonus(stats[3]),statBonus(stats[3]),statBonus(stats[3])]
    wisProfs = [statBonus(stats[4]),statBonus(stats[4]),statBonus(stats[4]),statBonus(stats[4]),statBonus(stats[4])]
    chaProfs = [statBonus(stats[5]),statBonus(stats[5]),statBonus(stats[5]),statBonus(stats[5])]
    pb = getPBonus(level)
    classInfo = classes.loc[classes['Class:']==clas]
    profRolls = classInfo.iloc[0,6]
    proficiencies = []
    while len(proficiencies) < profRolls:
        priorRolls = []
        r = randint(0,16)
        if r not in priorRolls and type(profs.loc[r,clas]) != float and profs.loc[r,clas] not in proficiencies:
            proficiencies.append(profs.loc[r,clas])
            priorRolls.append(r)
        else:
            priorRolls.append(r)
    for i in proficiencies:
        if i in strSkills:
            strProfs[strSkills.index(i)] += pb
        elif i in dexSkills:
            dexProfs[dexSkills.index(i)] += pb
        elif i in intSkills:
            intProfs[intSkills.index(i)] += pb
        elif i in wisSkills:
            wisProfs[wisSkills.index(i)] += pb
        elif i in chaSkills:
            chaProfs[chaSkills.index(i)] += pb
    if clas == 'Bard' and level >=2:
        for i in strSkills:
            if i not in proficiencies:
                strProfs[strSkills.index(i)] += pb//2
        for i in dexSkills:
            if i not in proficiencies:
                dexProfs[dexSkills.index(i)] += pb//2
        for i in intSkills:
            if i not in proficiencies:
                intProfs[intSkills.index(i)] += pb//2
        for i in wisSkills:
            if i not in proficiencies:
                wisProfs[wisSkills.index(i)] += pb//2
        for i in chaSkills:
            if i not in proficiencies:
                chaProfs[chaSkills.index(i)] += pb//2
        
    outProfs = [strProfs,dexProfs,intProfs,wisProfs,chaProfs]        
    return outProfs

def getSaves(level,stats,clas):
     classInfo = classes.loc[classes['Class:']==clas]
     out = [statBonus(stats[0]),statBonus(stats[1]),statBonus(stats[2]),statBonus(stats[3]),statBonus(stats[4]),statBonus(stats[5])]
     profs = [classInfo.iloc[0,4],classInfo.iloc[0,5]]
     pb = getPBonus(level)
     for i in profs:
         out[i] += pb
     return out
         

def makeCharacter(level, *args): # Input a list: [Amount of common items, Amount of uncommon items...]
    race = getRace()
    clas = getClass()
    classInfo = classes.loc[classes['Class:']==clas]
    sub = ''
    if level >= classInfo.iloc[0,2]:
        sub = getSub(clas)
    ft = getHeight(race)[0]
    inch = getHeight(race)[1]
    preStats = statOptimise(statGen(),clas)
    adjStats = statAdj(race,clas)
    stats = statCheck([m + n for m,n in zip(preStats,adjStats)])
    gend = choices(gender,[0.45,0.45,0.1])[0]
    alignment = choices(alignments,[5/36,5/36,5/36,5/36,5/36,5/36,2/36,2/36,2/36])[0]
    bg = getBG()
    pb = getPBonus(level)
    hp = getHealth(stats[2], clas, level)
    profs = getProfs(level, stats, clas, race)
    saves = getSaves(level, stats, clas)
    inv = []
    if len(args) == 0:
            output = [[gend, race, sub, clas, bg, stats, ft, inch, alignment, level, pb, hp], [profs, saves], inv]
    else:
        inv = getInv(*args)
        output = [[gend, race, sub, clas, bg , stats,ft,inch, alignment,level,pb,hp,hd],[profs,saves], inv]
    return output



char = makeCharacter(1)

def makeParty(n,*args):
    for i in range(n):
        print("Character " + str(i+1) + " is " + makeCharacter(*args))


Sheet_Path = 'C:/Users/2stic/Desktop/charactergen/Character Sheet.pdf'
OUTPUT_PATH = 'C:/Users/2stic/Desktop/charactergen/Out Character Sheet.pdf'


ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true'))) 
    annotations = template_pdf.pages[0][ANNOT_KEY]
    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if annotation[ANNOT_FIELD_KEY]:
                key = annotation[ANNOT_FIELD_KEY][1:-1]
                if key in data_dict.keys():
                    annotation.update(
                       pdfrw.PdfDict(AP=data_dict[key], V=data_dict[key])
                    )
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

data_dict = {
   'Gender': char[0][0],
   'Race' : char[0][1],
   'ClassLevel' : char[0][2] + ' ' + char[0][3] + ' ' + str(char[0][9]),
   'Background' : char[0][4],
   'ProfB' : '+ ' + str(char[0][10]),
   'HPMax' : char[0][11],
   'HPCurrent' : char[0][11],
   'STR' : char[0][5][0],
   'STRmod' : statBonus(char[0][5][0]),
   'DEX' : char[0][5][1],
   'DEXmod' : statBonus(char[0][5][1]),
   'CON' : char[0][5][2],
   'CONmod' : statBonus(char[0][5][2]),
   'INT' : char[0][5][3],
   'INTmod' : statBonus(char[0][5][3]),
   'WIS' : char[0][5][4],
   'WISmod' : statBonus(char[0][5][4]),
   'CHA' : char[0][5][5],
   'CHAmod' : statBonus(char[0][5][5]),
   'Alignment' : char[0][8],
   'SavingThrows' : char[1][1][0],
   'SavingThrows2' : char[1][1][1],
   'SavingThrows3' : char[1][1][2],
   'SavingThrows4' : char[1][1][3],
   'SavingThrows5' : char[1][1][4],
   'SavingThrows6' : char[1][1][5],
   'Athletics' : char[1][0][0][0],
   'Acrobatics' : char[1][0][1][0],
   'SleightofHand' : char[1][0][1][1],
   'Stealth' : char[1][0][1][2],
   'Arcana' : char[1][0][2][0],
   'History' : char[1][0][2][1],
   'Investigation' : char[1][0][2][2],
   'Nature' : char[1][0][2][3],
   'Religion' : char[1][0][2][4],
   'Animal Handling' : char[1][0][3][0],
   'Insight' : char[1][0][3][1],
   'Medicine' : char[1][0][3][2],
   'Perception' : char[1][0][3][3],
   'Survival' : char[1][0][3][4],
   'Deception' : char[1][0][4][0],
   'Intimidation' : char[1][0][4][1],
   'Performance' : char[1][0][4][2],
   'Persuasion' : char[1][0][4][3],
   'Passive' : 10 + char[1][0][3][3],
   'Equipment' : char[2],
   'HD' : 'd' + str(char[0][-1]),
   'HDTotal' : str(char[0][9]) + 'd' + str(char[0][-1]),
   
}

write_fillable_pdf(Sheet_Path, OUTPUT_PATH, data_dict)
