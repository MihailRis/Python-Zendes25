#-*- coding: utf-8 -*-
#Zendes 2.5 game constains
from pygame import transform, mixer, Surface, display
from pygame.image import load
from os import listdir
import time as timep
import sys
import math
#from SbColorFilter import *

mixer.init()

_path_1 = sys.path[1]

def resz(size):
	return max(int(float(size)*float(sz)), 1)

def reszy(size):
	return max(int(float(size)*float(szy)), 1)

#SCREEN_SIZE_MODE = "auto"
SCREEN_SIZE_MODE = "1024_720"

if SCREEN_SIZE_MODE == "auto":
	display.init()

	infoObject = display.Info()
	SIZE000 = (infoObject.current_w, infoObject.current_h)
else:
	splitted = SCREEN_SIZE_MODE.split("_")
	SIZE000 = int(splitted[0]),int(splitted[1])

sz = float(SIZE000[0])/1440.0
szy = float(SIZE000[1])/855.0

sz = 1.3
szy = 1.3

print sz


bs = int(45.0*sz)
SIZE = (int(1440.0*sz), int(855.0*szy))

import SbGenerator

gs = 100
recmax = 2

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
BLUELIGHT = (100,100,255)
PINK = (255,0,255)



RELOAD_LIBS = False

FONTNAME = "FreeSansBold"

def dist(x1,x2, y1,y2):
	k = ((x2-x1)**2 + (y2-y1)**2); #Формула расстояния между двумя точками
	k1 = math.sqrt(k)
	return k1

Slot1 = None

def slot_get(slot):
	global Slot1
	Slot1 = slot

un = 1.0

TEXTURES = {}
last_timep = timep.time()

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

try:
	for texture in listdir(_path_1+"/resources/textures/blocks"):
		texture_name = texture.split(".")[0]
		TEXTURES[texture_name] = transform.scale(load(_path_1+"/resources/textures/blocks/"+texture), (bs,bs))

	for texture in listdir(_path_1+"/resources/textures/items"):
		texture_name = texture.split(".")[0]
		TEXTURES[texture_name] = transform.scale(load(_path_1+"/resources/textures/items/"+texture), (bs,bs))

	for texture in listdir(_path_1+"/resources/textures/destroy"):
		texture_name = texture.split(".")[0].split("_")[1]
		TEXTURES["D"+texture_name] = transform.scale(load(_path_1+"/resources/textures/destroy/"+texture), (bs,bs))
	print "textures loaded in %s seconds" % (timep.time()-last_timep)
except OSError:
	print "textures not loaded"
del last_timep


SOUNDS = {}
try:
	for sound in listdir(_path_1+"/resources/sounds/blocks"):
		sound_name = sound.split(".")[0]
		SOUNDS[sound_name] = mixer.Sound(_path_1+"/resources/sounds/blocks/"+sound)

	for sound in listdir(_path_1+"/resources/sounds/effects"):
		sound_name = sound.split(".")[0]
		SOUNDS[sound_name] = mixer.Sound(_path_1+"/resources/sounds/effects/"+sound)
except OSError:
	print "sounds not loaded"

sh_format = 'png'


class BlockType:
	def __init__(self,
				 sound=None, 
				 texture=("air",), 
				 dest=1, 
				 collable=True,
				 alpha=False,
				 drop=None,
				 drop_count=1,
				 drop_NBTData=100,
				 visible=True,
				 material=None,
				 air=False,
				 replacement=False,
				 inv=False):

		if type(texture) == str: texture = (texture,)
		self.sound = sound
		self.texture = {}
		for tindex in texture:
			try: ttindex = tindex.split("__")[1]
			except IndexError: ttindex = ""
			self.texture[ttindex] = TEXTURES[tindex]
		self.dest = dest
		self.collable = collable
		self.alpha = alpha
		self.drop = drop
		self.drop_count = drop_count
		self.drop_NBTData = drop_NBTData
		self.visible = visible
		self.material = material
		self.air = air
		self.replacement = replacement
		self.inv = inv

class BlockInv:
	def __init__(self, block, sise=5, pos=(970, 10), canion=5):
		self.block = block
		self.pos = pos
		Sise = (int(sise*bs+canion*(sise+4)),int(sise*bs+canion*(sise+4)))
		self.sise = Sise
		self.orgsise = sise
		self.image = Surface(Sise)
		self.texture = load(_path_1+"/resources/textures/qui/chest.png")
		self.slots = []
		slot = 0
		slot_y = 0
		while slot != sise:
			while slot_y != sise:
				y = slot*(bs+canion)
				x = slot_y*(bs+canion)
				sl = Slot1((x+canion*2,y+canion*2), pos, _path_1)
				self.slots.append(sl)
				slot_y += 1
			slot += 1
			slot_y = 0
		self.load()
	def save(self, path, wname):
		slots_data = []
		for slot in self.slots:
			slots_data.append("%s!%s!%s" % (slot.id, slot.count, slot.NBTData))
		self.block.inventory_string = "I"+"$".join(slots_data)
		self.block.save(self.block.wname)
		

	def update(self, click, click2, shift, second_slots=None):
		self.image.blit(transform.scale(self.texture, self.sise), (0,0))
		for slot in self.slots:
			slot.update(click, click2, self.slots, 0, shift, second_slots)
			self.image.blit(slot.image, slot.pos)

	def load(self):
		inv_str = self.block.inventory_string
		if inv_str != "E":
			strslots = inv_str[1:].split("$")
			islen = len(strslots)
			for xx in xrange(self.orgsise*self.orgsise):
				if xx <= islen-1:
					slot_data = strslots[xx].split("!")
					slot = self.slots[xx]
					slot.id = int(slot_data[0])
					slot.count = int(slot_data[1])
					slot.NBTData = int(slot_data[2])
		

#IDS
BLOCK_AIR = 0
BLOCK_STONE = 1
BLOCK_DIRT = 2
BLOCK_GRASS = 3
BLOCK_COAL = 4
BLOCK_SAND = 5
BLOCK_DIAMOND = 6
BLOCK_WOOD = 7
BLOCK_FOLIAGE = 8
BLOCK_IRON = 9
BLOCK_WATER = 11

BLOCK_TNT = 12

BLOCK_WHEAT_1 = 13
BLOCK_WHEAT_2 = 14
BLOCK_WHEAT_3 = 15
BLOCK_WHEAT_4 = 16
BLOCK_WHEAT_5 = 17

BLOCK_SNOWED_GRASS = 18
BLOCK_SNOW = 19
BLOCK_PLANKS = 20
BLOCK_CHEST = 21
BLOCK_COBBLESTONE = 22
BLOCK_SANDSTONE = 23
BLOCK_APPLE_LEAVES = 24
BLOCK_MEGA_CRYSTAL = 25
BLOCK_LEAD = 26


ITEM_STICK = -1
ITEM_STONE_PICKAXE = -2
ITEM_IRON_PICKAXE = -3
ITEM_DIAMOND_PICKAXE = -4
ITEM_MEGA_CRYSTAL = -5
ITEM_DIAMOND = -6
ITEM_STONE_SHOVEL = -7
ITEM_IRON_SHOVEL = -8
ITEM_DIAMOND_SHOVEL = -9
ITEM_IRON_INGOT = -10
ITEM_BREAD = -11
ITEM_WHEAT = -12
ITEM_FLOUR = -13
ITEM_WHEAT_SEEDS = -14
ITEM_TORCH = -15
ITEM_STONE_COAL = -16
ITEM_IRON_AXE = -17
ITEM_STONE_AXE = -18
ITEM_APPLE = -19
ITEM_STONE_SWORD = -20


# BLOCKS
AIR_BLOCK        = BlockType(collable=False, alpha=True, visible=False, air=True, replacement=True)
STONE_BLOCK      = BlockType(sound="stone", texture="stone",     dest=200*un, material="stone", drop=BLOCK_COBBLESTONE)
DIRT_BLOCK       = BlockType(sound="dirt",  texture="dirt",      dest=20*un, material="dirt")
GRASS_BLOCK      = BlockType(sound="grass",  texture="grass",     dest=25*un, drop=BLOCK_DIRT, material="dirt")
COAL_ORE         = BlockType(sound="stone", texture="coal_ore",     dest=400*un, drop=-16, drop_count=3, material="stone")
SAND_BLOCK       = BlockType(sound="dirt",  texture="sand",      dest=15*un, material="dirt")
DIAMOND_ORE      = BlockType(sound="stone",  texture="diamond_ore",  dest=1500*un, drop=-6, drop_count=3, material="stone")
WOOD_BLOCK       = BlockType(sound="wood",  texture="wood",      dest=100*un, collable=False, material="wood", air=True)
LEAVES_BLOCK     = BlockType(sound="leaves",  texture="leaves",    dest=15*un, collable=False, alpha=False, material="leaves", air=True)
IRON_ORE         = BlockType(sound="stone",  texture="iron_ore", dest=600*un, material="stone")
COAL_BLOCK       = BlockType(sound="stone",  texture="coal_block", dest=120*un, material="stone")
WATER_BLOCK      = BlockType(sound="stone", texture="water",     dest=9789573489*un, collable=False, alpha=True, replacement=True)
TNT_BLOCK        = BlockType(sound="wood", texture="tnt",     dest=10*un, material="wood")

WHEAT_BLOCK_1    = BlockType(sound="leaves", texture="wheat_stade1", alpha=True, collable=False, drop=-14)
WHEAT_BLOCK_2    = BlockType(sound="leaves", texture="wheat_stade2", alpha=True, collable=False, drop=-14)
WHEAT_BLOCK_3    = BlockType(sound="leaves", texture="wheat_stade3", alpha=True, collable=False, drop=-14)
WHEAT_BLOCK_4    = BlockType(sound="leaves", texture="wheat_stade4", alpha=True, collable=False, drop=-14)
WHEAT_BLOCK_5    = BlockType(sound="leaves", texture="wheat_stade5", alpha=True, collable=False, drop=-12)

SNOWED_GRASS_BLOCK = BlockType(sound="grass",  texture="snowed_grass", dest=24*un, drop=BLOCK_DIRT, material="dirt")
SNOW_BLOCK         = BlockType(sound="dirt",   texture="snow", dest=12*un, material="dirt")
PLANKS_BLOCK       = BlockType(sound="wood",   texture="planks", dest=90*un, material="wood")
CHEST_BLOCK        = BlockType(sound="wood",  texture="chest",      dest=80*un, material="wood", inv=(5))

COBBLESTONE_BLOCK  = BlockType(sound="stone", texture="cobblestone",     dest=180*un, material="stone")
SANDSTONE_BLOCK    = BlockType(sound="stone", texture="sandstone",     dest=120*un, material="stone")

APPLE_LEAVES_BLOCK = BlockType(sound="leaves",  texture="apple_leaves",    dest=18*un, collable=False, alpha=False, material="leaves", air=True, drop=-19, drop_count=2, drop_NBTData=300)
MEGA_CRYSTAL_BLOCK = BlockType(sound="stone", texture="mega_crystal_block",     dest=4000*un, drop=ITEM_MEGA_CRYSTAL, drop_count=9, material="stone")
LEAD_BLOCK         = BlockType(sound="wood", texture=("lead", "lead__up"),     dest=20*un, material="wood", collable=False, air=True)


BlockTypes = {
				0:AIR_BLOCK,
				1:STONE_BLOCK,
				2:DIRT_BLOCK,
				3:GRASS_BLOCK,
				4:COAL_ORE,
				5:SAND_BLOCK,
				6:DIAMOND_ORE,
				7:WOOD_BLOCK,
				8:LEAVES_BLOCK,
				9:IRON_ORE,
				10:COAL_BLOCK,
				11:WATER_BLOCK,
				12:TNT_BLOCK,

				13:WHEAT_BLOCK_1,
				14:WHEAT_BLOCK_2,
				15:WHEAT_BLOCK_3,
				16:WHEAT_BLOCK_4,
				17:WHEAT_BLOCK_5,

				18:SNOWED_GRASS_BLOCK,
				19:SNOW_BLOCK,
				20:PLANKS_BLOCK,
				21:CHEST_BLOCK,
				22:COBBLESTONE_BLOCK,
				23:SANDSTONE_BLOCK,
				24:APPLE_LEAVES_BLOCK,
				25:MEGA_CRYSTAL_BLOCK,
				26:LEAD_BLOCK,
				}

def find_block(blocks, x, y, block_id):
	direction = 1

	x1 = int(x/bs)
	y1 = int((y+10)/bs)

	maxiter = 300
	itered = 0
	while itered < maxiter:	
		block_data = "_".join((str(int(x1/bs)),str(int(y1/bs))))
		print x
		if block_data in blocks:
			block = blocks[block_data]
			if block.id == block_id:
				return 1
			x1 += direction
		else:
			x1 = int(x/bs)
			direction = -1
		itered += 1
	return direction


class ItemType:
	def __init__(self,
				texture="",
				material=None,
				level=1,
				eat=0,
				clickable=False,
				set_block=0,
				stack=50,
				durable=101,
				inv_string="E",
				damage=0,
				tool=False,
				):
		self.texture = None
		if texture is not "":
			self.texture = TEXTURES[texture]
		self.material = material
		self.level = level
		self.eat = eat
		self.clickable = clickable
		self.set_block = set_block
		self.stack = stack
		self.durable = durable
		self.inv_string = inv_string
		self.damage = damage
		self.tool = tool

# ITEMS
EMPTY_ITEM = ItemType()
STICK_ITEM = ItemType(texture="stick")
STONE_PICKAXE = ItemType(material="stone", stack=1, texture="stone_pickaxe", level=2, durable=100, tool=True)
IRON_PICKAXE = ItemType(material="stone", stack=1, texture="iron_pickaxe", durable=250, level=4, tool=True)
DIAMOND_PICKAXE = ItemType(material="stone", stack=1, texture="diamond_pickaxe", durable=1000, tool=True, level=15)
MEGA_CRYSTAL = ItemType(stack=9, texture="mega_crystal", damage=100)
DIAMOND = ItemType(texture="diamond")
STONE_SHOVEL = ItemType(material="dirt", texture="stone_shovel", durable=100, level=2, tool=True)
IRON_SHOVEL = ItemType(material="dirt", texture="iron_shovel", durable=250, level=4, tool=True)
DIAMOND_SHOVEL = ItemType(material="dirt", texture="stone_shovel", durable=1000, tool=True)
IRON_INGOT = ItemType(texture="iron_ingot")
BREAD = ItemType(texture="bread", durable=60, eat=4, tool=True)
WHEAT = ItemType(texture="wheat")
FLOUR = ItemType(texture="flour", durable=10, eat=1, tool=True)
WHEAT_SEEDS = ItemType(texture="wheat_seeds", durable=20, eat=1, set_block=BLOCK_WHEAT_1, tool=True)
TORCH = ItemType(texture="torch", durable=4, clickable=True)
STONE_COAL = ItemType(texture="stone_coal")
IRON_AXE = ItemType(material="wood", texture="iron_axe", durable=250, level=4, tool=True)
STONE_AXE = ItemType(material="wood", texture="stone_axe", durable=100, level=2, tool=True)
APPLE = ItemType(texture="apple", durable=100, eat=1, tool=True)
STONE_SWORD = ItemType(texture="stone_sword", damage=1, durable=100, tool=True)






ItemTypes = {
			0:EMPTY_ITEM,
			-1:STICK_ITEM,
			-2:STONE_PICKAXE,
			-3:IRON_PICKAXE,
			-4:DIAMOND_PICKAXE,
			-5:MEGA_CRYSTAL,
			-6:DIAMOND,
			-7:STONE_SHOVEL,
			-8:IRON_SHOVEL,
			-9:DIAMOND_SHOVEL,
			-10:IRON_INGOT,
			-11:BREAD,
			-12:WHEAT,
			-13:FLOUR,
			-14:WHEAT_SEEDS,
			-15:TORCH,
			-16:STONE_COAL,
			-17:IRON_AXE,
			-18:STONE_AXE,
			-19:APPLE,
			-20:STONE_SWORD,
			}

