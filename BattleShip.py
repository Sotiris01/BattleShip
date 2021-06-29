
__author__ = 'Sotiris Mpalatsias'
__copyright__ = 'Copyright (C) 2021, BattleShip Game'
__version__ = '0.0.1'
__version__ = '2021/03/02'
__maintainer__ = 'Sotiris Mpalatsias'
__email__ = 'sotiris.mp@gmail.com'
__description__ = "A Simple BattleShip Game Player VS Player/Computer"

''' Begin Code '''

import random
import os
from sys import exit
from time import sleep
from copy import deepcopy
from msvcrt import getch
# try:
#     from sty import fg, rs
# except ModuleNotFoundError:
#     print("ERROR: Please install sty")
#     print(">pip install sty\n")
#     exit()

AUTOMATICALLY = False
MY_NAME = "■_■"

GAME_SIZE = 10
TOTAL_SHIPS = 5
MIN_SIZE = 3
CHAT_HISTORY = 20
CHAT_LIST = []

VS_Computer = True  # Player VS Computer by default
frame_list = []

def sea_(): return '~'
def hit_(): return 'x'
def target_(): return '+'
def miss_(): return 'o'
def myTurn_():
    return(random.choice(("My Turn",
            "It's my turn",
            "Me again",
            "I will make it this time",
            "Let's play hard now",
            "Now I'll crush you",
            "This time will be your last")))
def good_():
    return(random.choice(("hahaha",
                "Take this suckers",
                "No mercy",
                "Oh Yeah",
                "I've got this",
                "Finish them all",
                "Take this Bitch",
                "Make them cry",
                "The Win is mine",
                "There is no escape for you",
                "Go back to your mom",
                "I can hear you crying",
                "No one can beat me")))
def bad_():
    return(random.choice(("Damn it",
            "Next time",
            "Oh no",
            "Fuck",
            "I will end your laugh",
            "Mmm I have to focus",
            "Come on, you can do it",
            "I must try harder",
            "Come on now..",
            "Fuck I knew it",
            "Don't get your hopes up Folks",
            "Time will turn")))
def hit_happens_():
    return(random.choice(("That was a big one",
            "That must hurt",
            "ohhh",
            "They show no mercy",
            "Such a good fight",
            "Where is my pop-corn",
            "Let's see who wins",
            "This gave me chils")))


def main():
    global CHAT_LIST
    global VS_Computer
    global frame_list

    while True:
        next_frame()
        print("~~~ Welcome to BattleShip Game ~~~".center(80))
        print()

        print("You are the 1st Player")
        print("Give me your name: ", end='')
        name = input()[:10]
        player_1 = Player(name)

        print()

        print("If you want to play with me press <Enter>")
        print("else give me the name of the 2nd player: ", end='')
        name = input()[:10]

        if name == '':
            player_2 = Player()
        else:
            player_2 = Player(name)
            VS_Computer = False

        instructions = ("Place your ships: \n"
                        "you have "+str(TOTAL_SHIPS)+" ships \n"
                        "with sizes "+
                        ','.join(([str(MIN_SIZE+i) for i in range(TOTAL_SHIPS)]))+
                        "\nMove with <arrows> and rotate with <space>\n"
                        "then press <Enter>")

        # Player 1
        next_frame()
        input("{} are you ready...? <Enter>".format(player_1.name))

        frame_list.append(instructions)
        player_1.initialize_ships_positions()
        frame_list.pop()

        # Player 2
        if not VS_Computer:  
            next_frame()  
            input("{} are you ready...? <Enter>".format(player_2.name))

        frame_list.append(instructions)
        player_2.initialize_ships_positions()
        frame_list.pop()

        # Start Battle
        arena_1 = create_arena()
        arena_2 = create_arena()

        frame_list.append("{:^38} VS {:^38}".format(player_1.name,\
                                                    player_2.name))
        frame_list.append("")  # Arena
        frame_list.append("")  # Score
        frame_list.append("")  # Chat

        T = True  # Player 1 plays first
        p1_last_hit = [0,0]
        p2_last_hit = [0,0]
        while True:
            chat(player_1, player_2, T)

            if T:
                arena_2, p1_last_hit = make_a_hit(player_1, arena_1, arena_2,\
                                                    T, p1_last_hit)
                chat(player_1, player_2, T, arena_2[p1_last_hit[0]][p1_last_hit[1]])
            else:
                arena_1, p2_last_hit = make_a_hit(player_2, arena_1, arena_2,\
                                                    T, p2_last_hit)
                chat(player_1, player_2, T, arena_1[p2_last_hit[0]][p2_last_hit[1]])

            frame_list[2] = ("{:^37} hits {:^37}\n".format(score(arena_1),\
                                                        score(arena_2)))
            next_frame()

            if lost(arena_1):
                print(f"\n\n{player_2.name} you won !!!")
                break
            elif lost(arena_2):
                print(f"\n\n{player_1.name} you won !!!")
                break

            T = not T

        answer = input("Do you want to play again? [Y/n] ")
        if answer == '' or answer.upper()[0] == 'Y':
            frame_list = []
            CHAT_LIST = []
            del player_1
            del player_2
        else:
            break


def chat(player_1, player_2, hit_to_secont, hit=None):
    if hit_to_secont:
        if hit == None:
            print_to_chat("{:<80}".format(player_1.name+"> "+myTurn_()))
        elif hit == hit_():
            # print_to_chat("{:^80}".format(hit_happens_()))
            print_to_chat("{:<80}".format(player_1.name+"> "+good_()))
            # print_to_chat("{:>80}".format(player_2.name+bad_()))
        else:
            print_to_chat("{:<80}".format(player_1.name+"> "+bad_()))
    else:
        if hit == None:
            print_to_chat("{:>80}".format(myTurn_()+" <"+player_2.name))
        elif hit == hit_():
            # print_to_chat("{:^80}".format(hit_happens_()))
            print_to_chat("{:>80}".format(good_()+" <"+player_2.name))
            # print_to_chat("{:>80}".format(player_1.name+bad_()))
        else:
            print_to_chat("{:>80}".format(bad_()+" <"+player_2.name))


def print_to_chat(line):

    CHAT_LIST.append(line)
    if len(CHAT_LIST) > CHAT_HISTORY:
        CHAT_LIST.pop(0)

    frame_list[3] = '\n'.join(CHAT_LIST)
    # sleep(0.5)
    next_frame()


def lost(arena):
    global GAME_SIZE
    global MIN_SIZE
    global TOTAL_SHIPS

    c = MIN_SIZE
    total_points = sum([c+i for i in range(TOTAL_SHIPS)])

    count = score(arena)
    if count == total_points:
        return True
    else:
        return False


def score(arena):
    count = 0
    for i in range(GAME_SIZE):
        for j in range(GAME_SIZE):
            if arena[i][j] == hit_():
                count += 1
    return count


def make_a_hit(player, arena_1, arena_2, hit_to_secont, last_hit):
    board = player.get_board()
    arena = arena_2 if hit_to_secont else arena_1

    enter = False
    x,y = last_hit
    while True:
        if player.name == MY_NAME:
            x, y, _, enter = board_random_position()
        else:
            display_arenas(arena_1, arena_2, [x,y,hit_to_secont])
            x, y, _, enter = board_position(x,y)
        if enter:
            if arena[x][y] == sea_():
                break

    if board[x][y] == sea_():
        arena[x][y] = miss_()
    else:
        arena[x][y] = hit_()
    return arena, [x,y]


def create_arena():
    return [[sea_() for _ in range(GAME_SIZE)]\
                    for _ in range(GAME_SIZE)]


def display_arenas(arena_1, arena_2, target=None):
    global GAME_SIZE
    global frame_list
    if target is not None:
        hit_to_secont = target.pop()
    else:
        target = [-1,-1]
    arena = "\n"
    for i in range(GAME_SIZE):
        B1_line = ""
        B2_line = ""
        for j in range(GAME_SIZE):
            if [i,j] == target:
                if hit_to_secont:
                    B1_line += f" {arena_1[i][j]}"
                    B2_line += f" {target_()}"
                else:
                    B1_line += f" {target_()}"
                    B2_line += f" {arena_2[i][j]}"
            else:
                B1_line += f" {arena_1[i][j]}" 
                B2_line += f" {arena_2[i][j]}"
        arena += ("{:^38} ## {:^38}\n".format(B1_line, B2_line))
    arena += '\n'

    frame_list[1] = arena
    next_frame()


def board_position(x=0, y=0, flag=False,
                xmax=9, xmin=0,
                ymax=9, ymin=0):

    enter = False

    getKey = getch()

    if getKey == b'\r':
        enter = True
    elif getKey == b' ':
        flag = not flag
    elif getKey == b'\x1b':
        exit()
    elif getKey == b'\xe0':
        getKey = getch()

        if getKey == b'H':
            x -= 1  # Up
            x = xmin if x < xmin else x
        elif getKey == b'P':
            x += 1  # Down
            x = xmax if x > xmax else x
        elif getKey == b'M':
            y += 1  # Right
            y = ymax if y > ymax else y
        elif getKey == b'K':
            y -= 1  # Left
            y = ymin if y < ymin else y

    return (x, y, flag, enter)


def board_random_position(xmax=9, xmin=0, ymax=9, ymin=0):

    x = random.randint(xmin, xmax)
    y = random.randint(ymin, ymax)
    flag = bool(random.getrandbits(1))

    return(x, y, flag, True)
    

def next_frame():
    os.system('cls' if os.name == 'nt' else "printf '\033c'")
    print('='*80)
    print()
    for frame in frame_list:
        print(frame)


class Player:
    global GAME_SIZE
    global TOTAL_SHIPS
    name = "Player"

    def __init__(self, name=MY_NAME):
        # Name in form "JonWick"
        name = ''.join(name.title().split())
        if name != '':
            self.name = name
        self.create_board()
        self.create_ships()

    def __del__(self):
        for ship in self.ships:
            del ship

    def create_board(self):
        # 10x10 board
        self.board = [[sea_() for _ in range(GAME_SIZE)]\
                           for _ in range(GAME_SIZE)]

    def get_board(self):
        return self.board

    def create_ships(self):
        # Create 5 ships with sizes 3,4,5,6 and 7
        self.ships = [Ship(size) for size in range(MIN_SIZE,\
                                                    TOTAL_SHIPS+MIN_SIZE)]

    def displayBoard(self, board=None):
        if board is None:
            board = self.board
        next_frame()
        print()
        print("==> ", self.name)
        print()
        for i in range(GAME_SIZE):
            for j in range(GAME_SIZE):
                print(f" {board[i][j]}", end='')
            print()
        print()

    def __add_ship(self, ship, permanently=True):
        if permanently:
            board = self.board
        else:
            board = deepcopy(self.board)

        icon = ship.icon()
        for x,y in ship.get_position():
            board[x][y] = icon.__next__()

        if not permanently:    
            self.displayBoard(board)

    def ship_position_check(self, ship, x, y, is_horizontal):
        if is_horizontal:
            if y+ship.get_size() > GAME_SIZE:
                return False
        else:
            if x+ship.get_size() > GAME_SIZE:
                return False
        return True

    def ship_overlapping_check(self, ship):
        for x,y in ship.get_position():
            if self.board[x][y] != sea_():
                return False
        return True

    def initialize_ships_positions(self):
        for i, ship in enumerate(self.ships):
            # x,y = ship.x, ship.y
            h = True if ship.get_orientation() == "horizontal" else False

            while True:
                self.__add_ship(ship, permanently=False)
                # self.displayBoard()
                # self.__remove_ship(ship)

                if(self.name == MY_NAME):
                    x, y, h, submit = board_random_position()
                    # sleep(0.1)
                else:
                    if AUTOMATICALLY:
                        x, y, h, submit = board_random_position()
                    else:
                        x, y, h, submit = board_position(ship.x, ship.y, h)

                if self.ship_position_check(ship, x, y, h):

                    ship.set_position(x, y)
                    ship.set_orientation("horizontal" if h else "vertical")

                    if submit:
                        if self.ship_overlapping_check(ship):
                            break
                else:
                    h = True if ship.get_orientation() == "horizontal" else False
                    
            self.__add_ship(ship)
            self.displayBoard()
            self.ships[i] = ship


class Ship():
    __minSize = 2
    __maxSize = 10
    __size = 2
    __orientation = "horizontal"  # or "vertical"
    x,y = 0,0  # init position

    def __init__(self, size):
        if self.__minSize <= size <= self.__maxSize:
            self.__size = size
            self.__lives = size

    def icon(self):
        if self.__orientation == "horizontal":
            yield '◄'
        elif self.__orientation == "vertical":
            yield '▲'

        for _ in range(self.__size-2):
            yield '■'

        if self.__orientation == "horizontal":
            yield '►'
        elif self.__orientation == "vertical":
            yield '▼'

    def get_size(self):
        return self.__size

    def get_position(self):
        # return(self.x, self.y)
        if self.__orientation == "horizontal":
            i = self.x
            j = self.y
            h = True
        elif self.__orientation == "vertical":
            i = self.y
            j = self.x
            h = False

        for j in range(j, j+self.__size):
            yield (i,j) if h else (j,i)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_orientation(self):
        return self.__orientation

    def set_orientation(self, orientation):
        if orientation in ["horizontal", "vertical"]:
            self.__orientation = orientation


if __name__ == '__main__':
    main()