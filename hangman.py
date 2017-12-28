import re
import os
import random
import string
import datetime
from time import sleep
from hangmanlib import print_hangman


class Player:
    def __init__(self, name, playstarttime, playendtime, playtimes,  wintimes, mistakes=0, key='God'):
        '''
        define a player with name. playstarttime and playendtime are when the
        game begin and end, mistakes is the total times that player has not
        gotten the right letter.
        '''
        self.name = name
        self.__mistakes = mistakes
        self.__playstarttime = playstarttime
        self.__playendtime = playendtime
        self.__playtimes = playtimes
        self.__wintimes = wintimes
        self.__score = 0
        self.key = key

    def getmis(self):
        return self.__mistakes

    def setmis(self, mistakes):
        self.__mistakes = mistakes

    def getstartend(self):
        return self.__playstarttime, self.__playendtime

    def setstartend(self, playstarttime, playendtime):
        self.__playstarttime = playstarttime
        self.__playendtime = playendtime
   
    def setscore(self, mistakes):
        self.__score = 40 + (6-mistakes)*10

    def getscore(self):
        return self.__score

    def getplaytimes(self):
        return self.__playtimes

    def setplaytimes(self, playtimes):
        self.__playtimes = playtimes
    
    def setwintime(self, wintimes):
        self.__wintimes = wintimes
    
    def getwintime(self):
        return self.__wintimes


def wordschoose(wordspath):
    '''
    choose a word randomly from a file.
    '''
    pattern = re.compile(r'\s+')
    wordslist = []
    with open(wordspath) as fil:
        words = fil.read()
    wordslist = re.split(pattern, words.strip())
    # print(wordslist)
    word = random.choice(wordslist)
    return word


def gamegui(word, letterGuessed, player):
    '''
    generate the game gui.
    '''
    os.system('cls')
    print('*'*50)
    print()
    print('Hello, {0:s} ! '.format(player.name).center(50))
    print()
    print('You have played {} times. \n'.format(player.getplaytimes()).center(50))
    if player.getplaytimes() != 0:
        print('your win rate is : {0:4.2f}%\n'.format(100*player.getwintime()/player.getplaytimes()))
    print('Welcome to the hungman game, hope you good luck!\n')
    print('when the game loads successfully, just tap a letter.\n')
    print('*'*50)
    print('\n')
    print('guessed letters:', ' '.join(letterGuessed))
    print('mistakes: {}'.format(player.getmis()))
    print_hangman(spacewordchange(letterGuessed, word), player.getmis())
    print()


def getInput(word, key):
    char = input()
    if char == key:
        print(word)
        sleep(1)
        return '*'
    elif (len(char) == 1) and (char in string.ascii_letters):
        return char
    else:
        main()
        print('The game will be restarted')
        return '_'


def rightJudge(char, word):
    if char in word:
        return True
    else:
        return False


def spacewordchange(letterGuessed, word):
    wordlist = ['_', ' ']*len(word)
    for i in range(len(word)):
        if word[i] in letterGuessed:
            wordlist[2*i] = word[i]
    return ''.join(wordlist)


def whetherstop(letterGuessed, word):
    '''
    cnt = 0
    tag = False
    for item in word:
        if item in letterGuessed:
            cnt += 1
    if cnt == len(word):
        tag = True
    return tag
    '''
    tag = False
    for item in word:
        if item not in letterGuessed:
            break
    else:
        tag = True
    return tag


def logfile(player, word, letters, whetherwin):
    with open('{}logPlay.csv'.format(player.name), 'a+') as fil:
        fil.write('{0}\t{1}\t{2}\t{3[0]}\t{3[1]}\t'.format(player.name, player.getplaytimes(), player.getwintime(), player.getstartend()))
        fil.write(word)
        fil.write(' '*(25-len(word)))
        fil.write(' '.join(letters))
        fil.write(' '*(50-len(letters)*2))
        fil.write(whetherwin)
        fil.write('\n')


def play(player):
    word = wordschoose('words.txt')
    letters = []
    letterGuessed = []
    start = datetime.datetime.now()
    starttime = start.strftime('%Y-%m-%d %H:%M:%S')
    whetherwin = 'LOSE'
    gamegui(word, [], player)
    while(player.getmis() < 6):
        char = getInput(word, player.key)
        letters.append(char)
        if (not rightJudge(char, word)) and (char not in letterGuessed and (char != '*')):
            letterGuessed.append(char)
            player.setmis(player.getmis()+1)
            gamegui(word, letterGuessed, player)
        elif rightJudge(char, word) and (char not in letterGuessed):
            letterGuessed.append(char)
            gamegui(word, letterGuessed, player)
        elif char in letterGuessed:
            gamegui(word, letterGuessed, player)
        elif char == '*':
            gamegui(word, letterGuessed, player)
        if(whetherstop(letterGuessed, word)):
            break
    player.setscore(player.getmis())
    score = player.getscore()
    if player.getmis() == 6:
        print('You lose! ')
        print('Your score is: {0:4.1f}'.format(score))
        print("The right word is : {}, just keep trying !".format(word))
    if whetherstop(letterGuessed, word):
        print('You win! ')
        player.setwintime(player.getwintime()+1)
        whetherwin = 'WIN'
        print('Your score is: {0:4.1f}'.format(score))
        print("The right word is : {}, well done !".format(word))
    end = datetime.datetime.now()
    endtime = end.strftime('%Y-%m-%d %H:%M:%S')
    player.setstartend(starttime, endtime)
    player.setplaytimes(player.getplaytimes()+1)
    logfile(player, word, letters, whetherwin)


def main():
    plname = input('Please input your name below : ')
    playtimes = 0
    wintimes = 0
    try:
        with open('{}logPlay.csv'.format(plname), 'r') as fil:
            loglines = fil.readlines()
        logline = loglines[-1]
        longlinelist = logline.split()
        try:
            playtimes = int(longlinelist[1])
            wintimes = int(longlinelist[2])
        except IndexError:
            playtimes = 0
            wintimes = 0
    except OSError:
        with open('{}logPlay.csv'.format(plname), 'a+') as fil:
            fil.write('player name\t')
            fil.write('playtimes\t')
            fil.write('wintimes\t')
            fil.write('playStartTime\t')
            fil.write('PlayEndTime')
            fil.write(' '*20)
            fil.write('givenWord')
            fil.write(45*' ')
            fil.write('RESULT')
            fil.write('\n\n')
        playtimes = 0
        wintimes = 0
    player = Player(plname, 0, 0, playtimes, wintimes)
    while True:
        play(player)
        player.setmis(0)
        msg = input('Type (q/Q) to quit the game, type (y/Y) to continue: ')
        if msg.lower() == 'q':
            break
        elif msg.lower() == 'y':
            play(player)
        else:
            break


if __name__ == '__main__':
    main()
