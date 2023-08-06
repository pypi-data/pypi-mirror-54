#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import arcade
import random
import numpy as np
import time

imgpth=os.path.join( os.path.dirname(__file__),'images')


EXPLOSION_TIME=2
EXPLOSION_TIME_DELAY=2
FALL_SPEED=0.003
COLOR_SPEED=5
MAX_ALPHA=255
BLINK_TIME=0.25
MAX_BLINKS=12
BOUNCE_DRAG=7

class home(arcade.Sprite):
	"""
	Home button.
	"""
	def __init__(self,window):


		# Call the parent Sprite constructor
		super().__init__(os.path.join(imgpth,'HOME.png'),scale=0.15)
		w, h = window.size

		self.window=window
		self.center_x = w*0.12
		self.center_y = h*0.35	
		
		
class advance(arcade.Sprite):
	"""
	Advance button
	"""
	def __init__(self,window):


		# Call the parent Sprite constructor
		super().__init__(os.path.join(imgpth,'advance.png'))
		w, h = window.size

		self.window=window
		self.center_x = w*0.5
		self.center_y = h*0.02

class faller(arcade.Sprite):
	"""
	Sprite that represents the walker falling.
	"""
	def __init__(self,window):
		""" Set up the space ship. """

		# Call the parent Sprite constructor
		super().__init__(os.path.join(imgpth,'Falling_avatar.png'),scale=0.05)
		w, h = window.size
		self.alpha=0
		self.window=window
		self.isfalling=False
		self.floor=0
		

	def update(self):
		if (not self.isfalling):
			return
		w, h = self.window.size
		self.center_y-=h*FALL_SPEED
		if self.center_y<=self.floor:
			self.window.reset_game()
			self.isfalling=False
		super().update()    

	def fall(self):
		self.center_x=self.window.climber.center_x
		self.center_y=self.window.climber.center_y
		self.window.climber.alpha=0
		self.alpha=MAX_ALPHA
		self.isfalling=True
		
class walker(arcade.Sprite):
	"""
	Sprite that represents the walker.
	"""
	def __init__(self,window):

		# Call the parent Sprite constructor
		super().__init__(os.path.join(imgpth,"Approach_avatar.png"))
		w, h = window.size
		self.window=window
		self.alpha=0
		self.becoming_visible=True
		

	def update(self):
		if self.becoming_visible:
			self.alpha=min((self.alpha+COLOR_SPEED,MAX_ALPHA))
			if self.alpha==MAX_ALPHA:
				self.becoming_visible=False

		super().update()    



class climber(arcade.Sprite):
	"""
	Sprite that represents the climber.
	"""
	def __init__(self,window):
		# Call the parent Sprite constructor
		super().__init__(os.path.join(imgpth,"climbing_avatar.png"),scale=0.05)
		w, h = window.size
		self.window=window
		self.alpha=0
		self.becoming_visible=True

class winner(arcade.Sprite):
	"""
	Sprite that represents the climber.
	"""
	def __init__(self,window):
		# Call the parent Sprite constructor
		super().__init__(os.path.join(imgpth,"Summit_avatar.png"),scale=0.04)
		w, h = window.size
		self.window=window
		self.alpha=0
		self.blinking=False
		self.blink_count=0
		
	def update(self):
		if (not self.blinking):
			return
		w, h = self.window.size
		t=time.perf_counter()
		if t-self.blink_time>BLINK_TIME:
			self.alpha=MAX_ALPHA*(self.alpha==0)
			self.blink_count+=1
			self.blink_time=t
			if self.blink_count>MAX_BLINKS:
				self.blink_count=0
				self.alpha=0
				self.blinking=False
				self.window.reset_game()
		super().update()  
		
	def blink(self):
		w, h = self.window.size
		self.blinking=True
		self.alpha=MAX_ALPHA
		self.blink_time=time.perf_counter()
		self.center_x=self.window.climber.center_x
		self.center_y=self.window.climber.center_y+h*0.01

class exploder(arcade.Sprite):
	"""
	Sprite that represents our space ship.

	Derives from arcade.Sprite.
	"""
	def __init__(self,window):
		""" Set up the space ship. """

		# Call the parent Sprite constructor
		self.window=window
		w, h = window.size
		scale=0.25
		super().__init__(os.path.join(imgpth,"Explosion.png"),scale)
		self.alpha=0
		self.change=h*0.05
		self.isexploding=False

	def explode(self,pos_abs):
		self.isexploding=True
		self.time_end=time.perf_counter()
		self.time_flash=time.perf_counter()
		self.time_delay=time.perf_counter()
		x,y =pos_abs
		self.pos_orig_abs=x,y
		self.center_x=x
		self.center_y=y

	def update(self):
		if (not self.isexploding) or (time.perf_counter()-self.time_delay<EXPLOSION_TIME_DELAY):
			return
		if time.perf_counter()-self.time_end>EXPLOSION_TIME+EXPLOSION_TIME_DELAY:
			self.alpha=0
			self.isexploding=False
			self.window.faller.fall()
			return
		w,h=self.window.size
		x,y=self.pos_orig_abs
		if abs(y- self.center_y)>h*0.01:
			self.change=-self.change
		if time.perf_counter()-self.time_flash>0.1:
			self.alpha=0
			self.time_flash=time.perf_counter()
		else:
			self.alpha=MAX_ALPHA
		self.center_y+=self.change
		super().update()

class dices():
	def __init__(self,window,all_sprites_list):
		
		w,h=window.size
		self.dices=[
			dice(window, 8 ,-1  ,  1),
			dice(window, 12 ,-1.5,  0)
			]
		
		self.n_dices=len(self.dices)
		self.thrown=False
		self.window=window
		self.exploder = exploder(window)
		all_sprites_list.append(self.exploder)
		self.dices_green=[]
		self.dices_red=[]
		for i in range(self.n_dices):
			self.dices_green.append(dice_color(window,'green',self))
			self.dices_red.append(dice_color(window,'red',self))
		a=[]
		a.extend(self.dices)
		a.extend(self.dices_green)
		a.extend(self.dices_red)
		self.done=True
		for i in a:
			all_sprites_list.append(i)
		
	def update(self):
		c=False
		for i in range(self.n_dices):
			c=c or self.dices_green[i].coloring
			c=c or self.dices_red[i].coloring
		self.colouring=c
		self.was_thrown=self.thrown
		self.was_done=self.done
		self.thrown=False
		for i in self.dices:
			self.thrown=self.thrown or i.thrown
		self.done=(not self.thrown) and (not self.colouring) and (not self.exploder.isexploding) and (not self.window.faller.isfalling) and (not self.window.winner.blinking)
		if not (self.was_thrown and (not self.thrown)):
			return
		self.thrown=False
		if np.sum(self.eyes)<=self.window.min_eyes:
			for i in  range(self.n_dices):
				x,y=self.dices[i].center_x,self.dices[i].center_y
				self.dices_red[i].colorize([x,y],self.dices[i].eyes)
		else:
			for i in range(self.n_dices):
				x,y=self.dices[i].center_x,self.dices[i].center_y
				self.dices_green[i].colorize([x,y],self.dices[i].eyes)	
				
	def roll(self):
		self.reset()
		self.thrown=True
		self.eyes=[]
		self.eyes_tot=0
		for i in range(len(self.dices)):
			eyes=random.randint(1,6)
			self.eyes.append(eyes)
			self.dices[i].roll(eyes)
			self.eyes_tot+=eyes
			
	def reset(self):
		for i in range(self.n_dices):
			self.dices[i].reset()
			self.dices_red[i].alpha=0
			self.dices_green[i].alpha=0
	
			
	
class dice(arcade.Sprite):
	"""
	Sprite that represents our space ship.

	Derives from arcade.Sprite.
	"""
	def __init__(self,window,speed_x,speed_y,delay):
		""" Set up the space ship. """

		# Call the parent Sprite constructor
		super().__init__()
		self.offsetlist=[]
		w, h = window.size
		for img, in [[os.path.join(imgpth,"Dice1.png")],
		             [os.path.join(imgpth,"Dice2.png")],
		                [os.path.join(imgpth,"Dice3.png")],
		                [os.path.join(imgpth,"Dice4.png")],
		                [os.path.join(imgpth,"Dice5.png")],
		                [os.path.join(imgpth,"Dice6.png")]]:
			texture = arcade.load_texture(img)
			self.textures.append(texture) 
		self.set_texture(0)
		self.alpha=0
		self.window=window
		self.startpos=[0.03,0.97]
		self.center_x =w*self.startpos[0]
		self.center_y = h*self.startpos[1]
		self.thrown=False
		self.time_face_update=time.perf_counter()
		self.accel=1
		self.speed=[speed_x,speed_y]
		self.floor=h*0.15
		self.left_wall=w*0.5
		self.dice_loaded=False
		self.delay=delay


	def update(self):
		"""
		Update our position and other particulars.
		"""
		if (not self.dice_loaded) and (self.window.rendering==True):
			for i in range(6):
				self.set_texture(i)   
			self.dice_loaded=True
		w, h = self.window.size
		if (not self.thrown) or (time.perf_counter()-self.time_delay<self.delay):
			return
		if time.perf_counter()-self.time_face_update>1:
			eyes=random.randint(1,6)
			self.set_texture(eyes-1)
			self.time_face_update=time.perf_counter()

		if self.center_x>=w or self.center_x<=self.left_wall_tmp:
			self.left_wall_tmp=self.left_wall
			self.speed_x=-self.speed_x
		self.center_x += self.speed_x
		self.speed_y-=self.accel
		if self.center_y<=self.floor:
			self.speed_y=abs(self.speed_y)-BOUNCE_DRAG
			if self.speed_y<5*self.accel:
				self.thrown=False
				self.speed_y=0
				self.center_y=self.floor
				self.set_texture(self.eyes-1)
				return
		self.center_y += self.speed_y

		""" Call the parent class. """
		super().update()

	def roll(self,eyes): 
		x,y=self.speed
		self.speed_x=x
		self.speed_y=y		
		self.alpha=MAX_ALPHA  
		self.thrown=True
		self.eyes=eyes
		self.left_wall_tmp=0
		self.time_delay=time.perf_counter()
		
	def reset(self):
		w,h=self.window.size
		self.alpha=0
		self.center_x =w*self.startpos[0]
		self.center_y = h*self.startpos[1]		
	



class dice_color(arcade.Sprite):
	"""
	Sprite that represents our space ship.

	Derives from arcade.Sprite.
	"""
	def __init__(self,window,color,dices):
		""" Set up the space ship. """

		# Call the parent Sprite constructor
		super().__init__()
		self.offsetlist=[]
		for img, in [[os.path.join(imgpth,f"Dice1_{color}.png")],
		             [os.path.join(imgpth,f"Dice2_{color}.png")],
		                [os.path.join(imgpth,f"Dice3_{color}.png")],
		                [os.path.join(imgpth,f"Dice4_{color}.png")],
		                [os.path.join(imgpth,f"Dice5_{color}.png")],
		                [os.path.join(imgpth,f"Dice6_{color}.png")]]:
			texture = arcade.load_texture(img)
			self.textures.append(texture) 
		self.set_texture(0)
		self.alpha=0
		self.window=window
		self.dice_loaded=False
		self.coloring=False
		self.dices=dices
		self.dice_color=color
		
	def update(self):
		if (not self.dice_loaded) and (self.window.rendering==True):
			for i in range(6):
				self.set_texture(i)   
			self.dice_loaded=True	
		if self.dices.thrown:
			self.alpha=0
		if self.coloring:
			self.alpha=min((self.alpha+COLOR_SPEED,MAX_ALPHA))
			if self.alpha==MAX_ALPHA:
				self.coloring=False
				if self.dice_color=='red':
					self.dices.exploder.explode(self.window.climber.position)
				else:
					self.window.score+=self.window.nok_per_climb
					if self.window.climbed==self.window.steps_to_summit:
						self.window.climber.alpha=0
						self.window.winner.blink()
				
				

		super().update()
		
	def colorize(self,pos_abs,eyes):
		x,y=pos_abs
		self.center_x=x
		self.center_y=y		
		self.set_texture(eyes-1)
		self.coloring=True
		
	def reset(self):
		self.alpha=0
		
		

		
		

