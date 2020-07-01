# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 04:31:09 2020

@author: Dining
"""
import pickle
import numpy as np
from os import path
import os 

class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0 #initialization
        self.car_pos = (0,0)
        self.feature = [0,0,0,0,0,0,0,0,0]

        with open(path.join(path.dirname(__file__), 'save', 'decisiontreemodel_1.pickle'), 'rb') as file: self.model = pickle.load(file)
        pass




    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        speed_f = [100, 100, 100]
        speed_b = [100, 100, 100]

        def check_grid():
            self.car_pos = scene_info[self.player]
            if scene_info["status"] != "ALIVE":
                return "RESET"
        
            if len(self.car_pos) == 0:
                self.car_pos = (0,0)

            grid = set()
            speed_ahead = []

            for i in range(len(scene_info["cars_info"])): # for all cars information in scene of one frame
                car = scene_info["cars_info"][i]
                if car["id"]==self.player_no: #player's car information
                    self.car_vel = car["velocity"]
                    if self.car_pos[0] <= 45: # left bound
                        grid.add(1)
                        grid.add(4)
                        grid.add(7)
                    elif self.car_pos[0] >= 585: # right bound
                        grid.add(3)
                        grid.add(6)
                        grid.add(9)
                    elif self.car_pos[0] <=115:
                        grid.add(10)
                        grid.add(12)
                    elif self.car_pos[0] >=515:
                        grid.add(11)
                        grid.add(13)
                    elif self.car_pos[0] <=185:
                        grid.add(14)
                    elif self.car_pos[0] >=445:
                        grid.add(15)


                else: # computer's cars information
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position



                    if x <= 40 and x >= -40 :
                        if y >= 0 and y <= 300:
                            grid.add(2)
                            if y <= 150:
                                grid.add(5)
                                speed_f[1]=car["velocity"]
                        elif y <= 0 and y >= -200:
                            grid.add(8)
                            speed_b[1]=car["velocity"]
                    elif x >= -100 and x <= -40 :
                        if y >= 80 and y <= 250:
                            grid.add(3)
                            speed_f[2]=car["velocity"]
                        elif y <= -80 and y >= -200:
                            speed_b[2]=car["velocity"]
                            grid.add(9)
                        elif y <= 80 and y >= -80:
                            grid.add(6)
                    elif x <= 100 and x >= 40:
                        if y >= 80 and y <= 250:
                            grid.add(1)
                            speed_f[0]=car["velocity"]
                        elif y <= -80 and y >= -200:
                            speed_b[0]=car["velocity"]
                            grid.add(7)
                        elif y <= 80 and y >= -80:
                            grid.add(4)
                    elif x <= 160 and x >= 100:
                        if y >= 80 and y <= 250:
                            grid.add(10)
                        elif y <= 80 and y >= -80:
                            grid.add(12)
                    elif x >= -160 and x <= -100:
                        if y >= 80 and y <= 250:
                            grid.add(11)
                        elif y <= 80 and y >= -80:
                            grid.add(13)
                    elif x <= 220 and x>=160:
                        if(y >=-80 and y<=250):
                            grid.add(14)
                    elif x >= -220 and x<= -160:
                        if(y >=-80 and y<=250):
                            grid.add(15)
#            print(grid)

            coin_x = 1000
            coin_y = 1000

            for coin in scene_info["coins"]:
                temp_x = coin[0]
                temp_y = coin[1]
                if temp_y > 0:
                    if temp_x < coin_x:
                        coin_x = temp_x
                        coin_y = temp_y
            if coin_x == 1000:
                coin_x = 315
                coin_y = 0
            #if (5 in grid):
            #    coin_x=315

            return move(grid=grid,coin_x = self.car_pos[0]-coin_x,speed=self.car_vel-speed_f[1])
        
        def move(grid,coin_x ,speed):
            feature = []


            grid_tolist = list(grid)
            grid_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for i in grid_tolist:
                grid_data[i-1] = 1 # change grid set into feature's data shape
            grid_data.append(coin_x)
            #grid_data.append(coin_y)
            #grid_data.append(speed_f[0])
            grid_data.append(speed)
            '''grid_data.append(speed_f[2])
            grid_data.append(speed_b[0])
            grid_data.append(speed_b[1])
            grid_data.append(speed_b[2])'''

            grid_data = np.array(grid_data).reshape(1,-1)

            self.feature = grid_data
            self.feature = np.array(self.feature)
            self.feature = self.feature.reshape((1,-1))
            y = self.model.predict(self.feature)

            if y == 0:
                return ["SPEED"]
            if y == 1:
                return ["SPEED", "MOVE_LEFT"]
            if y == 2:
                return ["SPEED", "MOVE_RIGHT"]
            if y == 3:
                return ["BRAKE"]
            if y == 4:
                return ["BRAKE", "MOVE_LEFT"]
            if y == 5:
                return ["BRAKE", "MOVE_RIGHT"]
            if y == 6:
                return ["LEFT"]
            if y == 7:
                return ["RIGHT"]
            if y == 8:
                return ["NONE"]
        
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass
