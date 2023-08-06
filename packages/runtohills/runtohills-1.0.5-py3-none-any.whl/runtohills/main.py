#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run to the hills experiment
"""
import random
import math
import arcade
import os
#from win32api import GetSystemMetrics
import time
from . import info
import numpy as np
from . import sprites
import ctypes
import sys
import pyglet



SCREEN_WIDTH = 1900#int(GetSystemMetrics(0))
SCREEN_HEIGHT = 1100#int(GetSystemMetrics(1))
SCREEN_TITLE = "Run to the hills"
MAX_APPROACH_SCALE=50
NOK_PER_CLIMB=2
STEPS_TO_SUMMIT=20
MIN_EYES=3
N_LIVES=15

imgpth=os.path.join( os.path.dirname(__file__),'images')


def main():
    window = MyGame(os.path.join(imgpth,'Mountain_0sc.png'))
    window.start_new_game(20)
    arcade.run()


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self,background):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)#,fullscreen=True)
        #arcade.set_background_color(arcade.color.BLIZZARD_BLUE)
        self.background=arcade.load_texture(background)
        self.grey_area=arcade.load_texture(os.path.join(imgpth,'black.png'))
        

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        # Set up the player
        self.score = 0
        self.climber = None
        self.size=self.get_size()
        self.hand_cursor=pyglet.window.Window.get_system_mouse_cursor(self,'hand')
        self.min_eyes=MIN_EYES
        self.nok_per_climb=NOK_PER_CLIMB
        self.steps_to_summit=STEPS_TO_SUMMIT
        self.nlives=N_LIVES


    def start_new_game(self,dist_to_mountain):
        """ Set up the game and initialize the variables. """
        w,h=self.size
        self.frame_count = 0
        self.rendering=False
        self.game_over = False

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()

        self.ship_life_list = arcade.SpriteList()

        # Set up the player
        self.fields=[]
        self.score=0
        self.total_score=0
        self.game_number=0
        
        self.pos=info.mountain_pos
        self.dist_to_mountain=dist_to_mountain
        self.approach_scale_power=np.log(MAX_APPROACH_SCALE*0.75)/np.log(self.dist_to_mountain)
        self.approac_pos=np.array([[0.9,0.2],[0.48645833, 0.34]])
        
        self.add_sprites(self.nlives)
        
        self.reset_game(True)      
        
        
        

    def add_sprites(self,nlives):
        
        self.walker = sprites.walker(self)
        self.all_sprites_list.append(self.walker)    
        self.climber = sprites.climber(self)
        self.all_sprites_list.append(self.climber)          
        self.faller = sprites.faller(self)
        self.all_sprites_list.append(self.faller)     
        self.home=sprites.home(self)
        self.all_sprites_list.append(self.home)   
        self.advance_sprite=sprites.advance(self)
        self.all_sprites_list.append(self.advance_sprite)   
        self.winner=sprites.winner(self)
        self.all_sprites_list.append(self.winner)           
        
        self.make_lives()
        self.dices=sprites.dices(self, self.all_sprites_list)  

        

    def make_lives(self):
        # Set up the little icons that represent the player lives.
        w,h=self.size
        start_pos=0.12*w
        cur_pos = start_pos
        row=2
        scale=0.05
        self.lives=[]
        for i in range(self.nlives):
            if i==5:
                row=1
                cur_pos=start_pos
            life = arcade.Sprite(os.path.join(imgpth,'climbing_avatar.png'), scale)
            life.center_x = cur_pos + life.width
            life.center_y = row*life.height
            cur_pos += life.width
            self.lives.append(life)
            self.all_sprites_list.append(life)
            
              
        
         
        
    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.rendering=True
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                              SCREEN_WIDTH, SCREEN_HEIGHT, self.background)          
        # Draw all the sprites.
        self.all_sprites_list.draw()
        self.dices.update()

        # Put the text on the screen.
        
        a=[0.97,0.94,0.91,0.88,0.82]
        w,h=self.size
        
        arcade.draw_texture_rectangle(w*0.1665, h*0.94, w*0.27, h*0.15, self.grey_area, alpha=10)
        
        arcade.draw_text("Rehearsal:" ,int(w*0.03), int(h*0.1), arcade.color.BLACK, w*0.01)
        arcade.draw_text("Real money:" ,int(w*0.03), int(h*0.05), arcade.color.BLACK, w*0.01)
        
        arcade.draw_text("Score this round:" ,int(w*0.05), int(h*a[0]), arcade.color.BLACK, w*0.015)
        arcade.draw_text(str(self.score).rjust(3),int(w*0.23), int(h*a[0]), arcade.color.BLACK, w*0.015)
        arcade.draw_text("NOK",int(w*0.26), int(h*a[0]), arcade.color.BLACK, w*0.015)
        
        arcade.draw_text("Total score:" ,int(w*0.05), int(h*a[1]), arcade.color.BLACK, w*0.015)
        arcade.draw_text(str(self.total_score).rjust(3),int(w*0.23), int(h*a[1]), arcade.color.BLACK, w*0.015)
        arcade.draw_text("NOK",int(w*0.26), int(h*a[1]), arcade.color.BLACK, w*0.015)        
        
        arcade.draw_text("Distance to summit:", int(w*0.05), int(h*a[2]), arcade.color.BLACK, w*0.015)      
        arcade.draw_text(str(self.stilltogo).rjust(3),int(w*0.23), int(h*a[2]), arcade.color.BLACK, w*0.015)

        arcade.draw_text("Distance to mountain:",int(w*0.05), int(h*a[3]), arcade.color.BLACK, w*0.015)
        arcade.draw_text(str(self.dist_to_walk).rjust(3),int(w*0.23), int(h*a[3]), arcade.color.BLACK, w*0.015)
        if not self.dices.done:
            arcade.draw_text("WAIT",int(w*0.05), int(h*a[4]), arcade.color.BLACK, w*0.015)        

    def on_key_press(self, symbol, modifiers):
        """ Called whenever a key is pressed. """
        # Shoot if the player hit the space bar and we aren't respawning.
        if not self.dices.done:
            return
        if symbol == arcade.key.UP:
            self.advance()
                
            
        if symbol == arcade.key.F or symbol==arcade.key.ESCAPE:
            self.set_fullscreen(not self.fullscreen)
            w, h = self.size
            self.set_viewport(0, w, 0, h)
            
    def on_mouse_press(self, x, y, button, modifiers):
        if not self.dices.done:
            return
        if self.over_sprite(self.home, x, y):
            if sum(self.dices.eyes)<=MIN_EYES:
                self.total_score=0
            else:
                self.total_score+=self.score
            self.reset_game()
            return
        elif self.over_sprite(self.advance_sprite, x, y):
            self.advance()
            
        
    
    def on_mouse_motion(self,x, y, dx, dy):
        if self.dices.done and (self.over_sprite(self.home, x, y) or self.over_sprite(self.advance_sprite, x, y)):
            self.set_mouse_cursor(self.hand_cursor)  
        else:
            self.set_mouse_cursor(None)  
                 
    def reset_game(self,initial=False):
        w, h = self.size
        self.stilltogo=STEPS_TO_SUMMIT
        self.score=0
        self.climbed=0     
        self.dist_to_walk=self.dist_to_mountain
        self.dist_walked=0
        self.dices_rolling=False   
        self.walk()
        if not initial:
            self.lives[self.game_number].alpha=100
            self.game_number+=1
            if self.game_number==5:
                ctypes.windll.user32.MessageBoxW(0,  
                                                 """Your rehersal rounds are now over, and your score is reset to zero. 
                                                 What you earn from now on, will be paid out to you in cash""", 
                                                 "REHERSAL ROUNDS ARE OVER",
                                                 1)
                self.total_score=0
                
        self.climber.alpha=0
        self.walker.alpha=0
        self.walker.becoming_visible=True
        self.faller.alpha=0
        self.climber.alpha=0
        self.dices.reset()
    
    def advance(self):
        if not self.dices.done:
            return
        if self.dist_to_walk>0:
            self.dist_to_walk-=1
            self.dist_walked+=1
            self.walk()
            return
        self.walker.alpha=0
        self.climb()
        self.dices.roll()
            

        
    def climb(self):
        w, h = self.size
        x,y=self.pos[self.climbed]
        self.climber.center_x = w*x
        self.climber.center_y = h*(y+0.01)        
        if self.climbed==0:
            self.climber.alpha=sprites.MAX_ALPHA
        self.climbed+=1
        self.stilltogo-=1   

        
    def walk(self):
        w, h = self.size
        a=self.approach_scale_power
        r=0.75/float(self.dist_walked+1)**a
        q=float(self.dist_walked)/self.dist_to_mountain
        x,y=q*self.approac_pos[1]+(1-q)*self.approac_pos[0]
        self.walker.scale=r
        self.walker.center_x = w*x
        self.walker.center_y = h*y 
        a=0

    def update(self, x):
        """ Move everything """

        self.frame_count += 1

        if not self.game_over:
            self.all_sprites_list.update()

    def over_sprite(self,s,x,y):
        w1,h1=self.size
        w2,h2=self.get_size()
        wr=w2/w1
        hr=h2/h1
        hgt=s.height*0.5*hr
        wdt=s.width*0.5*wr
        
        ctr_x=s.center_x*wr
        ctr_y=s.center_y*wr
        
        return (x>ctr_x-wdt and x<ctr_x+wdt 
                and y>ctr_y-hgt and y<ctr_y+wdt)
    
    
