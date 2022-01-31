#!/usr/bin/python3

import random
import math
import os
import time
from functools import reduce

class Socrates:

    def __init__(self):
        self.position=None

    def start(self):
        print("Socrates says start")
        self.position = [board.XMAX//2, board.YMAX//2]

    def turn(self):
        choice = memory.pick()
        if choice != None:
            self.move(choice)
        else:
            print("Socrates appears to have won!")

    def move(self,choice):
        move = self.direction(choice)
        new_position = [self.position[0] + move[0], 
                        self.position[1] + move[1]]
        if (board.is_on_board(new_position)):
            print("Socrates moves %s\n" % (self.direction_name(choice)))
            self.position = new_position
            #board.add_to_trail(self.position[0], self.position[1], 's')
        else:
            print("Socrates can't move %s off board\n" % (self.direction_name(choice)))

    def direction(self,choice):
        if (choice == deck.HEARTS):
            return board.DOWN
        elif (choice == deck.CLUBS):
            return board.LEFT
        elif (choice == deck.DIAMONDS):
            return board.RIGHT
        elif (choice == deck.SPADES):
            return board.UP
        else:
            raise Exception("can't happen")

    def direction_name(self,choice):
        if (choice == deck.HEARTS):
            return "down"
        elif (choice == deck.CLUBS):
            return "left"
        elif (choice == deck.DIAMONDS):
            return "right"
        elif (choice == deck.SPADES):
            return "up"
        else:
            raise Exception("can't happen")

    def lost(self):
        return hound.won()

    def won(self):
        return not(self.lost()) and deck.empty()

class Hound:
    def __init__(self):
        self.position = None
        self.dir = None

    def start(self):
        self.position = [1, board.YMAX-2]
        self.dir = board.RIGHT

    def turn(self):
        move = self.direction()
        if move != None:
            self.dir = move
        else:
            move = self.dir
        self.position = [self.position[0] + move[0], 
                         self.position[1] + move[1]]
        if not board.is_on_board(self.position):
            raise Exception("Hound moved to %s off board" % (self.position))
        #board.add_to_trail(self.position[0], self.position[1], 'h')
        
    def direction(self):
        (x,y) = self.position
        if (x == 1 and y == 1):
            return board.UP
        if (x == 1 and y == board.YMAX-2):
            return board.RIGHT
        if (x == board.XMAX-2 and y == board.YMAX-2):
            return board.DOWN
        if (x == board.XMAX-2 and y == 1):
            return board.LEFT
        return None

    def won(self):
        return (self.position == socrates.position)

class Deck:
    N_DECKS = 4

    HEARTS = 0
    CLUBS = 1
    DIAMONDS = 2
    SPADES = 3

    def __init__(self):
        self.cards = None

    def start(self):
        print("Deck says start")
        self.cards = [13 * self.N_DECKS] * 4

    def deal(self):
        choice = random.randint(0,3)
        n = self.cards[choice]
        if (n > 0):
            self.cards[choice] = n-1
            return choice
        elif self.empty():
            return None
        else:
            return self.deal()

    def empty(self):
        return (reduce((lambda x,y :x+y), self.cards) == 0)

class Memory:
    forget_n = 5

    def __init__(self):
        stack = None
        point = None

    def start(self):
        self.stack = []
        self.point = None


    def pick(self):
        choice = None
        if self.point != None:
            print("stack len %d point %d" % (len(self.stack), self.point))
        else:
            print("stack len %d" % len(self.stack))

        if self.point != None and self.point < len(self.stack):
            choice = self.stack[self.point]
            self.point += 1
            if self.point > len(self.stack):
                self.point = None
        else:
            choice = deck.deal()
            if choice != None:
                self.stack.append(choice)
        print("stack %s %s" % ("".join(map(lambda x : ['R','L','D','U'][x], self.stack[0:self.point])),
                               "".join(map(lambda x : ['R','L','D','U'][x], self.stack[self.point:]))))
        return choice

    def replay(self):
        print("Replay")
        self.point = 0
        if self.forget_n < len(self.stack):
            print("Forgetting last %d moves" % (self.forget_n))
            self.stack = self.stack[0 : -self.forget_n]
        else:
            print("Forgetting all moves")
            self.stack = []
    
    def show(self):
        print("Memory: %s" % (self.stack))

class Board:
    XMAX = 9
    YMAX = 9
    UP = (0,1)
    DOWN = (0,-1)
    LEFT = (-1,0)
    RIGHT = (1,0)

    def __init__(self):
        self.move = 0
        self.trail = self.matrix(self.XMAX, self.YMAX)

    # http://dada.perl.it/shootout/matrix.python.html
    def matrix(self, xmax, ymax):
        count = 1
        m = [ None ] * xmax
        for i in range(xmax):
            m[i] = [None] * ymax
            for j in range(ymax):
                m[i][j] = None
        return m


    def add_to_trail(self,x,y,s):
        old = self.trail[x][y]
        if old is None:
            self.trail[x][y] = s
        elif old != s:
            self.trail[x][y] = '*'
        
    def start(self):
        print("Board says start")
        deck.start()
        memory.start()
        self.play()

    def play(self):
        while not deck.empty() and not socrates.won():
            move = 0
            hound.start()
            socrates.start()
            self.show()
            while not hound.won() and not socrates.won():
                self.clear()
                self.move += 1
                hound.turn()
                socrates.turn()
                self.show()
                self.pause()
            if hound.won():
                print("Hound won")
                memory.replay()
                self.long_pause()
            elif socrates.won():
                print("Socrates won")
                return

    def is_on_board(self, position):
        (x,y) = position
        if x < 0 or y < 0:
            return False
        if x >= self.XMAX or y >= self.YMAX:
            return False
        return True

    def show(self):
        print("Move %d: Socrates=%s Hound=%s" % (self.move, socrates.position, hound.position))
        saw_socrates = False
        saw_hound = False
        for y in range(self.YMAX-1, -1, -1):
            for x in range(self.XMAX):
                position = [x,y]
                if socrates.position == position and hound.position == position:
                    print("X", end='')
                    saw_socrates = True
                    saw_hound = True
                if socrates.position == position:
                    print("S", end='')
                    saw_socrates = True
                elif hound.position == position:
                    print("H", end='')
                    saw_hound = True
                elif self.trail[x][y] != None:
                    print(self.trail[x][y], end='')
                else:
                    print(".", end='')

            print()
        print
        if saw_socrates and saw_hound:
            return
        print("Move %d: Socrates=%s Hound=%s\n" % (self.move, socrates.position, hound.position))
        if not saw_socrates:
            raise Exception("didn't see socrates")
        if not saw_hound:
            raise Exception("didn't see hound")

    def clear(self):
        os.system("clear")

    def pause(self):
        time.sleep(0.1)

    def long_pause(self):
        time.sleep(3)

deck = Deck()
memory = Memory()
socrates = Socrates()
hound = Hound()
board = Board()

board.start()


