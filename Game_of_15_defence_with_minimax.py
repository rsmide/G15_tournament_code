# -*- coding: utf-8 -*-
"""
Burnley defence with short cake strategy 
and baby versions of kill vector and blind dart

Created on Tue Feb 21 19:16:21 2023

@author: rsmid
"""

import numpy as np
from Game_of_15_finalV import Game

class Burnley(Game):
    def __init__(self):
        #self._evens = [2,4,6,8]
        #self._odds = [1,3,5,7,9]
        #self._gameboard = np.zeros(shape=(3,3))
        Game.__init__(self)
        
        self.next_move = 0
        self.turn = 1
        self.recent_odd = 0
        
        self.temp_gameboard = np.zeros(shape=(3,3), dtype=int)
        
    def get_remaining_odds(self):
        return self._odds
    #def get_gameboard(self):
        #return self._gameboard
    def get_temp_gameboard(self):
        return self.temp_gameboard
    def copy_gameboard(self):
        self.temp_gameboard=self.get_gameboard().copy()
        return self.temp_gameboard
    
    ### THIS FUNCTION ONLY FOR TESTING
    #def set_remaining_evens(self, digit):
        #self._evens.remove(digit)
    
    def read_gameboard(self, lst):
        if len(lst)==9:
            gb = np.array(lst)
            
            new_odd = list(set(self._odds)& set(lst))[0]
            
            ## save last added odd (for kill_vector)
            self.recent_odd=new_odd
            
            self._odds.remove(new_odd)
            new_board = gb.reshape(3,3)
            self._gameboard=new_board
        else:
            print('Invalid input')
        
    def evaluate_vectors(self, query):
        ## row, column & diagonal sums
        if query=="row":
            return self._gameboard.sum(axis=1)
        elif query=="col":
            return self._gameboard.sum(axis=0)
        elif query=="dgnl":
            principal = 0
            secondary = 0
            for i in range(0, 3):
                principal += self._gameboard[i][i]
                secondary += self._gameboard[i][3 - i - 1]
            return principal, secondary
        
    def threath_opportunity(self, situation):
        gameboard=self.get_gameboard()
            
        ## determine whether looking for potential win or avoiding loss
        if situation=='W':
            digits = self._evens
        elif situation=='L':
            digits = self._odds
            
        query_lst = ['row', 'col', 'dgnl']
        for query in query_lst:
            ## idx 0,1,2 for rows and cols & 0,1 for dgnls
            for idx in range(len(self.evaluate_vectors(query))):
                for digit in digits:
                    ## find instances where a vector is one digit away from 15
                    if self.evaluate_vectors(query)[idx]+digit==15:
                        
                        ## next conditions based on type of vector
                        
                        ## rows
                        if query=='row':
                            i=idx
                            row = gameboard[i]
                            ## test if the vector has exactly one empty space
                            ## true if no zeros
                            if np.count_nonzero(row)==2:
                                j = np.where(row == 0)[0][0]
                                ## next move depends on W or L
                                if situation=='W':
                                    self.next_move = (i,j,digit)
                                else:
                                    self.next_move = (i,j)

                                return True
                        
                        ## columns
                        elif query=='col':
                            ## test if the vector has exactly one empty space
                            ## true if no zeros
                            j=idx
                            col = gameboard[:,j]
                            if np.count_nonzero(col)==2:
                                i = np.where(col == 0)[0][0]
                                ## next move depends on W or L
                                if situation=='W':
                                    self.next_move = (i,j,digit)
                                else:
                                    self.next_move = (i,j)

                                return True
                        
                        ## diagonals
                        elif query=='dgnl':
                            ## check whether principal or secondary diagonal
                        
                            if idx == 0:
                                # principal
                                dgnl = gameboard.diagonal()
                                if np.count_nonzero(dgnl)==2:
                                
                                    for index in range(0,3):
                                        if self._gameboard[index][index] == 0:
                                            i,j=index,index


                                    if situation=='W':
                                        self.next_move = (i,j,digit)
                                    else:
                                        self.next_move = (i,j)

                                    return True
                            else:
                                # secondary
                                
                                dgnl = np.flipud(gameboard).diagonal()
                                if np.count_nonzero(dgnl)==2:
                                
                                    for index in range(0,3):
                                        if self._gameboard[index][3 - index - 1]==0:
                                            i,j=index,3-index-1
                                
                                    if situation=='W':
                                        self.next_move = (i,j,digit)
                                    else:
                                        self.next_move = (i,j)

                                    return True
        
        return False
    
                    
    ## allows two step validation (post-condition)                
    def potential_threat(self,i,j,digit):
        
        self.copy_gameboard()
        gameboard=self.get_temp_gameboard()
        if gameboard[i,j]==0:
            ## check that digit is odd (and still usable)
            if digit in self._evens:
                gameboard[i,j]=digit
                #print(self.get_temp_gameboard())
            else:
                print('Invalid digit')
        else:
            print('Invalid move')
            
        digits = self._odds
            
        query_lst = ['row', 'col', 'dgnl']
        for query in query_lst:
            ## idx 0,1,2 for rows and cols & 0,1 for dgnls
            for idx in range(len(self.evaluate_vectors(query))):
                for digit in digits:
                    ## find instances where a vector is one digit away from 15
                    if self.evaluate_vectors(query)[idx]+digit==15:
                        
                        ## next conditions based on type of vector
                        
                        ## rows
                        if query=='row':
                            row = gameboard[i]
                            ## test if the vector has exactly one empty space
                            
                            if np.count_nonzero(row)==2:
                                return True
                        
                        ## columns
                        elif query=='col':
                            ## test if the vector has exactly one empty space
                            
                            col = gameboard[:,j]
                            if np.count_nonzero(col)==2:
                                return True
                        
                        ## diagonals
                        elif query=='dgnl':
                            ## check whether principal or secondary diagonal
                        
                            if idx == 0:
                                # principal
                                dgnl = gameboard.diagonal()
                                if np.count_nonzero(dgnl)==2:
                                    return True
                            else:
                                # secondary
                                dgnl = np.flipud(gameboard).diagonal()
                                if np.count_nonzero(dgnl)==2:
                                    return True
        
        return False
    
    def short_cake(self, turn):
        ## our next move should put any even in any corner
        if turn=='first':
            ## check if odd started with middle 5
            if self.get_gameboard()[1][1]==5:
                ## pick random pair of index (00, 02, 20, 22)
                pool = np.repeat([0,2,0,2],3)
                i,j = pool[np.random.randint(12)], pool[np.random.randint(12)]
                digit = self.pick_random_digit()
                self.next_move = (i,j,digit)
                return True
            else:
                return False
            
        elif turn=='second':
            odd_played=0
            even_played=0
            cake_offered = True
            ## check if the opponent reacted with the 'wrong' digit
            ## first find which diagonal is used (should be full by this point)
            dgnl = self.get_gameboard().diagonal()
            #secnd = np.flipud(self.get_gameboard()).diagonal()
            if np.all(dgnl)==True: ## principal true (check places 00, 22)
                if self.get_gameboard()[0][0]%2==0:
                    odd_played= self.get_gameboard()[2][2]
                    even_played= self.get_gameboard()[0][0]
                    if (even_played==2 and odd_played==1):
                        self.next_move = (2,1,6)
                    elif (even_played==2 and odd_played==3):
                        self.next_move = (1,2,4)
                    elif (even_played==4 and odd_played==7):
                        self.next_move = (2,1,2)
                    elif (even_played==4 and odd_played==1):
                        self.next_move = (1,2,8)
                    elif (even_played==6 and odd_played==9):
                        self.next_move = (1,2,2)
                    elif (even_played==6 and odd_played==3):
                        self.next_move = (2,1,8)
                    elif (even_played==8 and odd_played==7):
                        self.next_move = (1,2,6)
                    elif (even_played==8 and odd_played==9):
                        self.next_move = (2,1,4)
                    else:
                        cake_offered=False
                else:
                    odd_played= self.get_gameboard()[0][0]
                    even_played= self.get_gameboard()[2][2]
                    if (even_played==2 and odd_played==1):
                        self.next_move = (1,0,6)
                    elif (even_played==2 and odd_played==3):
                        self.next_move = (0,1,4)
                    elif (even_played==4 and odd_played==7):
                        self.next_move = (1,0,2)
                    elif (even_played==4 and odd_played==1):
                        self.next_move = (0,1,8)
                    elif (even_played==6 and odd_played==9):
                        self.next_move = (0,1,2)
                    elif (even_played==6 and odd_played==3):
                        self.next_move = (1,0,8)
                    elif (even_played==8 and odd_played==7):
                        self.next_move = (0,1,6)
                    elif (even_played==8 and odd_played==9):
                        self.next_move = (1,0,4)
                    else:
                        cake_offered=False
            else:
                # implement secondary diagonal                                     
                if self.get_gameboard()[2][0]%2==0:
                    odd_played= self.get_gameboard()[0][2]
                    even_played= self.get_gameboard()[2][0]
                    if (even_played==2 and odd_played==1):
                        self.next_move = (0,1,6)
                    elif (even_played==2 and odd_played==3):
                        self.next_move = (1,2,4)
                    elif (even_played==4 and odd_played==7):
                        self.next_move = (0,1,2)
                    elif (even_played==4 and odd_played==1):
                        self.next_move = (1,2,8)
                    elif (even_played==6 and odd_played==9):
                        self.next_move = (1,2,2)
                    elif (even_played==6 and odd_played==3):
                        self.next_move = (0,1,8)
                    elif (even_played==8 and odd_played==7):
                        self.next_move = (1,2,6)
                    elif (even_played==8 and odd_played==9):
                        self.next_move = (0,1,4)
                    else:
                        cake_offered=False
                else:
                    odd_played= self.get_gameboard()[2][0]
                    even_played= self.get_gameboard()[0][2]
                    if (even_played==2 and odd_played==1):
                        self.next_move = (2,1,6)
                    elif (even_played==2 and odd_played==3):
                        self.next_move = (1,0,4)
                    elif (even_played==4 and odd_played==7):
                        self.next_move = (2,1,2)
                    elif (even_played==4 and odd_played==1):
                        self.next_move = (1,0,8)
                    elif (even_played==6 and odd_played==9):
                        self.next_move = (1,0,2)
                    elif (even_played==6 and odd_played==3):
                        self.next_move = (2,1,8)
                    elif (even_played==8 and odd_played==7):
                        self.next_move = (1,0,6)
                    elif (even_played==8 and odd_played==9):
                        self.next_move = (2,1,4)
                    else:
                        cake_offered=False

            if cake_offered==True:
                return True
            else:
                return False
            
    ## attack the starting digit        
    ## based on odds starting move
    def threathen_first(self):
        
        if self.get_gameboard()[1][1]!=5: ## otherwise would use short_cake
        
            ## find odds starting location
            location=0
            for i in range(0,3):
                for j in range(0,3):
                    if self.get_gameboard()[i][j]==self.recent_odd:
                        location = (i,j)
                        break
                    
            ## based on odds starting location choose answer loc for even
            if location!=0:
                if location == (0,0):
                    desireable_grid_loc_lst = [(0,1),(1,0)]
                    rand_idx = self.spin_the_wheel(len(desireable_grid_loc_lst))
                    i,j = desireable_grid_loc_lst[rand_idx]
                elif location == (0,1):
                    i,j = (2,1)
                elif location == (0,2):
                    desireable_grid_loc_lst = [(0,1),(1,2)]
                    rand_idx = self.spin_the_wheel(len(desireable_grid_loc_lst))
                    i,j = desireable_grid_loc_lst[rand_idx]
                elif location == (1,0):
                    i,j = (1,2)
                elif location == (1,1):
                    desireable_grid_loc_lst = [(0,1),(1,2),(2,1),(1,0)]
                    rand_idx = self.spin_the_wheel(len(desireable_grid_loc_lst))
                    i,j = desireable_grid_loc_lst[rand_idx]
                elif location == (1,2):
                    i,j = (1,0)
                elif location == (2,0):
                    desireable_grid_loc_lst = [(1,0),(2,1)]
                    rand_idx = self.spin_the_wheel(len(desireable_grid_loc_lst))
                    i,j = desireable_grid_loc_lst[rand_idx]
                elif location == (2,1):
                    i,j = (0,1)
                elif location == (2,2):
                    desireable_grid_loc_lst = [(1,2),(2,1)]
                    rand_idx = self.spin_the_wheel(len(desireable_grid_loc_lst))
                    i,j = desireable_grid_loc_lst[rand_idx]

            
            ## assign which digit to play
            if self.recent_odd==1:
                ## play 6 or 8
                options=[6,8]
                rand_idx=self.spin_the_wheel(2)
                digit = options[rand_idx]
                self.next_move = (i,j,digit)
                
            elif self.recent_odd==3:
                ## play 4 or 8
                options=[4,8]
                rand_idx=self.spin_the_wheel(2)
                digit = options[rand_idx]
                self.next_move = (i,j,digit)
                
            elif self.recent_odd==5:
                ## play any
                options=[2,4,6,8]
                rand_idx=self.spin_the_wheel(4)
                digit = options[rand_idx]
                self.next_move = (i,j,digit)
                
            elif self.recent_odd==7:
                ## play 2 or 6
                options=[2,6]
                rand_idx=self.spin_the_wheel(2)
                digit = options[rand_idx]
                self.next_move = (i,j,digit)
                
            elif self.recent_odd==9:
                ## play 2 or 4
                options=[2,4]
                rand_idx=self.spin_the_wheel(2)
                digit = options[rand_idx]
                self.next_move = (i,j,digit)
    
    def spin_the_wheel(self, num_outcomes):
        x=np.arange(num_outcomes)
        return np.random.choice(x)
    
    def blind_dart(self):
        ## desireable grids 01 12 21 10 for evens 
        ### (populating these reduces odds potential winning scenarios)
        desireable_grid_loc_lst = [(0,1),(1,2),(2,1),(1,0)]
        grid_loc_left=[]
        for loc in desireable_grid_loc_lst:
            i,j = loc
            if self.get_gameboard()[i][j]==0:
                grid_loc_left.append(loc)
        try:
            options=self._evens
            rand_idx=self.spin_the_wheel(len(options))
            digit = options[rand_idx]
            rand_idx2=self.spin_the_wheel(len(grid_loc_left))
            i,j = grid_loc_left[rand_idx2]
            
            self.next_move = (i,j,digit)
            return True
        except:
            return False
    
    def pick_random_digit(self):
        rand_idx = np.random.randint(len(self._evens))
        return self._evens[rand_idx]
                
    def play(self,i,j,digit): 
        ## check if the index position is available (not necessary anymore [double check])
        #i,j,digit = self.next_move
        if self._gameboard[i,j]==0:
            ## check that digit is even (and still usable)
            if digit in self._evens:
                self._gameboard[i,j]=digit
                self.turn+=1
                self._evens.remove(digit)
                print(self.get_gameboard())
            else:
                print('Invalid digit')
        else:
            print('Invalid move')
    
    def answer(self):
       
        ## check first if win one move away
        if self.threath_opportunity('W')==True:
            i,j,digit = self.next_move
            self.play(i,j,digit)
            print('even wins.')
            
        ### defensive game start heuristic #1
        elif (self.turn==1) and (self.short_cake('first')==True):
            i,j,digit = self.next_move
            self.play(i, j, digit)
        
        ### defensive game start heuristic #2
        elif (self.turn==1) and (self.short_cake('first')==False):
            self.threathen_first()
            i,j,digit = self.next_move
            self.play(i, j, digit)
            
        ### gsh #1 continued        
        elif (self.turn==2) and (self.short_cake('second')==True):
            i,j,digit = self.next_move
            self.play(i, j, digit)
            print('checkmate.')
            
        ## minimax
        elif self.turn>1:
            board = self.get_gameboard()
            i,j,digit = self.minimax(board)
            
            ## use defend with minimax instead of play (could be integrated to one method)
            self.defend(i,j,digit)
            self.turn+=1
            
        ## check for immediate threat
        elif self.threath_opportunity('L')==True:
            i,j = self.next_move
            ## if threath sum is 10, pick the digit that is the remainder when
            ## odds are subtracted (9-1->8 & 7-3->4)
            ### NOT IMPLEMENTED YET
            digit = self.pick_random_digit() 
            ## check that our next move doesn't do any harm
            if self.potential_threat(i,j,digit)!=True:
                self.play(i,j,digit)
            else:
                print("need to run a different digit")

        ###
        ### first 2 moves, avoid populating 2/3 of an empty vector with evens
        ###
        
        ## this method ahould not be used
        elif self.blind_dart()==True:
            print('CAUTION: blind dart!')
            i,j,digit = self.next_move
            self.play(i, j, digit)
        else:
            print('Not yet determined')
    
    ## function to return the gameboard as a list
    def output_gameboard(self):
        return self._gameboard.reshape(1,9).tolist()[0]