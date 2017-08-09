#!/usr/bin/env python3

def processFile(fileName):
    file = open(fileName, 'r')
    data = file.read()
    file.close()
        
    beg = 0
    end = 0
    while (True):
        beg = data.find('PokerStars', end)
        if beg == -1:
            break
        end = data.find('***********', beg)
        if end is not -1:
            listOfHands.append(data[beg:end])
        else:
            listOfHands.append(data[beg:])
            
#--------------------------------------------------
listOfHands = []

processFile('file1.txt')
processFile('file2.txt')
processFile('file3.txt')

print("Number of Hands Processed: " + str(len(listOfHands)))
#---------------------------------------------------

#print(listOfHands[3])

seat4 = 'Seat 4: ' # EP
seat5 = 'Seat 5: ' # MP
seat6 = 'Seat 6: ' # CO
seat1 = 'Seat 1: ' # BU
seat2 = 'Seat 2: ' # SB
seat3 = 'Seat 3: ' # BB

baseInfo = listOfHands[3][:listOfHands[3].find('*** HOLE CARDS ***')]
#print('Base Info:\n' + baseInfo)

baseInfoLines = baseInfo.split('\n')

for i in range(len(baseInfoLines)):
    if seat4 in baseInfoLines[i]:
        nameEP = baseInfoLines[i][len(seat4):].split()[0]
        stackEP = baseInfoLines[i][len(seat4):].split()[1][1:]
    if seat5 in baseInfoLines[i]:
        nameMP = baseInfoLines[i][len(seat5):].split()[0]
        stackMP = baseInfoLines[i][len(seat5):].split()[1][1:]
    if seat6 in baseInfoLines[i]:
        nameCO = baseInfoLines[i][len(seat6):].split()[0]
        stackCO = baseInfoLines[i][len(seat6):].split()[1][1:]
    if seat1 in baseInfoLines[i]:
        nameBU = baseInfoLines[i][len(seat1):].split()[0]
        stackBU = baseInfoLines[i][len(seat1):].split()[1][1:]
    if seat2 in baseInfoLines[i]:
        nameSB = baseInfoLines[i][len(seat2):].split()[0]
        stackSB = baseInfoLines[i][len(seat2):].split()[1][1:]
    if seat3 in baseInfoLines[i]:
        nameBB = baseInfoLines[i][len(seat3):].split()[0]
        stackBB = baseInfoLines[i][len(seat3):].split()[1][1:]

BB = 5

#print("   EP: " + nameEP + ' ' * (20 - len(nameEP)) + stackEP + ' ' * (10 - len(stackEP)) + str(float(stackEP[1:]) * 100 / BB) + ' BB')
#print("   MP: " + nameMP + ' ' * (20 - len(nameMP)) + stackMP + ' ' * (10 - len(stackMP)) + str(float(stackMP[1:]) * 100 / BB) + ' BB')
#print("   CO: " + nameCO + ' ' * (20 - len(nameCO)) + stackCO + ' ' * (10 - len(stackCO)) + str(float(stackCO[1:]) * 100 / BB) + ' BB')
#print("   BU: " + nameBU + ' ' * (20 - len(nameBU)) + stackBU + ' ' * (10 - len(stackBU)) + str(float(stackBU[1:]) * 100 / BB) + ' BB')
#print("   SB: " + nameSB + ' ' * (20 - len(nameSB)) + stackSB + ' ' * (10 - len(stackSB)) + str(float(stackSB[1:]) * 100 / BB) + ' BB')
#print("-> BB: " + nameBB + ' ' * (20 - len(nameBB)) + stackBB + ' ' * (10 - len(stackBB)) + str(float(stackBB[1:]) * 100 / BB) + ' BB')

# ----------------------------------------------

seats = {'EP': 'Seat 4',
         'MP': 'Seat 5',
         'CO': 'Seat 6',
         'BU': 'Seat 1',
         'SB': 'Seat 2',
         'BB': 'Seat 3',}

actions = []

for seat in seats.keys():
    
    foldedHands = 0

    for hand in listOfHands:

        PFpos = hand.find('*** HOLE CARDS ***')
        
        baseHandInfo = hand[:PFpos]
        #print('===============================')
        #print(baseHandInfo)
        namePos = baseHandInfo.find(seats[seat]) + len(seats[seat]) + 2
        endName = baseHandInfo.find('($', namePos) - 1
        
        name = baseHandInfo[namePos:endName]
        #print('-------------------------------')
        #print('name: ' + name)

        otherPos = hand.find('***', PFpos + 18)
        preflop = hand[PFpos:otherPos]
        #print('-------------------------------')
        #print(preflop)
        playerPos = preflop.find(name + ':')
        if playerPos is -1:
            break
        action = preflop[playerPos + len(name) + 2:].split()[0]
        #print('action: ' + action)

        if action == 'folds':
            foldedHands += 1
        if action not in actions:
            actions.append(action)
    
    numberOfHands = len(listOfHands)
    playedHands = numberOfHands - foldedHands

    print(seat + " playes " + str(playedHands) + "/" + str(numberOfHands) + " [" + str(100 * playedHands / numberOfHands) + ']')

print(actions)
