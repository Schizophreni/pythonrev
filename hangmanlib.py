'''
hangmanlib.py
   A set of library functions for use with your Hangman game
   Actually you can add all help functions here, and just 
   import you can use all functions! 
   Enjoy!
'''

LINEPERIMAGE = 9  # Every LINEPERIMAGE is a perfect picture of hangman


def print_hangman(spaceword, mistakes=6):
    '''
    print hangman : from 0 (hang) to 6 (hanged)
    '''

    lines = LINES.split('\n')
    space = (14+2*len(spaceword)//2)*' '
    start = mistakes * LINEPERIMAGE
    for line in lines[start: start + 5]:
        print(space, end='')
        print(line)
    print(7*' ', end='')
    print(spaceword, end='')
    print(' '*7, end='')
    print(lines[start+5])
    for line in lines[start+6:start+LINEPERIMAGE]:
        print(space, end='')
        print(line)

# end print_hangman_image

# We intentionally add LINES below: it's too long


LINES = ''' ______
|  |
|
|
|
|
|_____
|     |____
|__________|
______
|  |
|  O
| 
|  
| 
|_____
|     |____
|__________|
 ______
|  |
|  O
| /
| 
|
|_____
|     |____
|__________|
 ______
|  |
|  O
| /|
|  |
|
|_____
|     |____
|__________|
 ______
|  |
|  O
| /|\\
|  |
|
|_____
|     |____
|__________|
 ______
|  |
|  O
| /|\ 
|  |
| /
|_____
|     |____
|__________|
 ______
|  |
|  O
| /|\ 
|  |
| / \ 
|_____
|     |____
|__________|

'''