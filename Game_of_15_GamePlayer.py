# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 19:40:34 2023

@author: rsmid
"""

from Game_of_15_attack_with_minimax_v2 import Attack
from Game_of_15_defence_with_minimax import Burnley

def play_game():
    player=input("Are you playing with odds or evens?: ")
    if player.lower() in ['odds','o']:
        game = Attack()
        start = input('Are you ready to start the game?: ')
        if start.lower() in ['yes','y']:
            game.start_game()
            print("\nGameboard as a list:", game.output_gameboard())
            
            while(game.terminal(game.get_gameboard())==False):
                
                input_board = input('Please input the opponent board as a list w/o brackets: ')
                input_board_lst = input_board.split(",")
                try:
                    if len(input_board_lst)==9:
                        current_board = [int(input_board_lst[i]) for i in range(len(input_board_lst))]
                        game.read_gameboard(current_board)
                
                        game.answer()
                        print("\nGameboard as a list:", game.output_gameboard())
                    else:
                        print('Invalid input; try again.')
                except:
                    print('Something went wrong :(')
            print('\nGame Over.')
            
            
    elif player.lower() in ['evens','e']:
        game = Burnley()
        
        ## wait for odd to start
        print('Waiting for odd to start...')
        while(game.terminal(game.get_gameboard())==False):
            
            input_board = input('Please input the opponent board as a list w/o brackets: ')
            input_board_lst = input_board.split(",")
            try:
                if len(input_board_lst)==9:
                    current_board = [int(input_board_lst[i]) for i in range(len(input_board_lst))]
                    game.read_gameboard(current_board)
            
                    game.answer()
                    print("\nGameboard as a list:", game.output_gameboard())
                else:
                    print('Invalid input; try again.')
            except:
                print('Something went wrong, try again!')
        print('\nGame Over.')
    