# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 20:03:27 2023

@author: rsmid
"""

import numpy as np
from Game_of_15_finalV import Game

class Attack(Game):
    def __init__(self):
        #self._evens = [2,4,6,8]
        #self._odds = [1,3,5,7,9]
        #self._gameboard = np.zeros(shape=(3,3))
        Game.__init__(self)
        self.next_move = 0
        self.turn = 1
        
        self.recent_even = 0
        self.odd_on_threath_vector = 0
        self.temp_gameboard = np.zeros(shape=(3,3), dtype=int)
        self.start_digit = 0
        
        
    def get_remaining_evens(self):
        return self._evens
    #def get_gameboard(self):
        #return self._gameboard
    def get_temp_gameboard(self):
        return self.temp_gameboard
    def copy_gameboard(self):
        self.temp_gameboard=self.get_gameboard().copy()
        return self.temp_gameboard
    
    ### THIS FUNCTION ONLY FOR TESTING
    #def set_remaining_odds(self, digit):
        #self._odds.remove(digit)
    
    def read_gameboard(self, lst):
        if len(lst)==9:
            gb = np.array(lst)
            
            new_even = list(set(self._evens)& set(lst))[0]
            
            ## save last added even (for kill_vector)
            self.recent_even=new_even
            
            self._evens.remove(new_even)
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
            digits = self._odds
        elif situation=='L':
            digits = self._evens
            
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
                                    vector=row
                                    for a in range(3):
                                        if str(vector[a]) in "13579":
                                            self.odd_on_threath_vector=a
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
                                    vector=col
                                    for a in range(3):
                                        if str(vector[a]) in "13579":
                                            self.odd_on_threath_vector=a
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
                                        vector=dgnl
                                        for a in range(3):
                                            if str(vector[a]) in "13579":
                                                self.odd_on_threath_vector=a
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
                                        vector=dgnl
                                        for a in range(3):
                                            if str(vector[a]) in "13579":
                                                self.odd_on_threath_vector=a
                                    return True
        
        return False
        
       
    
    ## allows two step validation (post-condition)                
    def potential_threat(self,i,j,digit):
        
        self.copy_gameboard()
        gameboard=self.get_temp_gameboard()
        if gameboard[i,j]==0:
            ## check that digit is odd (and still usable)
            if digit in self._odds:
                gameboard[i,j]=digit
                #print(self.get_temp_gameboard())
            else:
                print('Invalid digit')
        else:
            print('Invalid move')
            
        digits = self._evens
            
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
                            ## true if no zeros
                            if np.count_nonzero(row)==2:
                                return True
                        
                        ## columns
                        elif query=='col':
                            ## test if the vector has exactly one empty space
                            ## true if no zeros
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
    
    ## just a function to pick random number from a set
    def spin_the_wheel(self, num_outcomes):
        x=np.arange(num_outcomes)
        return np.random.choice(x)
    
    ## function to call when starting the attack (1st move on an empty board)
    def blind_dart(self):
        ## desireable grids 01 12 21 10 for evens 
        ### (populating these reduces evens potential to defend)
        ### we like to start by populating one of these
        desireable_grid_loc_lst = [(0,1),(1,2),(2,1),(1,0)]
        grid_loc_left=[]
        for loc in desireable_grid_loc_lst:
            i,j = loc
            if self.get_gameboard()[i][j]==0:
                grid_loc_left.append(loc)
        try:
            options=self._odds.copy()
            
            ## if first round, don't use 5
            if self.turn==1:
                options.remove(5)
                
            rand_idx=self.spin_the_wheel(len(options))
            digit = options[rand_idx]
            rand_idx2=self.spin_the_wheel(len(grid_loc_left))
            i,j = grid_loc_left[rand_idx2]
            
            self.next_move = (i,j,digit)
            return True
        except:
            return False
    
    def kill_vector(self, present_odd):
        if present_odd==1:
            return 7
        elif present_odd==7:
            return 1
        elif present_odd==3:
            return 9
        elif present_odd==9:
            return 3
        else:
            return None
        
    def pick_random_digit(self):
        rand_idx = np.random.randint(len(self._odds))
        return self._odds[rand_idx]
                
    def play(self,i,j,digit): 
        ## check if the index position is available (not necessary anymore [double check])
        #i,j,digit = self.next_move
        if self._gameboard[i,j]==0:
            ## check that digit is odd (and still usable)
            if digit in self._odds:
                self._gameboard[i,j]=digit
                self.turn+=1
                self._odds.remove(digit)
                print(self.get_gameboard())
            else:
                print('Invalid digit')
        else:
            print('Invalid move')
            
            
    def start_game(self):
        ## start the game by "blindly" throwing dart around the centre
        if self.blind_dart()==True:
            i,j,digit = self.next_move
            self.play(i, j, digit)
            self.start_digit= digit
    
    ## start executing the short game plan
    ## if first even in the corner (x: even, y: odd)
    ## [0 1 0]  [0 1 0]  [0 1 0]  [x 1 x]  [0 1 0]
    ## [y 0 0]  [0 0 y]  [y 0 y]  [x 0 x]  [0 x 0]
    ## [0 0 x]  [x 0 0]  [0 x 0]  [0 y 0]  [0 y 0]
    ## y=3      y=3      y=9      y=9      y=3 or y=7
    ## 
    def short_game(self):
        
        def which_digit(start_odd, answer_even, situation):
            if situation=='corner':
                if start_odd == 1:
                    digit=3
                elif start_odd == 3:
                    digit=1
                elif start_odd == 7:
                    digit=9
                elif start_odd == 9:
                    digit=7
                return digit
            elif situation=='force':
                if start_odd == 1:
                    digit=9
                elif start_odd == 3:
                    digit=7
                elif start_odd == 7:
                    digit=3
                elif start_odd == 9:
                    digit=1
                return digit
            elif situation=='bait':
                if start_odd == 1:
                    if answer_even==2:
                        digit=3
                    elif answer_even==4:
                        digit=7
                elif start_odd == 3:
                    if answer_even==2:
                        digit=1
                    elif answer_even==6:
                        digit=9
                elif start_odd == 7:
                    if answer_even==4:
                        digit=1
                    elif answer_even==8:
                        digit=9
                elif start_odd == 9:
                    if answer_even==6:
                        digit=3
                    elif answer_even==8:
                        digit=7
                return digit
        ## need to figure out which digit we played first and where
        ## where did the opponent put their 
        ## (assume it is in a position that doesn't threathen us immeadiately)
        if self.threath_opportunity('L')!=True and self.turn==2:
            #print('checkpoint 1')
            start_odd = self.start_digit
            answer_even = self.recent_even ## only needed for the middle model
            
            odd_loc =(3,3)
            even_loc =(3,3)
            
            ## find locations
            for i in range(3):
                for j in range(3):
                    if self.get_gameboard()[i][j]==start_odd:
                        odd_loc = (i,j)
                        #print(odd_loc)
                    elif self.get_gameboard()[i][j]==answer_even:
                        even_loc = (i,j)
                        #print(even_loc)
                        
            ## 4 possible starting grids, 4 possible starting digits
            
            ## start: up centre (0,1)
            if odd_loc==(0,1):
                if even_loc == (2,0):
                    i,j = (1,2)
                    ## digit based on start_digit
                    digit = which_digit(start_odd, answer_even, 'corner')
                    self.next_move=(i,j,digit)
                elif even_loc == (2,2):
                    i,j = (1,0)
                    ## digit based on start_digit
                    digit = which_digit(start_odd, answer_even, 'corner')
                    self.next_move=(i,j,digit)
                elif even_loc == (2,1):
                    i,j = (1,0)
                    ## digit based on start_digit
                    digit = which_digit(start_odd, answer_even, 'corner')
                    self.next_move=(i,j,digit)
                elif even_loc == (1,1):
                    i,j = (2,1)
                    digit = which_digit(start_odd, answer_even, 'bait')
                    self.next_move=(i,j,digit)
                else:
                    i,j = (2,1)
                    digit = which_digit(start_odd, answer_even, 'force')
                    self.next_move=(i,j,digit)
            
            ## start: left centre (1,0)
            elif odd_loc==(1,0):
                if even_loc == (0,2):
                    i,j = (2,1)
                    digit = which_digit(start_odd, answer_even, 'corner')
                    self.next_move=(i,j,digit)
                elif even_loc == (2,2):
                    i,j = (0,1)
                    digit = which_digit(start_odd, answer_even, 'corner')
                    self.next_move=(i,j,digit)
                elif even_loc == (1,2):
                    i,j = (0,1)
                    digit = which_digit(start_odd, answer_even, 'corner')
                    self.next_move=(i,j,digit)
                elif even_loc == (1,1):
                    i,j = (1,2)
                    digit = which_digit(start_odd, answer_even, 'bait')
                    self.next_move=(i,j,digit)
                else:
                    i,j = (1,2)
                    digit = which_digit(start_odd, answer_even, 'force')
                    self.next_move=(i,j,digit)
            
            ## start: right centre (1,2)
            elif odd_loc==(1,2):
                if even_loc == (0,0):
                    i,j = (2,1)
                    digit = which_digit(start_odd, answer_even, 'corner')
                    self.next_move=(i,j,digit)
                elif even_loc == (2,0):
                    i,j = (0,1)
                    digit = which_digit(start_odd, answer_even, 'corner')
                    self.next_move=(i,j,digit)
                elif even_loc == (1,0):
                    i,j = (0,1)
                    digit = which_digit(start_odd, answer_even, 'corner')
                    self.next_move=(i,j,digit)
                elif even_loc == (1,1):
                    i,j = (1,0)
                    digit = which_digit(start_odd, answer_even, 'bait')
                    self.next_move=(i,j,digit)
                else:
                    i,j = (1,0)
                    digit = which_digit(start_odd, answer_even, 'force')
                    self.next_move=(i,j,digit)
                
            ## start: bottom centre (2,1)
            elif odd_loc==(2,1):
                if even_loc == (0,0):
                    i,j = (1,2)
                    digit = which_digit(start_odd, answer_even, 'corner')
                    self.next_move=(i,j,digit)
                elif even_loc == (0,2):
                    i,j = (1,0)
                    digit = which_digit(start_odd, answer_even, 'corner')
                    self.next_move=(i,j,digit)
                elif even_loc == (0,1):
                    i,j = (1,0)
                    digit = which_digit(start_odd, answer_even, 'corner')
                    self.next_move=(i,j,digit)
                elif even_loc == (1,1):
                    i,j = (0,1)
                    digit = which_digit(start_odd, answer_even, 'bait')
                    self.next_move=(i,j,digit)
                else:
                    i,j = (0,1)
                    digit = which_digit(start_odd, answer_even, 'force')
                    self.next_move=(i,j,digit)

    ## game strategy after the first move        
    def answer(self):
       
        ## check first if win one move away
        if self.threath_opportunity('W')==True:
            i,j,digit = self.next_move
            self.play(i,j,digit)
            print('odd wins.')    
        ## minimax
        elif self.turn>2:
            board = self.get_gameboard()
            i,j,digit = self.minimax(board)
            
            ## use attack with minimax instead of play (could be integrated to one method)
            self.attack(i,j,digit)
            self.turn+=1
            
        ## check for immediate threat
        elif self.threath_opportunity('L')==True:
            i,j = self.next_move
            ## in threath, answer with digit that doesn't form 15 with
            ## the odd digit present on the threath vector
            ## (pairings 3 & 9 and 1 & 7)
            ## if need to populate middle, use 5
            if i==1 and j==1:
                digit=5
            else:  
                potential_digit = self.kill_vector(self.odd_on_threath_vector)
                if potential_digit != None:
                    digit = potential_digit
                else:
                    digit = self.pick_random_digit()
            ### NOT FULLY IMPLEMENTED YET
            
            ## check that our next move doesn't do any harm 
            ## (in our game strategy we only use this on the second turn 
            ## as minimax will take of the rest)
            if self.potential_threat(i,j,digit)!=True:
                self.play(i,j,digit)
            else:
                print("need to run a different digit")
        
        else:
        
            ### NEED A HEURISTIC if even doesn't threathen (as is in 50% of the cases)
            ## start executing the short game plan
            if self.turn==2:
                self.short_game()
                i,j,digit = self.next_move
                self.play(i, j, digit)
        
            
    ## function to return the gameboard as a list
    def output_gameboard(self):
        return self._gameboard.reshape(1,9).tolist()[0]