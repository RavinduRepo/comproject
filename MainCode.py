import pygame
import button, time
import importlib
import multiprocessing
from multiprocessing import Process, Value
import Tic_Tac_Toe_module as T
T.exit_board()
import PianoTyles_module as P
P.exit_board()
# import Hangman_module as H
# H.exit_board()

pygame.init()

font = pygame.font.SysFont("arialblack", 40)

TEXT_COL = (255, 255, 255)


screen = pygame.display.set_mode((800, 600))


#variables
screentype = "MainMenu"
butnX = 480
notlose = True
level_P = 4
P.change_level_P(level_P)
# MulPiano = True
play = True

#button images
back_img = pygame.image.load("MyImages/back.png").convert_alpha()
mainmenu_img = pygame.image.load("MyImages/mainmenu.png").convert_alpha()
mute_img = pygame.image.load("MyImages/mute.png").convert_alpha()
options_img = pygame.image.load("MyImages/options.png").convert_alpha()
pause_img = pygame.image.load("MyImages/pause.png").convert_alpha()
quit_img = pygame.image.load("MyImages/quit.png").convert_alpha()
resume_img = pygame.image.load("MyImages/resume.png").convert_alpha()
tictactoe_img = pygame.image.load("MyImages/tictactoe.png").convert_alpha()
hangman_img = pygame.image.load("MyImages/hangman.png").convert_alpha()
pianotiles_img = pygame.image.load("MyImages/pianotiles.png").convert_alpha()
twoplayer_img = pygame.image.load("MyImages/twoplayermode.png").convert_alpha()
singleplayer_img = pygame.image.load("MyImages/singleplayermode.png").convert_alpha()
menu_BG = pygame.image.load('MyImages/menuBG.png')
tictactoe_BG = pygame.image.load('MyImages/tictactoeBG.png')
hangman_BG = pygame.image.load('MyImages/hangmanBG.png')
pianotiles_BG = pygame.image.load('MyImages/pianotilesBG.png')

tictactoe_button = button.Button(butnX, 175, tictactoe_img, 1)
hangman_button = button.Button(butnX, 425, hangman_img, 1)
pianotiles_button = button.Button(butnX, 300, pianotiles_img, 1)
quit_button = button.Button(butnX, 525, quit_img, 0.65)
back_button = button.Button(butnX, 225, back_img, 1)
mainmenu_button = button.Button(butnX, 225, mainmenu_img, 1)
mute_button = button.Button(butnX, 225, mute_img, 1)
options_button = button.Button(butnX, 225, options_img, 1)
pause_button = button.Button(butnX, 225, pause_img, 1)
resume_button = button.Button(butnX, 225, resume_img, 1)
twoplayer_button = button.Button(butnX, 325, twoplayer_img, 0.8)
singleplayer_button = button.Button(butnX, 425, singleplayer_img, 0.8)
mainmenu_button = button.Button(butnX, 150, mainmenu_img, 0.8)

def Menu():
    #create game window
    pygame.display.set_caption("Main Menu")
    screen.blit(menu_BG, (0,0))

def TicTacToe():
    if screentype == "tictactoe":
        pygame.display.set_caption("TicTacToe")
    if screentype == "Ttwo":
        pygame.display.set_caption("TicTacToe Two Player")
    if screentype == "Tsingle":
        pygame.display.set_caption("TicTacToe Single Player")
    screen.blit(tictactoe_BG, (0,0))

def Pianotiles(share_T_play):
    importlib.reload(P)
    global notlose
    while notlose and share_T_play.value:
        print("piano loop")
        P.Play_P()
        notlose = P.play
    # pygame.display.set_caption("Pianotiles")

    
def Hangman():
    pygame.display.set_caption("Hangman")
    screen.blit(hangman_BG, (0,0))

# def Main_loop():
#     global screentype, play, WelcomeTicTacToe, welcomePianotiles, welcomeHangman, MulPiano
if __name__ == '__main__':
    share_T_play = Value('i', 1)
    while play:
        
        if screentype == "MainMenu":
            Menu()
            if tictactoe_button.draw(screen):
                screentype = "tictactoe"
                WelcomeTicTacToe = True
    
            if pianotiles_button.draw(screen):
                screentype = "pianotiles" 
                welcomePianotiles = True
                
            if hangman_button.draw(screen):
                screentype = "hangman"
                welcomeHangman = True
            if quit_button.draw(screen):
                play = False 
        #tictactoe game loop
        if screentype == "tictactoe":
            TicTacToe()
            goback = back_button.draw(screen)
            Quit = quit_button.draw(screen)
            twoplayer = twoplayer_button.draw(screen)
            singleplayer = singleplayer_button.draw(screen)
            pygame.display.update()
            if goback:
                screentype = "MainMenu"
                T.exit_board()
            if Quit:
                play = False 
            if twoplayer:
                screentype = "Ttwo"
            if singleplayer:
                screentype = "Tsingle"
                
        #2 player tictactoe
        if screentype == "Ttwo":
            TicTacToe()
            goback = back_button.draw(screen)
            Quit = quit_button.draw(screen) 
            menu = mainmenu_button.draw(screen)
            pygame.display.update()             
            if WelcomeTicTacToe:
                    importlib.reload(T)
                    T.WelcomeT()
                    WelcomeTicTacToe = False
            T.PlayTtwo()
            if goback:
                screentype = "tictactoe"
                T.exit_board()
                WelcomeTicTacToe = True
            if Quit:
                play = False 
            if menu:
                screentype = "MainMenu"
                T.exit_board()
        #1 player tictactoe
        if screentype == "Tsingle":
            TicTacToe()
            goback = back_button.draw(screen)
            Quit = quit_button.draw(screen) 
            menu = mainmenu_button.draw(screen)
            pygame.display.update()             
            if WelcomeTicTacToe:
                    importlib.reload(T)
                    T.WelcomeVsPC()
                    WelcomeTicTacToe = False    
            T.PlayTsingle()          
            if goback:
                screentype = "tictactoe"
                T.exit_board()
                WelcomeTicTacToe = True
            if Quit:
                play = False 
            if menu:
                screentype = "MainMenu"
                T.exit_board()
        
      
        #pianotiles game loop
        if screentype == "pianotiles":
            pygame.display.set_caption("Pianotiles")
            screen.blit(pianotiles_BG, (0,0))
            
            goback = back_button.draw(screen)
            Quit = quit_button.draw(screen)
            pygame.display.update()
            
            if goback:
                screentype = "MainMenu"
                P.exit_board()
                share_T_play.value = 0
            if Quit:
                play = False
                share_T_play.value = 0
            if welcomePianotiles:
                welcomePianotiles = False
                game_process = multiprocessing.Process(target=Pianotiles, args=(share_T_play,))
                # game_process.daemon = True

                game_process.start()
                print("pianotiles cliked")

        #hangman game loop
        if screentype == "hangman":
            Hangman()
            goback = back_button.draw(screen)
            Quit = quit_button.draw(screen)
            pygame.display.update()
            
            if goback:
                screentype = "MainMenu"
                P.exit_board()
            if Quit:
                play = False

            if welcomeHangman:
                welcomeHangman = False
                try:
                    import Hangman_module as H
                except:
                    importlib.reload(H)

                H.exit_board()
        

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False

        pygame.display.update()

    pygame.quit()