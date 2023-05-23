from pyfirmata import Arduino , util , INPUT , OUTPUT
import time
import TicTacToewithPC as PC

count1 = 0 #Click counts of button 1
count2 = 0 #Click counts of button 2
count3 = 0 #Click counts of button 3
swt1 = 0 #Status of button 1
swt2 = 0 #Status of button 2
swt3 = 0 #Status of button 3
swt1B = False #Last time status of button 1
swt2B = False #Last time status of button 2
swt3B = False #Last time status of button 3
player1_win_count = 0 #player 1 wins
player2_win_count = 0 #player 2 wins
draws = 0 #daw counts
Last_blink_time_s = 0 #last blink time for selector
loop_count_s = 0 #loop count for selector
Last_blink_time_p2 = 0 #last blink time for player2
loop_count_p2 = 0 #loop count for player2
M = [0,0,0,0,0,0,0,0,0]
player1 = [0,0,0,0,0,0,0,0,0]#player1 inputs
pb1 =  [0,0,0,0,0,0,0,0,0]
player2 = [0,0,0,0,0,0,0,0,0] #player2 inputs
pb2 = [0,0,0,0,0,0,0,0,0]
select = [0,0,0,0,0,0,0,0,0] #selector input
final = [0,0,0,0,0,0,0,0,0] #final list
used_points = 0 #used points on the list
continue_play = True 

board = Arduino("COM4") # initialising the arduino board

def exit_board():
    global board
    board.exit()

# initialising pints 
board.digital[2].mode = OUTPUT
board.digital[3].mode = OUTPUT
board.digital[4].mode = OUTPUT
board.digital[5].mode = OUTPUT
board.digital[6].mode = OUTPUT
board.digital[7].mode = OUTPUT
board.digital[8].mode = OUTPUT
board.digital[9].mode = OUTPUT
board.digital[10].mode = OUTPUT
board.digital[11].mode = OUTPUT#buzzer
board.analog[1].mode = INPUT#btn1
board.digital[12].mode = INPUT#btn2
board.digital[13].mode = INPUT#btn3

it = util.Iterator(board)
it.start()
board.analog[1].enable_reporting()
board.digital[12].enable_reporting()
board.digital[13].enable_reporting()

def ConvForPC(list):
    M3 = [0,0,0,0,0,0,0,0,0]
    for i in range(9):
        if list[i] == 2:
            list[i] = 'x'
    M3 = list
    return M3
def ConvFromPC(list):
    M3 = [0,0,0,0,0,0,0,0,0]
    for i in range(9):
        if list[i] == 'x':
            M3[i] = 1
    return M3

def welcome():
    ''' welcome message '''
    print("****WELCOME TO THE GAME OF TIC TAC TOE****")
    print("_"*len("****WELCOME TO THE GAME OF TIC TAC TOE****"))

def Btn1():
    ''' counts the number of cliks of btn 1 and return True '''
    global count1, swt1, swt1B
    sw = board.analog[1].read()
    time.sleep(0.02)
    if sw!= None:
        if sw > 0.5:
            swt1 = True
        elif sw < 0.1:
            swt1 = False
        if swt1 != swt1B:
            swt1B = swt1
            if swt1 == True:
                count1 += 1
                return True
    return False    

def Btn2():
    ''' counts the number of cliks of btn 2 and return True '''
    global count2,swt2,swt2B
    swt2 = board.digital[12].read()
    if swt2 !=swt2B:
        swt2B = swt2
        if swt2 == True:
            count2+=1
            return True        
    return False        

def Btn3():
    ''' counts the number of cliks of btn 3 and return True '''
    global count3,swt3,swt3B
    swt3 = board.digital[13].read()
    if swt3 !=swt3B:
        swt3B = swt3
        if swt3 == True:
            count3+=1
            return True
    return False
        
def MatrixAdd(M1,M2):
    ''' add given two lists of same size and return sum matrix '''
    temp_M1 = M1.copy()
    temp_M2 = M2.copy()
    M3 = [0,0,0,0,0,0,0,0,0]
    for i in range(9):
        if temp_M1[i] !=0:
           temp_M1[i] = 1
        if temp_M2[i] !=0:
           temp_M2[i] = 2 
        M3[i] = temp_M1[i] + temp_M2[i]
    return M3


def Select():
    ''' select a point on the list according to the 1,2 buttons '''
    global select
    if count1%3 == 0:
        for i in range(3):
            if count2%3 == i:
                select = [0,0,0,0,0,0,0,0,0]
                select[i] = 1

    if count1%3 == 1:
        for i in range(3):
            if count2%3 == i:
                select = [0,0,0,0,0,0,0,0,0]                
                select[i+3] = 1

    if count1%3 == 2:
        for i in range(3):
            if count2%3 == i:
                select = [0,0,0,0,0,0,0,0,0]
                select[i+6] = 1

def BlinkSelect(M1,delay):
    ''' blinking the select lits in gven delay '''
    global Time , Last_blink_time_s ,loop_count_s , M
    M0 = [0,0,0,0,0,0,0,0,0]
    if Time - Last_blink_time_s >= delay:
        Last_blink_time_s = Time
        loop_count_s += 1
        if loop_count_s%2 == 0:
            M = M1
        elif loop_count_s%2 == 1:
            M = M0
    return M

def BlinkP2(M1,delay):
    ''' blinking the player2 lits in gven delay'''
    global Time , Last_blink_time_p2 ,loop_count_p2 , M
    M0 = [0,0,0,0,0,0,0,0,0]
    if Time - Last_blink_time_p2 >= delay:
        Last_blink_time_p2 = Time
        loop_count_p2 += 1
        if loop_count_p2%2 == 0:
            M = M1
        elif loop_count_p2%2 == 1:
            M = M0
    return M

def LEDprint(grid):
    ''' print the given list on the 3*3 LED board '''
    for i in range(9):
        if grid[i] != 0:
            board.digital[i+2].write(1)
        elif grid[i] == 0:
            board.digital[i+2].write(0)

def GridPrint(grid):
    ''' print the given list (0 = "  " , 1 = " X " , 2 = " O " ) as a grid on the computer cmd '''
    PrintGrid = []
    for i in grid:
        if i == 0:
            PrintGrid.append("   ")
        elif i == 1:
            PrintGrid.append(" X ")
        elif i == 2:
            PrintGrid.append(" O ")

    print(PrintGrid[0],"|",PrintGrid[1],"|",PrintGrid[2])
    print("_______________")
    print(PrintGrid[3],"|",PrintGrid[4],"|",PrintGrid[5])
    print("_______________")
    print(PrintGrid[6],"|",PrintGrid[7],"|",PrintGrid[8])

def Print_status():  
    global player1, pb1, player2, pb2
    ''' print number of wins of each player '''
    p1 = player1.copy()
    p2 = player2.copy()
    if p1.count(0) != pb1.count(0) or p2.count(0) != pb2.count(0):
        pb1 = p1
        pb2 = p2
        printstst()

def printstst():
    global player1, player2
    print("\n\n\n\n")
    GridPrint(MatrixAdd(player1, player2))
    print("%s (X): %10s" %(P1,player1_win_count))
    print("%s (O): %10s" %(P2,player2_win_count))



def get_winner(player):
    ''' return True if a player of the given list has won or return False '''
    
    # Check for horizontal wins
    if (player[0] != 0 and player[0] == player[1] and player[1] == player[2]):
        return True
    elif (player[3] != 0 and player[3] == player[4] and player[4] == player[5]):
        return player[3]
    elif (player[6] != 0 and player[6] == player[7] and player[7] == player[8]):
        return True
    # Check for vertical wins
    elif (player[0] != 0 and player[0] == player[3] and player[3] == player[6]):
        return True
    elif (player[1] != 0 and player[1] == player[4] and player[4] == player[7]):
        return True
    elif (player[2] != 0 and player[2] == player[5] and player[5] == player[8]):
        return True
    # Check for diagonal wins
    elif (player[0] != 0 and player[0] == player[4] and player[4] == player[8]):
        return player[0]
    elif (player[2] != 0 and player[2] == player[4] and player[4] == player[6]):
        return True
    # If no winner yet
    else:
        return False

def new_round():
    ''' reset values for a new round '''
    global pb1, pb2,continue_play,draws,M,final,select,player2,player1,loop_count_p2,Last_blink_time_p2,loop_count_s,Last_blink_time_s,count1,count2,count3,swt1,swt2,swt3,swt1B,swt2B,swt3B

    count1 = 0
    count2 = 0
    count3 = 0
    swt1 = 0
    swt2 = 0
    swt3 = 0
    swt1B = False
    swt2B = False
    swt3B = False
    Last_blink_time_s = 0
    loop_count_s = 0
    Last_blink_time_p2 = 0
    loop_count_p2 = 0
    M = [0,0,0,0,0,0,0,0,0]
    player1 = [0,0,0,0,0,0,0,0,0]
    player2 = [0,0,0,0,0,0,0,0,0]
    select = [0,0,0,0,0,0,0,0,0]
    final = [0,0,0,0,0,0,0,0,0]
    continue_play = True
    pb1 =  [0,0,0,0,0,0,0,0,0]
    pb2 =  [0,0,0,0,0,0,0,0,0]


def reset():
    ''' reset all values back to start '''
    global continue_play,draws,M,final,player1_win_count,player2_win_count,select,player2,player1,loop_count_p2,Last_blink_time_p2,loop_count_s,Last_blink_time_s,count1,count2,count3,swt1,swt2,swt3,swt1B,swt2B,swt3B
    new_round()
    player1_win_count = 0
    player2_win_count = 0
    draws = 0
 

def start_pattern():
    ''' in lobby animation '''
    pattern = []
    t = time.time()
    period = 1  # duration of one cycle (in seconds)
    speed = 0.2 # speed of pattern movement (in seconds per LED)
    phase = 2 * speed * ((t % period) / period)  # current phase of pattern
    for i in range(9):
        row = i // 3
        col = i % 3
        time_offset = speed * (row + col)
        val = int((t - time_offset - phase) % (2*speed) < speed)
        pattern.append(val)
    return pattern

def ending_pattern():
    ''' ending pattern '''
    pattern = []
    t = time.time()
    for i in range(9):
        val = int((t * 10 + i) % 2)
        pattern.append(val)
    return pattern

def GetNames():
    global P1, P2
    P1 = input("Player 1(X): ") # get player names
    P2 = input("Player 2(O): ")

def WelcomeT():#the main looping function
    global Time,continue_play,draws,M,final,player1_win_count,player2_win_count,select,player2,player1,loop_count_p2,Last_blink_time_p2,loop_count_s,Last_blink_time_s,count1,count2,count3,swt1,swt2,swt3,swt1B,swt2B,swt3B
    
    # while not(Btn3() or Btn2() or Btn1()):
    #     continue
    welcome()
    #this part plays a welcome pattern in the LED board
    Time = int(time.time()* 1000)
    while int(time.time())*1000 < Time + 2000:
        pattern = start_pattern()
        LEDprint(pattern)
    reset()
    print("Enter players name\n")
    GetNames()
    print("\n\n\n\n")
    GridPrint(MatrixAdd(player1, player2))
    print("%s (X): %10s" %(P1,player1_win_count))
    print("%s (O): %10s" %(P2,player2_win_count))
    
def PlayTtwo():
    global player1,player2,Time,continue_play,draws,M,final,player1_win_count,player2_win_count,select,player2,player1,loop_count_p2,Last_blink_time_p2,loop_count_s,Last_blink_time_s,count1,count2,count3,swt1,swt2,swt3,swt1B,swt2B,swt3B
    Time = int(time.time() * 1000) # take the current time of the loop

    Btn1()
    Btn2()
    Select()
    
    if Btn3():
        for i in range(9):
            if select[i] == (player1[i] or player2[i]) != 0:
                count3-=1
                printstst()
                print("this is already selected")
            elif count3%2 == 1: # player 1 input
                player1[i] = player1[i] + select[i]
            elif count3%2 == 0: # player 2 input
                player2[i] = player2[i] + select[i]
                
        Print_status()
        if count3%2 == 1:#print next player
            print(P2,"is next")
        elif count3%2 == 0:
            print(P1,"is next")

    LEDprint(MatrixAdd(MatrixAdd(player1,BlinkSelect(select,200)),BlinkP2(player2,50)))# print given lists in given delays on LED s


    if get_winner(player1) or get_winner(player2): #check for winners
        if get_winner(player1):
            print(P1," has won. ",P2," has defeted")
            player1_win_count += 1
            board.digital[11].write(1)
            time.sleep(0.5)
            board.digital[11].write(0)

        elif get_winner(player2):
            print(P2," has won. ",P1," has defeted")
            player2_win_count += 1
            board.digital[11].write(1)
            time.sleep(0.5)
            board.digital[11].write(0)
        printstst()       
        while int(time.time())*1000 < Time + 2000:
            pattern = ending_pattern()
            LEDprint(pattern)
        new_round()
            

    #check if match is a draw
    used_points = 0
    for i in range(9):
        final[i] = player1[i] + player2[i]
        if final[i] != 0:
            used_points += 1

    if used_points == 9:
        printstst()
        print("\t\t\t\t the match is a draw")
        draws +=1
        time.sleep(0.5)
        while int(time.time())*1000 < Time + 2000:
            pattern = ending_pattern()
            LEDprint(pattern)
        new_round()


def WelcomeVsPC():
    global P1,P2
    welcome()
    #this part plays a welcome pattern in the LED board
    Time = int(time.time()* 1000)
    while int(time.time())*1000 < Time + 2000:
        pattern = start_pattern()
        LEDprint(pattern)
    print("Enter your name\n")
    P1 = input("Player name: ")
    P2 = 'PC'
    print("\n\n\n\n")
    GridPrint(MatrixAdd(player1, player2))
    print("%s (X): %10s" %(P1,player1_win_count))
    print("%s (O): %10s" %(P2,player2_win_count))

def PlayTsingle():
    global pb1, pb2, player1,player2,Time, continue_play,draws,M,final,player1_win_count,player2_win_count,select,player2,player1,loop_count_p2,Last_blink_time_p2,loop_count_s,Last_blink_time_s,count1,count2,count3,swt1,swt2,swt3,swt1B,swt2B,swt3B
    Time = int(time.time() * 1000) # take the current time of the loop

    Btn1()
    Btn2()
    Select()
    if Btn3():
        
        for i in range(9):
            if select[i] == (player1[i] or player2[i]) != 0:
                count3-=1
                printstst()
                print("this is already selected")
            else: # player  input
                player1[i] = player1[i] + select[i]
                     
    LEDprint(MatrixAdd(MatrixAdd(player1,BlinkSelect(select,200)),BlinkP2(player2,50)))# print given lists in given delays on LED s
    Print_status()

    if get_winner(player1) or get_winner(player2): #check for winners
        if get_winner(player1):
            print(P1," has won. ",P2," has defeted")
            player1_win_count += 1
            board.digital[11].write(1)
            time.sleep(0.5)
            board.digital[11].write(0)

        elif get_winner(player2):
            print(P2," has won. ",P1," has defeted")
            player2_win_count += 1
            board.digital[11].write(1)
            time.sleep(0.5)
            board.digital[11].write(0)
        printstst()  
        while int(time.time())*1000 < Time + 2000:
            pattern = ending_pattern()
            LEDprint(pattern)
        
        new_round()
            

    #check if match is a draw
    used_points = 0
    for i in range(9):
        final[i] = player1[i] + player2[i]
        if final[i] != 0:
            used_points += 1

    if used_points == 9:
        printstst()
        print("\t\t\t\t the match is a draw")
        draws +=1
        time.sleep(0.5)
        while int(time.time())*1000 < Time + 2000:
            pattern = ending_pattern()
            LEDprint(pattern)
        new_round()
    player2 = ConvFromPC(PC.Computer(ConvForPC(MatrixAdd(player1,player2))))
