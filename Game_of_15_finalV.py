# -*- coding: utf-8 -*-
"""
Example Game
Contains minimax functionality

Created on Tue Feb 21 18:29:35 2023

@author: rsmid
"""

import numpy as np
import copy
import math

class Game():
    ## create the gameboard
    def __init__(self):
        self._gameboard = np.zeros(shape=(3,3), dtype=int)
        self._odds = [1,3,5,7,9]
        self._evens = [2,4,6,8]
        
    def get_gameboard(self):
        return self._gameboard
    
    def get_gameboard_as_list(self):
        return self._gameboard.reshape(1,9).tolist()[0]
    
    def get_any_board_as_list(self, board):
        return board.reshape(1,9).tolist()[0]
    
    def get_remaining_digits(self, board):
        evens=[2,4,6,8]
        odds=[1,3,5,7,9]
        board_list = self.get_any_board_as_list(board)
        digits_used = "".join([str(elem) for elem in board_list if elem !=0])
        for even in [2,4,6,8]:
            if str(even) in digits_used:
                evens.remove(even)
        for odd in [1,3,5,7,9]:
            if str(odd) in digits_used:
                odds.remove(odd)
        return odds, evens
    
    def whos_turn(self, board):
        odds_count = 0
        evens_count = 0
        # simply iterate over the given 2D array and calculate how many odds and evens are there
        for y_axis in board: 
            for x_axis in y_axis:
                if x_axis!=0:
                    if x_axis%2!=0:
                        odds_count += 1
                    elif x_axis%2==0:
                        evens_count += 1
        # if number of odds is smaller or equal to evens, it is a turn for an odds because it always goes first
        if odds_count <= evens_count: 
            return 'odd'
        else:  # otherwise it is a turn for an O
            return 'even'
        
    def actions(self, board, remaining_digits):
        possible_actions = set() # set is used just to be sure there will only be unique tuples
        for y, y_axis in enumerate(board):
            for x, x_axis in enumerate(y_axis):
                for digit in remaining_digits:
                    # initial implementation puts variable EMPTY in all cells, which is equal to None
                    if x_axis == 0: 
                        possible_actions.add((y, x, digit))
        return possible_actions
    
    def result(self, board, action):
        if len(action) != 3:  # check if given action is a tuple of three elements
            raise Exception("result function: incorrect action")
        # check if given action is within the boundaries of the board (3x3)
        if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
            raise Exception("result function: incorrect action value")
        y, x = action[0], action[1]
        digit = action[2]
        board_copy = copy.deepcopy(board) # using the imported library 'copy'
        # check if action is already there (even though we will call 'actions' before it)
        if board_copy[y][x] != 0:
            raise Exception("suggested action has already been taken")
        else:  # here we use the player function to know which letter to put in the copy
            board_copy[y][x] = digit
        return board_copy

    def winner(self, board):
        ## check if the game is over
        if self.game_over(board):
            ## if the next turn would be odd -> even won
            ## if the next turn would be even -> odd won
            if self.whos_turn(board)=='odd':
                return 'even'
            else:
                return 'odd'

        return None
    
    def terminal(self, board):
        if self.winner(board) == 'even' or self.winner(board) == 'odd': # check if there is a winner
            return True
        # check if there is a tie (if no cells left and neither odd nor even won)
        elif 0 not in board[0] and 0 not in board[1] and 0 not in board[2]:
            return True
        else: # otherwise return that the game is still going on
            return False
        
    def utility(self, board):
        if self.winner(board) == 'odd':
            return 1
        elif self.winner(board) == 'even':
            return -1
        else:
            return 0
     
    def minimax(self, board):
        
        digits= self.get_remaining_digits(board)
        
        if self.terminal(board):
            return None
        if self.whos_turn(board) == 'odd':
            score = -math.inf
            action_to_take = None
            for action in self.actions(board, digits[0]):
                min_val = self.minvalue(self.result(board, action))
                if min_val > score:
                    score = min_val
                    action_to_take = action
                    #digits[0].remove(action[2])
            return action_to_take
        elif self.whos_turn(board) == 'even':
            score = math.inf
            action_to_take = None
            for action in self.actions(board, digits[1]):
                max_val = self.maxvalue(self.result(board, action))
                if max_val < score:
                    score = max_val
                    action_to_take = action
                    #digits[1].remove(action[2])
            return action_to_take
        
    def minvalue(self, board):
        # if game over, return the utility of state
        if self.terminal(board):
            return self.utility(board)
        # iterate over the available actions and return the minimum out of all maximums
        max_value = math.inf
        digits= self.get_remaining_digits(board)
        for action in self.actions(board, digits[1]):
            max_value = min(max_value, self.maxvalue(self.result(board, action)))
        return max_value
    
    def maxvalue(self,board):
        # if game over, return the utility of state
        if self.terminal(board):
            return self.utility(board)
        # iterate over the available actions and return the maximum out of all minimums
        min_val = -math.inf
        digits= self.get_remaining_digits(board)
        for action in self.actions(board, digits[0]):
            min_val = max(min_val, self.minvalue(self.result(board, action)))
        return min_val
                
    def evaluate_board(self, board, query):
        gameboard=board
        ## row, column & diagonal sums
        if query=="row":
            return gameboard.sum(axis=1)
        elif query=="col":
            return gameboard.sum(axis=0)
        elif query=="dgnl":
            principal = 0
            secondary = 0
            for i in range(0, 3):
                principal += gameboard[i][i]
                secondary += gameboard[i][3 - i - 1]
            return principal, secondary
        
    def game_over(self, board):
        gameboard = board
        query_lst = ['row', 'col', 'dgnl']
        for query in query_lst:
            for idx in range(len(self.evaluate_board(gameboard, query))):
                if self.evaluate_board(gameboard, query)[idx]==15:
                    ## rows
                    if query=='row':
                        i=idx
                        row = gameboard[i]
                        ## true if no zeros
                        if np.count_nonzero(row)==3:
                            return True
                    
                    ## columns
                    elif query=='col':
                        ## true if no zeros
                        j=idx
                        col = gameboard[:,j]
                        if np.count_nonzero(col)==3:
                            return True
                    
                    ## diagonals
                    elif query=='dgnl':
                        ## check whether principal or secondary diagonal
                    
                        if idx == 0:
                            # principal
                            dgnl = gameboard.diagonal()
                            if np.count_nonzero(dgnl)==3:
                                return True
                        else:
                            # secondary
                            dgnl = np.flipud(gameboard).diagonal()
                            if np.count_nonzero(dgnl)==3:
                                return True
        return False
                
    def attack(self,i,j,digit):
        ## check if the index position is available
        if self._gameboard[i,j]==0:
            ## check that digit is odd (and still usable)
            if digit in self._odds:
                self._gameboard[i,j]=digit
                self._odds.remove(digit)
                print(self.get_gameboard())
                if self.game_over(self.get_gameboard())==True:
                    return "odd wins."
            else:
                print('Invalid digit')
        else:
            print('Invalid move')
            
    def defend(self,i,j,digit):
        ## check if the index position is available
        if self._gameboard[i,j]==0:
            ## check that digit is even (and still usable)
            if digit in self._evens:
                self._gameboard[i,j]=digit
                self._evens.remove(digit)
                print(self.get_gameboard())
                if self.game_over(self.get_gameboard())==True:
                    return "even wins."
            else:
                print('Invalid digit')
        else:
            print('Invalid move')