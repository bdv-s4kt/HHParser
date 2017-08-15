#!/usr/bin/env python3

def processFile(fileNames):
    """
    Using fileName opens this file,
    and return a list of hands
    """

    data = ""

    for file in fileNames:
        f = open(file, 'r')
        data += f.read()
        f.close()

    hands = []
    
    beg = 0
    end = 0

    while (True):
        beg = data.find('PokerStars', end)
        if beg == -1:
            break
        end = data.find('***********', beg)
        if end is not -1:
            hands.append(data[beg:end])
        else:
            hands.append(data[beg:])
            
    return hands

def getPlayers(header):
    """
    Return a map with info about players on each seat.
    """

    players = {}

    max6Seats = ['BU', 'SB', 'BB', 'EP', 'MP', 'CO']

    pos_beg = header.find('Seat #') + 6
    pos_end = header.find(' is the button')
    BU_pos = int(header[pos_beg : pos_end])

    while (True):
        pos_beg = header.find('Seat ', pos_end)
        if pos_beg == -1:
            break

        pos_beg += 5
        pos_end = header.find(':', pos_beg)
        
        num_seat = int(header[pos_beg : pos_end])

        index = (6 + num_seat - BU_pos) % 6

        pos_beg = pos_end + 2
        pos_end = header.find('(', pos_beg)

        player_name = header[pos_beg : pos_end - 1]

        pos_beg = pos_end + 1
        pos_end = header.find(' in chips', pos_beg)

        player_stack = header[pos_beg : pos_end]

        players[player_name] = {
            'Pos': max6Seats[index],
            'Stack': player_stack,
            'Hole': '',
            'PF_actions': [],
            'F_actions': [],
            'T_actions': [],
            'R_actions': []
        }

    # now we get all info about 'Seat X' lines
    # and it's left to handle post blinds

    while (True):
        pos_beg = header.find('\n', pos_end) + 1
        pos_end = header.find(':', pos_beg)
        if pos_end == -1:
            break

        post_name = header[pos_beg : pos_end]

        pos_beg = pos_end + 2
        pos_end = header.find('\n', pos_beg)
        
        post_action = header[pos_beg : pos_end]

        players[post_name]['PF_actions'].append(post_action)
        
    return players

def parseHeaderInfo(header):
    """
    Return a structure that describes header of hand:
    such info as hand #, table name, time of play and so on
    """

    info = {}

    pos_beg = header.find('#')
    pos_end = header.find(':', pos_beg)

    info['Hand #'] = header[pos_beg + 1 : pos_end]

    pos_beg = pos_end + 3
    pos_end = header.find('(', pos_beg)

    info['Game'] = header[pos_beg : pos_end - 1]

    pos_beg = pos_end + 1
    pos_end = header.find(')', pos_beg)

    info['Blinds'] = header[pos_beg : pos_end]

    pos_beg = header.find('[', pos_end)
    pos_end = header.find(' ', pos_beg)

    info['Date'] = header[pos_beg  + 1 : pos_end]

    pos_beg = pos_end + 1
    pos_end = header.find(']', pos_beg)

    info['Time'] = header[pos_beg : pos_end]

    pos_beg = header.find('Table') + 6
    pos_end = header.find('Seat') - 1

    info['Table'] = header[pos_beg : pos_end]

    info['Players'] = getPlayers(header)
    
    return info

def parseHand(hand):
    """
    Return a structure that holds an information about hand
    which is getting from parser of hand,
    and it is read to put to SQL
    """

    res = {}

    header = hand[:hand.find('*** HOLE CARDS ***')]
    res = parseHeaderInfo(header)

    for name in res['Players'].keys():
        print(name)

        #res['Players'][name]['PF_actions'].append(
        
    
    return res

if __name__ == '__main__':
    fileNames = ['file1.txt',
                 'file2.txt']
    hands = processFile(fileNames)
    print("Processed: %s files, obtain %s hands."  % (len(fileNames), len(hands)))

    x = 28
    #print(hands[index])
    print(parseHand(hands[x]))

