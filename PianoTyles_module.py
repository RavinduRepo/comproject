import winsound
import random
import time
from pyfirmata import Arduino , OUTPUT , INPUT ,util
board = Arduino("COM4")
Hard_level = 4 # 1 to 4
L = (5 - Hard_level)/2
def change_level_P(level):
    global Hard_level
    Hard_level = level
# initialising pints
board.digital[11].mode = OUTPUT
board.digital[2].mode = OUTPUT
board.digital[3].mode = OUTPUT
board.digital[4].mode = OUTPUT
board.digital[5].mode = OUTPUT
board.digital[6].mode = OUTPUT
board.digital[7].mode = OUTPUT
board.digital[8].mode = OUTPUT
board.digital[9].mode = OUTPUT
board.digital[10].mode = OUTPUT
board.analog[1].mode = INPUT
board.digital[12].mode = INPUT
board.digital[13].mode = INPUT

it = util.Iterator(board)
it.start()
board.analog[1].enable_reporting()
board.digital[12].enable_reporting()
board.digital[13].enable_reporting()


M = [0,0,0,0,0,0,0,0,0]
roundcount=0
points = 0
play = True
n1 = 100
n2 = 100
n3 = 100


def printLED(list):
    ''' print the given list on the 3*3 LED board '''
    for i in range(9):
        if list[i] != 0:
            board.digital[i+2].write(1)
        elif list[i] == 0:
            board.digital[i+2].write(0)

def welcome():
    print("WELCOME TO THE GAME OF PIANO TILES!!!!")
    player_name =  input('Enter player name: ')

def Play_P():
    global M, points, play, n1, n2, n3, roundcount, L, play
    n1 = random.randint(0,2)
    M[n1] = 1
    if n2 != 100:
        M[n2 + 3] = 1
    if n3 != 100:
        M[n3 + 6] = 1
    n3 = n2
    n2 = n1

    roundcount +=1
    printLED(M) 

    c1 = 0
    c2 = 0
    c3 = 0  
    start_time = time.time() 
    while time.time() - start_time < L:
        if board.analog[1].read()!=None:
            if  board.analog[1].read() >0.5:
                c1 = 1
        if board.digital[12].read() == 1:
            c2 = 1
        if board.digital[13].read() == 1:
            c3 = 1

    if c1 == 1 and M[6] == 1:
        play = True
        points +=1
        print("your score is", points)

    elif c2 == 1 and M[7] == 1:
        play = True
        points +=1
        print("your score is", points)

    elif c3 == 1 and M[8] == 1:
        play = True
        points +=1
        print("your score is", points)
       
    elif M[6] == 0 and M[7] == 0 and M[8] == 0:
        play = True
    else:
        play = False

    M = [0,0,0,0,0,0,0,0,0]
    printLED(M) 
    time.sleep(0.01) 
points_file = open('opintsP.xlsx','w')
points_file.write("hiiiii")

def exit_board():
    global board
    board.exit()
