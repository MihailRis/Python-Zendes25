# -*- coding:utf-8 -*-

import random
from pygame.sprite import Sprite, collide_rect
from pygame.image import load
from pygame import Surface, transform
from pygame import event
from pygame import mouse, MOUSEBUTTONUP
from SbDev import sb_output, region_get, toogle, Delay, dist
from pygame import mixer
from os.path import isfile, isdir
from os import makedirs, listdir
from SbGenerator import generation
import sys
import random
import time
from SbConstants import *
from SbEffects import explode
from pygame.locals import *

pink_mat = Surface((bs,bs))
pink_mat.fill(PINK)


path = sys.path[1]

id_item = 0

mixer.init()

SOUND_VOLUME = 1.0

BLACK = (0,0,0)
PINK = (255,0,255)
SCREEN_SISE = (33*bs, 20*bs)


#self.spawnmobs.append((position, name, hp, velocity, (item_id, count, NBTData)))
BLD = {}


def give(id_item_give):
	id_item = id_item_give

def csize(size):
	return (size[0]+bs, size[1]+bs)

class Camera():
	def __init__(self,player):
		pos = (player.x, player.y)
		self.player = player
		self.pos = pos
		self.x = pos[0]
		self.y = pos[1]
def camera_func(camera, pos, SIZE1):
	global SCREEN_SISE
	SCREEN_SISE1 = csize(SIZE1)
	SCREEN_SIZE = SCREEN_SISE1
	player_in_screen = ((SCREEN_SISE1[0]/2)-1*bs, (SCREEN_SISE1[1]/2)-2*bs)
	posi = (-(camera.player.x - player_in_screen[0] - pos[0]), -(camera.player.y - player_in_screen[1] - pos[1]))
	return posi

def unc_func(camera):
	mpos = mouse.get_pos()
	dat_x = int((mpos[0]+camera.player.x-SCREEN_SISE[0]*sz/2)/bs)+2
	dat_y = int((mpos[1]+camera.player.y-SCREEN_SISE[1]*sz/2)/bs)+3

	data_pos = "%s_%s" % (dat_x, dat_y)
	return data_pos

def unc2_func(camera):
	mpos = mouse.get_pos()
	dat_x = int((mpos[0]+camera.player.x-SCREEN_SISE[0]*sz/2)/bs)+2
	dat_y = int((mpos[1]+camera.player.y-SCREEN_SISE[1]*sz/2)/bs)+3

	data_pos = (dat_x*bs, dat_y*bs)
	return data_pos

def loadId(self, wname):
	path = self.path+"/worlds/%s/regions/" % (wname)
	reg = region_get(self.x/bs, self.y/bs)
	if isfile(path+"region%s.reg" % reg):
		regfile = open(path+"region%s.reg" % reg, 'r')
		regfile1 = regfile.readlines()
		blockdata = (str(int(self.x/bs))+"_"+str(int(self.y/bs)))+"_"
		for block in regfile1:
			if block.startswith(blockdata):
				self.id = int(((block.split("_"))[2]))
				self.data = BlockTypes[self.id]
				self.destred = self.deststart = self.data.dest
				self.oldest = int(block.split("_")[3])
				self.inventory_string = block.split("_")[4][:-1]

				self.blit_texture()
				break

		regfile.close()
	if isfile(self.path+"/worlds/%s/mobs/region%s.reg" % (wname, reg)):
		regfile = open(self.path+"/worlds/%s/mobs/region%s.reg" % (wname, reg), 'r')
		reglines = regfile.readlines()
		ls = '' #ls - lines string
		for line in reglines:
			linedata = line.split("#")
			xpos = int(linedata[0])
			ypos = int(linedata[1])
			name = str(linedata[2])
			hp   = int(float(linedata[3]))
			xvel = float(linedata[4])
			yvel = float(linedata[5])

			itemid = int(linedata[6])
			count = int(linedata[7])
			NBTData = int(linedata[8])
			if int(xpos/bs) == int(self.x/bs) and int(ypos/bs) == int(self.y/bs):
				self.spawnmobs.append(((xpos, ypos), name, hp, (xvel, yvel), (itemid, count, NBTData)))
			else:
				ls += line

		regfile.close()

		regfile = open(self.path+"/worlds/%s/mobs/region%s.reg" % (wname, reg), 'w')
		regfile.write(ls)
	try: regfile.close()
	except:pass


class Block(Sprite):
	def save(self, wname):
		reg = region_get(int(self.x/bs), int(self.y/bs))
		path2 = self.path+"/worlds/%s/regions" % wname
		path3 = self.path+"/worlds/%s/regions/region%s.reg" % (wname, reg)
		if not isdir(path2):
			makedirs(path2)
		saved = False
		ls = ""
		dat = str(self.x/bs)+"_"+str(self.y/bs)+"_"

		ULS = dat+str(self.id)+"_"+str(self.oldest)+"_"+self.inventory_string+"\n"
		if isfile(path3):
			f = open(path3, 'r')
			for l in f.readlines():
				if dat in l:
					ls += ULS
					saved = True
				else:
					ls += l
			if not saved:
				ls+=ULS
			f.close()
			f = open(path3, 'w')
			f.write(ls)
			f.close()
		else:
			f = open(path3, 'w')
			ls+=ULS
			f.write(ls)
		f.close()
		

	def __init__(self, path, x, y, block_id, name, mode="start", blocks={}):
		Sprite.__init__(self)
		self.state = ""
		self.inventory_string = "E"
		self.spawnmobs = []
		self.image = Surface((bs,bs), SRCALPHA|HWSURFACE).convert_alpha()
		self.id = block_id

		self.data = BlockTypes[block_id]

#		self.blit_texture()

		try:
			self.x = int(x)
			self.y = int(y)
		except:
			print x, y
			#quit()
		self.path = path
		self.over = False
		self.preid = 0
		self.timer1 = 60
		self.wname = name
		self.destred = self.deststart = self.data.dest
		self.oldest = 0
		self.nbt_id = 0
		self.nbt_list = []
		loadId(self, name)
		self.grass_timer = 0
		self.generated = False
		self.timer2 = Delay()
		self.click22 = True
		self.start_clicked = 0
		self.drop_NBTData = 100
		self.first = True

		global BLD
		BLD = blocks
#		self.save(self.wname)
		#SPAWN FLEBER
		try:
			if time.time() % 10 == 0:
				if mode == "in_game":
					down_block = blocks[str(int(self.x/bs))+"_"+str(int(self.y/bs)+1)]
					if abs(int(int(self.x) + int(self.y) + int(time.time()*10))) % 100 == 0 and self.data.air and down_block.id == 3:
						for _ in xrange(1):
							self.spawnmobs.append(((self.x, self.y), "fleber", None, (0, 0), (0, 0, 0)))
		except KeyError:
			pass



	def create_nbt_id(self):
		return str(self.x//bs)+"_"+str(self.y//bs)

	def create_nbt_pos(self, x, y):
		return str(x//bs)+"_"+str(y//bs)

	def blit_texture(self):
		if self.data.alpha:
			self.image.fill((0,0,0,0))
		if self.data.visible:
			try: self.image.blit(self.data.texture[self.state], (0,0))
			except KeyError: self.image.blit(self.data.texture[''], (0,0))

	def sound(self):
		try:
			snd = SOUNDS[str(self.data.sound)]
			snd.set_volume(SOUND_VOLUME)
			snd.play()
		except KeyError:
			pass
	def reid(self):
		speed_break = 2
		try:
			itm = ItemTypes[id_item]
		except KeyError:
			itm = EMPTY_ITEM
		if self.data.material == itm.material:
			speed_break += itm.level
		if self.destred <= 0:
			self.drop_self()
			self.sound()
			self.reset_block(0)
			return True
		else:
			self.destred += -speed_break
			st = (int((float(self.destred) / float(self.deststart))*10))
			if self.data.visible:
				try:
					self.image.blit(TEXTURES["D"+str(st)], (0,0))
				except KeyError:
					pass
		return False
	def drop_self(self):
		drop_count = self.data.drop_count
		drop = 0
		if self.data.drop != None:
			drop = self.data.drop
		else:
			drop = self.id

		if drop != 0:
			try:
				NBT = ItemTypes[drop].durable
			except KeyError:
				NBT = 100
			self.spawnmobs.append(((self.x+bs//2, self.y+bs//2), "item", None, (0.0,-1.0), (drop, drop_count, NBT)))

	def reset_block(self, new_id, save=True):
		global BLD
		self.data = BlockTypes[new_id]
		self.id = new_id
		self.oldest = 0
		self.state = ''
		self.destred = self.deststart = self.data.dest
		if save:
			self.save(self.wname)
		if new_id == BLOCK_LEAD:
			try:
				up_block    = BLD[self.create_nbt_pos(self.x, self.y-bs)]

				try:left_block  = BLD[self.create_nbt_pos(self.x-bs, self.y)]
				except KeyError:left_block = None

				try: right_block = BLD[self.create_nbt_pos(self.x+bs, self.y)]
				except KeyError: right_block = None

				if up_block.id == BLOCK_LEAD:
					self.state = ''
					self.blit_texture()
					return None

				#print left_block, right_block
				if ((not left_block is None) and left_block.data.collable) or ((not right_block is None) and right_block.data.collable):
					self.state = 'up'
					self.blit_texture()
					return None
				else:
					self.drop_self()
					self.reset_block(0)

			except KeyError:
				pass
		self.blit_texture()

#UPDATE
	def update(self, mobs, blocks, id_it, rclick, inv, TIG, player):
		global BLD
		if self.first:
			self.reset_block(self.id, save=False)
			self.first = False
			if self.state:
				print self.state
		BLD = blocks
		if self.oldest == 0:
			self.oldest = TIG
		if self.destred != self.deststart:
			self.destred += 1
			if self.data.visible:
				st = (int((float(self.destred) / float(self.deststart))*10))
				self.blit_texture()
				if not self.data.alpha:
					try:
						self.image.blit(TEXTURES["D"+str(st)], (0,0))
					except KeyError:
						pass
		if self.id == 3:
			coords_data = str(self.x/bs)+"_"+str((self.y/bs-1))
			try:
				if blocks[coords_data].data.collable:
					self.reset_block(2)
			except KeyError:
				pass
		if self.id == 2:
			coords_data = str(self.x/bs)+"_"+str((self.y/bs-1))
#			print self.grass_timer
			try:
				if not blocks[coords_data].data.collable:
					if TIG-self.oldest >= 1000:
						self.oldest = TIG
						self.reset_block(3)
					if (TIG-self.oldest) % 200 == 0:
						self.save(self.wname)
			except KeyError:
				pass
		if self.id == 8:
			wood = False
			if (int(self.x)+int(self.y)+TIG) % 50 == 0 and self.oldest >= 1000 and int(dist(self.x, player.x, self.y, player.y)) <= 8*bs:
				for block_key in blocks:
					block = blocks[block_key]
					distance = dist(self.x, block.x, self.y, block.y)
					if int(distance) <= 4*bs:
						if block.id == 7:
							wood = True
				if not wood:
					self.reset_block(0)

		self.timer2.update()
		if self.timer2.get() >= 10 and self.id == 11:
			try:
				self.timer2.remove()
				coords_data1 = str(self.x/bs)+"_"+str((self.y/bs+1))
				bl1 = blocks[coords_data1]
				coords_data2 = str(self.x/bs+1)+"_"+str((self.y/bs))
				bl2 = blocks[coords_data2]
				coords_data3 = str(self.x/bs-1)+"_"+str((self.y/bs))
				bl3 = blocks[coords_data3]
				if bl1.id == 0 or bl1.id == 11:
					if bl1.id != 11:
						bl1.reset_block(11)
						self.save(self.wname)
				else:
					if bl2.id == 0:
						bl2.reset_block(11)
						self.save(self.wname)
					if bl3.id == 0:
						bl3.reset_block(11)
						self.save(self.wname)

			except KeyError:
				self.timer2.set(30)

		if self.id == 5:
			coords_data1 = str(int(self.x/bs))+"_"+str(int(self.y/bs)+1)
			try:
				bbl = blocks[coords_data1]
				if not bbl.data.collable:
					self.reset_block(0)
					return ("mob", (self.x, self.y), "fall_sand", 100)


					
			except KeyError:
				pass

		if self.id in (13,14,15,16):
			mytig = self.oldest
			if TIG-self.oldest >= 20000:
				self.reset_block(self.id+1)
				self.oldest = mytig+20000
			try:
				down_block = blocks[str(int(self.x/bs))+"_"+str(int(self.y/bs)+1)]
				if not down_block.data.collable:
					inv.add(self.id, 1, 100)
					self.reset_block(0)
				if (TIG-self.oldest)%10 == 0:
					self.save(self.wname)
			except KeyError:
				pass
		if self.id == 17:
			try:
				down_block = blocks[str(int(self.x/bs))+"_"+str(int(self.y/bs)+1)]
				if not down_block.data.collable:
					inv.add(-12, 1, 100)
					self.reset_block(0)
			except KeyError:
				pass
		global id_item
		id_item = id_it
		if self.id == 12:
			if not rclick:
				self.click22 = False
