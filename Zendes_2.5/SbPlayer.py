# -*- coding: utf-8 -*-
import sys
from os import listdir
from os.path import isdir, isfile
from pygame.sprite import Sprite, collide_rect
from pygame.image import load
from pygame import Surface, time, transform
from SbDev import sb_output
from SbAnimation import Animation
from SbConstants import *
#from pygame import event
#from pygame import mouse, MOUSEBUTTONUP
#from SbDev import sb_output, region_get
#from pygame import mixer
#from os.path import isfile, isdir
#from os import makedirs


GRAVITY = 0.198*float(sz)
SPEED = int(float(5*sz))
JUMP = int(float(4*sz))

width = int(38*sz)
height = int(85*sz)

def Player_load(self, path, wname):
	path1 = path+"/worlds/%s/player.sav" % wname
	try:
		with open(path1, 'r') as playerfile:
			f = playerfile.readlines()
			pos = f[1][0:-1].split("_")
			pos1 = (int(pos[0])*bs, int(pos[1])*bs)
			self.x = pos1[0]
			self.y = pos1[1]
			self.hp = int(pos[2])
			self.hunger = float(pos[3])
	except IOError:
		pass



class Player():
	def __init__(self, x, y, path, wname):
		self.path = path
		self.wname = wname
		self.image = Surface((width, height))
		self.x = x
		self.y = y
		self.startpos = (x, y)
		self.onground = True
		self.xvel = 0
		self.yvel = 0
		self.hp = 20
		self.hunger = 20
		Player_load(self, path, wname)
		self.spawnpoint = (x,y)
		self.started = False
		self.stay_sprites = [transform.scale(load(path+"/resources/textures/glo/player/stay0.png"), (int(width*1.2), height)),\
							transform.scale(load(path+"/resources/textures/glo/player/stay1.png"), (int(width*1.2), height)),\
							transform.scale(load(path+"/resources/textures/glo/player/stay2.png"), (int(width*1.2), height)),\
							transform.scale(load(path+"/resources/textures/glo/player/stay1.png"), (int(width*1.2), height))]

		self.stayr_sprites = [transform.scale(load(path+"/resources/textures/glo/player/stayr0.png"), (int(width*1.2), height)),\
							transform.scale(load(path+"/resources/textures/glo/player/stayr1.png"), (int(width*1.2), height)),\
							transform.scale(load(path+"/resources/textures/glo/player/stayr2.png"), (int(width*1.2), height)),\
							transform.scale(load(path+"/resources/textures/glo/player/stayr1.png"), (int(width*1.2), height))]

		self.run_sprites = [transform.scale(load(path+"/resources/textures/glo/player/run0.png"), (int(width*1.2), height)),\
							transform.scale(load(path+"/resources/textures/glo/player/run1.png"), (int(width*1.2), height))]

		self.runr_sprites = [transform.scale(load(path+"/resources/textures/glo/player/runr0.png"), (int(width*1.2), height)),\
							transform.scale(load(path+"/resources/textures/glo/player/runr1.png"), (int(width*1.2), height))]

		self.stay_anim = Animation(self.stay_sprites, 500)
		self.stayr_anim = Animation(self.stayr_sprites, 500)
		self.run_anim = Animation(self.run_sprites, 200)
		self.runr_anim = Animation(self.runr_sprites, 200)
		self.dt = 0
		self.clock = time.Clock()
		self.right = False
		self.air = 20
		self.pink = Surface((width, height))
		self.pink.fill(PINK)
		self.jump_delay = 0

		self.timers = {
						"hunger_hp":0,
						"air_hp":0,
						"air":0,
						"hunger":0,
						"hp_hunger_plus":0,
						}


	def save_data(self):
		path1 = self.path+"/worlds/%s/player.sav" % self.wname
#		sb_output(self.path, 'Saving player\'s data in the world %s' % self.wname)
		with open(path1, 'w') as playerfile:
			f = playerfile.write("Zendes 2.5 Sandbox 2d player data save-file\n"+str(int(self.x/bs))+"_"+str(int(self.y/bs))+"_"+str(int(self.hp))+"_"+str(float(self.hunger))+"\n")

	def get_pos(self):
		return (self.x, self.y)

	def update(self, path, blocks, up, left, right, fly):
		self.onground = False
		self.collide(blocks)
		if self.hunger > 20:
			self.hunger = 20
		if self.timers["hunger"] >= 10000:
			self.hunger += -1
			self.timers["hunger"] = 0
		else:
			self.timers["hunger"] += 10
		if self.hunger <= 0:
			if self.timers["hunger_hp"] >= 10000:
				self.hp -= 1
				self.timers["hunger_hp"] = 0
			else:
				self.timers["hunger_hp"] += 100
		if self.hunger >= 15 and self.hp < 20:
			if self.timers["hp_hunger_plus"] >= 10000:
				self.hp += 1
				self.timers["hp_hunger_plus"] = 0
			else:
				self.timers["hp_hunger_plus"] += (self.hunger-14)*20
		if self.jump_delay != 0:
			self.jump_delay += -1
		#ON GROUND
		try:
			if not self.onground:
				if blocks[str(int((self.x+bs/10)/bs))+"_"+str(int((self.y+10)/bs))].id == BLOCK_WATER:
					self.yvel += GRAVITY*0.45
					self.yvel = self.yvel*0.9
				else:	
					self.yvel += GRAVITY
				if blocks[str(int((self.x+bs/10)/bs))+"_"+str(int((self.y+10)/bs))].id == BLOCK_LEAD:
					if up:
						if self.yvel > -3.0:
							self.yvel += -1.0
			else:
				if up:
					if self.jump_delay == 0:
						if blocks[str(int((self.x+bs/10)/bs))+"_"+str(int((self.y+10)/bs))].id == BLOCK_WATER:
							self.yvel += -JUMP*2
							self.y += - JUMP
							self.timers["hunger"] += 500
						else:
							self.yvel += -JUMP
							self.y += - JUMP
							self.timers["hunger"] += 250
						self.jump_delay = 10
		except KeyError:
			pass
		if right:
			try:
				if blocks[str(int((self.x+bs/10)/bs))+"_"+str(int((self.y+10)/bs))].id == 11:
					self.xvel = int(SPEED*0.5)
				else:
					self.xvel = SPEED
				self.image.blit(self.pink, (0,0))
				self.image.set_colorkey(PINK)
				self.runr_anim.update(self.dt)
				self.image.blit(self.runr_anim.get_sprite(), (0,0))
				self.right = True
				self.timers["hunger"] += 5
			except KeyError:
				pass
		if left:
			try:
				if blocks[str(int((self.x+bs/10)/bs))+"_"+str(int((self.y+10)/bs))].id == 11:
					self.xvel = int(-SPEED*0.5)
				else:
					self.xvel = -SPEED
				self.image.blit(self.pink, (0,0))
				self.image.set_colorkey(PINK)
				self.run_anim.update(self.dt)
				self.image.blit(self.run_anim.get_sprite(), (0,0))
				self.right = False
				self.timers["hunger"] += 5
			except KeyError:
				pass
			
		if fly:
			self.yvel = 0
			self.y += -10
		#NOT RIGHT AND NOT LEFT
		if not right and not left:
			self.xvel = int(self.xvel*0.95)
			self.image.blit(self.pink, (0,0))
			self.image.set_colorkey(PINK)
			if self.right:
				self.stayr_anim.update(self.dt)
				self.image.blit(self.stayr_anim.get_sprite(), (0,0))
			else:
				self.stay_anim.update(self.dt)
				self.image.blit(self.stay_anim.get_sprite(), (0,0))
		self.collide(blocks)
		self.dt = self.clock.tick(60)

	def collide(self, blocks):
		try:
			#GET BLOCKS
			down_y = 0
			if down_y >= 0:
				down_y = int(self.y/bs)
			else:
				down_y = -(int(self.y/bs))
			down_block = blocks[str(int((self.x+width-resz(4))/bs))+"_"+str(int(self.y/bs)+2)]
			down_block2 = blocks[str(int((self.x+resz(4))/bs))+"_"+str(int(self.y/bs)+2)]
			up_block = blocks[str(int((self.x+bs/10)/bs))+"_"+str(int((self.y+10)/bs)-1)]
			head_block = blocks[str(int((self.x+bs/10)/bs))+"_"+str(int((self.y+10)/bs))]

			left_down_block = blocks[str(int((self.x+10)/bs)-1)+"_"+str(int(self.y/bs+1))]
			right_down_block = blocks[str(int((self.x-10)/bs)+1)+"_"+str(int(self.y/bs+1))]

			left_up_block = blocks[str(int((self.x+10)/bs)-1)+"_"+str(int(self.y/bs))]
			right_up_block = blocks[str(int((self.x-10)/bs)+1)+"_"+str(int(self.y/bs))]

			if head_block.data.air:
				self.air = 20
			else:
				if self.air >= 0:
					if self.timers["air"] == 10000:
						self.air += -1
						self.timers["air"] = 0
					else:
						self.timers["air"] += 100
			if self.air <= 0:
				if self.timers["air_hp"] == 10000:
					self.hp += -1
					self.timers["air_hp"] = 0
				else:
					self.timers["air_hp"] += 200
				self.air += 0

			if self.y+height >= down_block.y:
				if down_block.data.collable:
					self.onground = True
					#HP- ПРИ ПАДЕНИИ
					if self.yvel > 8:
						if self.started:
							self.hp -= int(self.yvel*0.25)
					if not self.started:
						self.started = True
						self.spawnpoint = self.startpos
					self.yvel = 0
					self.y = down_block.y - height
			if self.y+height >= down_block2.y:
				if down_block2.data.collable:
					self.onground = True
					#HP- ПРИ ПАДЕНИИ
					if self.yvel > 8:
						if self.started:
							self.hp -= int(self.yvel*0.25)
					self.started = True
					self.yvel = 0
					self.y = down_block2.y - height

			if self.y <= up_block.y+bs and up_block.data.collable:
				self.y = up_block.y + bs
				self.yvel = -self.yvel
			# LEFT AND RIGHT DOWN BLOCKS
			if self.x < left_down_block.x+bs and left_down_block.data.collable:
				self.x = left_down_block.x+bs+resz(2)
				self.xvel = 0
			if self.x < right_down_block.x and right_down_block.data.collable:
				self.x = right_down_block.x-width-resz(2)
				self.xvel = 0
			# LEFT AND RIGHT UP BLOCKS
			if self.x+resz(1) < left_up_block.x+bs and left_up_block.data.collable:
				self.x = left_up_block.x+bs+resz(2)
				self.xvel = 0
			if self.x+resz(2) < right_up_block.x and right_up_block.data.collable:
				self.x = right_up_block.x-width-resz(2)
				self.xvel = 0


			self.x += self.xvel
			self.y += self.yvel
		except KeyError:
			pass
