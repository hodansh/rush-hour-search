from __future__ import annotations
from typing import List
import numpy as np
import copy

import utils


class BoardState():
    def __init__(self, board: List[List[str]], fuel: dict) -> None:
        self.board = board
        self.fuel = fuel

    def get_game_cars(self) -> List[str]:
        flat_board = np.array(self.board).flatten()
        board_string = ''.join(str(x) for x in flat_board) 
        return utils.get_cars(board_string)

    def has_fuel(self, vehicle: str) -> bool:
        return self.fuel[vehicle] > 0
    
    def spend_fuel(self, vehicle: str) -> None:
        self.fuel[vehicle] = self.fuel[vehicle] - 1

    def is_solved(self) -> bool:
        return (self.board[2][4] == 'A' and self.board[2][5] == 'A')

    #state of board (2D)
    def print_board(self) -> None:
        for row in self.board:
            for col in row:
                print(col, end=' ')
            print() # New line

    def get_board_string(self) -> str:
        flat_board = np.array(self.board).flatten()
        board_string = ''.join(str(x) for x in flat_board) 
        return board_string

    def print_board_1d(self) -> None:
        print(self.get_board_string())

    #fuel of all cars
    def print_fuel(self) -> None:
        print('Car fuel available: ', end=' ')
        for car in self.fuel:
            print(f'{car}: {self.fuel[car]}', end='  ')
        print()

    #check if vehicle is horizontal or not
    def is_horizontal(self, vehicle:str) -> bool:
        temp1 = ""
        temp2 = ""
        for row in self.board:
            for col in range(0, 5):
                temp1 = row[col]
                temp2 = row[col+1]
                if(temp1 == temp2 and temp1 == vehicle):
                    return True
        return False

    #if vehicle is horizontal, returns which row the vehicle is in
    def vehicle_row(self, vehicle:str) -> int:
        if(self.is_horizontal(vehicle)):
            row_value = 0
            for row in self.board:
                for col in row:
                    if(vehicle == col):
                        return row_value 
                row_value += 1
    
    #if vehicle is verticle, returns which col the vehicle is in
    def vehicle_col(self, vehicle:str)->int:
        if not(self.is_horizontal(vehicle)):
            col_value = 0
            for i in range(0, 6):
                column_list = np.array([row[i] for row in self.board])
                if(vehicle in column_list):
                    return col_value
                col_value += 1
    
    #-------------------MOVE RIGHT--------------------------#

    def move_right_available(self, vehicle:str, dist:int) -> bool:
        spacesFree = False  #spaces to be moved to are free or not
        if(self.is_horizontal(vehicle)):
            if not self.has_fuel(vehicle):
                return False
            vehicle_row = self.vehicle_row(vehicle)
            right_most_index_pos = 6 - self.board[vehicle_row][::-1].index(vehicle) -1 #gets right most index of vehicle
            spacesFree = False  #spaces to be moved to are free or not
            nextSpaces = []
            for spaces in range(0, dist):
                try:
                    nextSpaces.append(self.board[vehicle_row][right_most_index_pos+1+spaces])
                except:
                    return False
            #check if all the values in array is a .
            if all(x == '.' for x in nextSpaces):
                spacesFree = True
        return spacesFree
    
    def move_right(self, vehicle:str, dist:int) -> BoardState:
        if(self.move_right_available(vehicle, dist)):
            board_copy = copy.deepcopy(self)
            board_copy.spend_fuel(vehicle)
            vehicle_row = board_copy.vehicle_row(vehicle)
            right_most_index_pos = 6 - board_copy.board[vehicle_row][::-1].index(vehicle) - 1 #gets right most index of vehicle
            left_most_index_pos = board_copy.board[vehicle_row].index(vehicle)
            for x in range(0, dist):
                board_copy.board[vehicle_row][left_most_index_pos+x] = '.' 
                board_copy.board[vehicle_row][right_most_index_pos+x+1] = vehicle
            return board_copy

    #-------------------MOVE LEFT--------------------------#
        
    def move_left_available(self, vehicle:str, dist:int) -> bool:
        spacesFree = False  #spaces to be moved to 
        if(self.is_horizontal(vehicle)):
            if not self.has_fuel(vehicle):
                return False
            vehicle_row = self.vehicle_row(vehicle)
            right_most_index_pos = 6 - self.board[vehicle_row][::-1].index(vehicle) - 1 #gets right most index of vehicle
            left_most_index_pos = self.board[vehicle_row].index(vehicle) 
            nextSpaces = []
            for spaces in range(0, dist):
                try:
                    nextSpaces.append(self.board[vehicle_row][left_most_index_pos - 1 - spaces])
                except:
                    return False
            
            #check if all the values in array is a .
            if all(x == '.' for x in nextSpaces):
                spacesFree = True
        
        return spacesFree

    def move_left(self, vehicle:str, dist:int) -> BoardState:
        if(self.move_left_available(vehicle, dist)):
            board_copy = copy.deepcopy(self)
            board_copy.spend_fuel(vehicle)
            vehicle_row = board_copy.vehicle_row(vehicle)
            right_most_index_pos = 6 - board_copy.board[vehicle_row][::-1].index(vehicle) -1 #gets right most index of vehicle
            left_most_index_pos = board_copy.board[vehicle_row].index(vehicle) 

            tempArray = []
            for x in range(0, dist):
                tempArray.append(left_most_index_pos-x-1)

            if all(position>=0 for position in tempArray):
                for x in range(0, dist):
                        board_copy.board[vehicle_row][right_most_index_pos-x] = '.' 
                        board_copy.board[vehicle_row][left_most_index_pos-x-1] = vehicle
                return board_copy
            else:
                pass

    #-------------------MOVE UP--------------------------#
    def move_up_available(self,vehicle:str, dist: int) -> bool:
        spacesFree = False  #spaces to be moved to 
        if not(self.is_horizontal(vehicle)):
            if not self.has_fuel(vehicle):
                return False
            vehicle_col = self.vehicle_col(vehicle)
            tempArray = np.array(self.board)[:, vehicle_col].tolist()
            top_most_index_pos = tempArray.index(vehicle) #represents the row that the top letter is in
            bottom_most_index_pos = 6- tempArray[::-1].index(vehicle) -1 
            nextSpaces = []
            for spaces in range(0, dist):
                try:
                    nextSpaces.append(tempArray[top_most_index_pos-1-spaces])
                except:
                    return False
            
            #check if all the values in array is a .
            if all(x == '.' for x in nextSpaces):
                spacesFree = True
        return spacesFree
    
    def move_up(self, vehicle:str, dist: int) -> BoardState:
        if(self.move_up_available(vehicle, dist)):
            board_copy = copy.deepcopy(self)
            board_copy.spend_fuel(vehicle)
            vehicle_col = board_copy.vehicle_col(vehicle)
            tempArray = np.array(board_copy.board)[:, vehicle_col].tolist()
            top_most_index_pos = tempArray.index(vehicle) #represents the row that the top letter is in
            bottom_most_index_pos = 6 - tempArray[::-1].index(vehicle) -1 

            tempArray = []
            for x in range(0, dist):
                tempArray.append(top_most_index_pos-x-1)

            if all(position>=0 for position in tempArray):
                for x in range(0, dist):
                        board_copy.board[top_most_index_pos-1-x][vehicle_col] = vehicle
                        board_copy.board[bottom_most_index_pos-x][vehicle_col] = '.'
                return board_copy
            else:
                pass
                
          

            
    #-------------------MOVE DOWN--------------------------#

    def move_down_available(self, vehicle:str, dist: int) -> bool:
        spacesFree = False  #spaces to be moved to 
        if not(self.is_horizontal(vehicle)):
            if not self.has_fuel(vehicle):
                return False
            vehicle_col = self.vehicle_col(vehicle)
            tempArray = np.array(self.board)[:, vehicle_col].tolist()
            top_most_index_pos = tempArray.index(vehicle) #represents the row that the top letter is in
            bottom_most_index_pos = 6- tempArray[::-1].index(vehicle) -1 
            nextSpaces = []

            for spaces in range(0, dist):
                try:
                    nextSpaces.append(tempArray[bottom_most_index_pos+1+spaces])
                except:
                    return False
            #check if all the values in array is a .
            if all(x == '.' for x in nextSpaces):
                spacesFree = True
        return spacesFree

    def move_down(self, vehicle:str, dist: int) -> BoardState:
        if(self.move_down_available(vehicle, dist)):
            board_copy = copy.deepcopy(self)
            board_copy.spend_fuel(vehicle)
            vehicle_col = board_copy.vehicle_col(vehicle)
            tempArray = np.array(board_copy.board)[:, vehicle_col].tolist()
            top_most_index_pos = tempArray.index(vehicle) #represents the row that the top letter is in
            bottom_most_index_pos = 6- tempArray[::-1].index(vehicle) -1 
            for x in range(0, dist):
                    board_copy.board[top_most_index_pos+x][vehicle_col] = '.'
                    board_copy.board[bottom_most_index_pos+x+1][vehicle_col] = vehicle
            return board_copy