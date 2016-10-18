#-*- coding: utf-8 -*-
from os import mkdir
from os.path import isdir, isfile
from pygame import Surface, mouse
from SbInterface import *
from SbDev import sb_output
from SbTerrain import unc_func
from pygame.image import load
from pygame import font

from SbCrafts import crafts
from SbConstants import *

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY100 = (100,100,100)
PINK = (255,0,255)
YELLOW = (255,255,0)

global temp
temp = 0
global temp_count
temp_count = 0
global temp_nbt
temp_nbt = 0
global mouse1
mouse1 = False
global mouse2
mouse2 = False


CRAFTS = crafts()

#
def add_to_inv(slots, BOI, BOIC, BOID): #Block Or Item, Block Or Item Count
	done = False
	for slot in slots:
		stack = slot.data.stack
		if slot.id  == BOI:
			if BOIC <= stack-slot.count:
				slot.id = BOI
				slot.count += BOIC
				slot.NBTData = BOID
				return 0
			else:
				BOIC -= stack-slot.count
				slot.count += stack-slot.count
				if BOIC == 0:
					return 0
	for slot in slots:
		stack = slot.data.stack
		if slot.id == 0 or slot.id == BOI:
			if BOIC <= stack-slot.count:
				slot.id = BOI
				try:
					slot.data = ItemTypes[BOI]
				except:
					slot.data = EMPTY_ITEM
				slot.count += BOIC
				if BOID != 0:
					slot.NBTData = BOID
				else:
					slot.NBTData = 100
				done = True
				return 0
			else:
				BOIC -= stack-slot.count
				slot.count += stack-slot.count
				if BOIC == 0:
					break
	return BOIC







class Slot():
	def __init__(self, pos, pos1, path, setable=True, pickable=True):
		self.text = font.Font(path+"/resources/FreeSansBold.ttf", 12)
		self.pos = pos
		self.pos1 = pos1
		self.id = 0
		self.count = 0
		self.freeze = False
		self.sise = (bs+2,bs+2)
		self.image = Surface(self.sise)
		self.path = path
		self.duble_timer = 0
		self.NBTData = 100
		self.white = Surface(self.sise)
		self.white.fill(WHITE)
		self.black = Surface(self.sise)
		self.black.fill(GRAY100)
		self.image.convert()
		self.setable = setable
		self.pickable = pickable
		self.data = EMPTY_ITEM
#Обновление слота
	def update(self,click1, click2, slots, mode, shift, second_slots):
		if self.id in ItemTypes:
			self.data = ItemTypes[self.id]
		if second_slots is None:
			second_slots = slots
		preid = self.id
		if self.count <= 0:
			self.id = 0
		if mode == 0:
			mp = mouse.get_pos()
			if self.duble_timer >= 1:
				self.duble_timer += -1
			if mp[0] > self.pos[0]+self.pos1[0] and mp[0] < self.pos1[0]+self.pos[0]+self.sise[0] and mp[1] > self.pos[1]+self.pos1[1] and mp[1] < self.pos1[1]+self.pos[1]+self.sise[1]:
				self.image.blit(self.white, (0,0))
				global mouse1
	#--------
				#ЛЕВЫЙ КЛИК НА СЛОТ
				if (click1 and not mouse1) or (click1 and shift):
					global temp
					global temp_count
					global temp_nbt
					if self.duble_timer == 0:
						self.duble_timer = 20
					else:

						stack = self.data.stack
						#ДВОЙНОЙ КЛИК ЛЕВЫЙ
						for slot in slots:
							if slot.id == temp and slot.pickable:
								if slot.count <= stack-temp_count:
									temp_count += slot.count
									slot.count = 0
									slot.id = 0
								else:
									slot.count -= stack-temp_count
									temp_count += stack-temp_count
					if not shift:
						if temp != self.id:
							if temp == 0 or self.setable:
								temp1 = temp
								temp3 = temp_nbt
								temp1_c = temp_count
								temp = self.id
								temp_nbt = self.NBTData
								self.NBTData = temp3
								del temp3
								temp_count = self.count
								self.id = temp1
								self.count = temp1_c
						if temp == self.id and self.setable:
							stack = self.data.stack
							if temp_count <= stack-self.count:
								self.count += temp_count
								temp_count = 0
								temp = 0
							else:
								temp_count = temp_count-(stack-self.count)
								self.count += stack-self.count
					else:
						sl_id = self.id
						sl_count = self.count
						sl_NBTData = self.NBTData

						self.id = 0
						self.data = EMPTY_ITEM
						self.count = 0
						self.NBTData = 100

						add_to_inv(second_slots, sl_id, sl_count, sl_NBTData)
					mouse1 = True
				if not click1:
					mouse1 = False
	#--------
				#ПРАВЫЙ КЛИК НА СЛОТ
				global mouse2
				if click2 and not mouse2 and self.setable:
					global temp
					global temp_count
					if temp == 0:
						if self.id != 0 and self.count != 1:
							temp2 = self.count
							self.count = int(self.count/2)
							temp_count = temp2 - self.count
							mouse2 = True
							temp = self.id
					else:
						
						if temp == self.id or self.id == 0:
							stack = self.data.stack
							if not self.freeze and self.count < stack:
								self.id = temp
								self.count += 1
								temp_count += -1
								self.freeze = True
								if temp_count == 0:
									temp = 0
					
				if not click2 and self.setable:
					mouse2 = False
					self.freeze = False
					for slot in slots:
						if mp[0] > slot.pos[0]+slot.pos1[0] and mp[0] < slot.pos1[0]+slot.pos[0]+slot.sise[0] and mp[1] > slot.pos[1]+slot.pos1[1] and mp[1] < slot.pos1[1]+slot.pos[1]+slot.sise[1]:
							pass
						else:
							slot.freeze = False
							slot.image.fill(GRAY100)

	#--------------------
			else:
				if self.freeze:
					self.image.fill(YELLOW)
				else:
					self.image.fill(GRAY100)
		if mode == 1:
			self.image.blit(self.black, (0,0))
		if self.id != 0:
			if self.id <= -1:
				self.data = ItemTypes[self.id]
				self.image.blit(self.data.texture, (2,2))
			else:
				self.image.blit(BlockTypes[self.id].texture[''], (2,2))

		#NBTDATA
		if self.data.tool:
			try:
				pers1 = float(float(self.NBTData)/float(self.data.durable))
				NBT_SURF = Surface((int(float(float(self.NBTData)/float(self.data.durable))*bs), 4))
				NBT_SURF.fill((int(255-pers1*255),int(pers1*255),0))
				self.image.blit(NBT_SURF, (0,bs-4))
			except:
				pass
		if self.count > 1:
			dopsurf = pygame.Surface((30, 20))
			dopsurf.set_alpha(150)
			self.image.blit(dopsurf, (30, 35))
			self.image.blit(self.text.render(str(self.count), 0, (200, 200, 0)), (30,35))

		if self.id != preid and preid != 0:
			return True
		else:
			return False






#ИНВЕНТАРЬ----------------------------------------------------------------------------------------
class Inventory():
	def __init__(self, path, wname, pos=(260,10), canion=5, width=700, height=300):
		self.cursor_text = font.Font(path+"/resources/FreeSansBold.ttf", 14)
		self.width = width
		self.height = height
		self.image = Surface((width,height))
		self.texture = load(path+"/resources/textures/qui/inventory.png")
		self.path = path
		self.pos = pos
		self.slots = []
		self.cursor_image = Surface((bs,bs))
		self.wname = wname
		slot = 0
		slot_y = 0
		filed = False
		self.craft_slots = []
		try:
			ff = open("%s/worlds/%s/inventory.dat" % (self.path, self.wname), 'r')
			f = ff.readlines()
			filed = True
		except IOError:
			pass
		loaded = -999
		if filed:
			if "MihailRis"  in f[0]:
				loaded = 0
			else:
				print "Так чья это игра?"
		while slot != 5:
			while slot_y != 10:
				y = slot*(bs+canion)
				x = slot_y*(bs+canion)
				sl = Slot((x+canion*2,y+canion*2), pos, path)
				self.slots.append(sl)
				slot_y += 1
				loaded += 1
				if filed:
					slot_data = f[loaded][0:-1].split("_")
					sl.id = int(slot_data[0])
					sl.count = int(slot_data[1])
					sl.NBTData = int(slot_data[2])
			slot += 1
			slot_y = 0
		try:ff.close()
		except NameError:pass
		self.craft_slots.append(Slot((12*bs-canion,canion*2), pos, path))
		self.craft_slots.append(Slot((13*bs,canion*2), pos, path))
		self.craft_slots.append(Slot((14*bs+canion,canion*2), pos, path))



		self.craft_slots.append(Slot((12*bs-canion,canion*3+bs), pos, path))
		self.craft_slots.append(Slot((13*bs,canion*3+bs), pos, path))
		self.craft_slots.append(Slot((14*bs+canion,canion*3+bs), pos, path))

		self.craft_slots.append(Slot((12*bs-canion,canion*4+bs*2), pos, path))
		self.craft_slots.append(Slot((13*bs,canion*4+bs*2), pos, path))
		self.craft_slots.append(Slot((14*bs+canion,canion*4+bs*2), pos, path))

		self.craft_result_slot = Slot((13*bs,canion*6+bs*3), pos, path, setable=False)



	def save(self):
		inv_data = "Zendes 2.5 inventory save file, game created by MihailRis\n"
		path = "%s/worlds/%s" % (self.path, self.wname)
		for slot in self.slots:
			data_slot = "%s_%s_%s\n" % (slot.id, slot.count, slot.NBTData)
			inv_data += data_slot
		ffile = open(path+"/inventory.dat", 'w')
		ffile.write(inv_data)
		ffile.close()
		
		


	def add(self, BOI, BOIC, BOID): #Block Or Item, Block Or Item Count
		return add_to_inv(self.slots, BOI, BOIC, BOID)


	def update(self, click1, click2, shift, second_slots1, color=(200,200,200), t=2):
		global temp_count
		w = self.width
		h = self.height
		self.image.blit(self.texture, (0,0))
		global temp

		##CRAFT###################################################
		completed = False
		ccraft = None
		for craft1 in CRAFTS:
			if not completed:
				for x in xrange(0, 9):
					craft = CRAFTS[craft1]
					if not craft[-1][2]:
						if (self.craft_slots[x].id == craft[x][0] and
							self.craft_slots[x].count >= craft[x][1]):
							completed = True
						else:
							completed = False
							break

				if completed:
					ccraft = craft
					break
		if completed:
			self.craft_result_slot.id = ccraft[-1][0]
			self.craft_result_slot.count = ccraft[-1][1]
			if ccraft[-1][0] < 0:
				self.craft_result_slot.NBTData = ItemTypes[ccraft[-1][0]].durable
		else:
			self.craft_result_slot.id = 0
			self.craft_result_slot.count = 0

		picked = self.craft_result_slot.update(click1, click2, (self.craft_result_slot,), 0, shift, self.slots)
		if picked:
			for x in xrange(0, 9):
				if self.craft_slots[x].id != 0:
					if self.craft_slots[x].count != ccraft[x][1]:
						self.craft_slots[x].count += -ccraft[x][1]
					else:
						self.craft_slots[x].count = 0
						self.craft_slots[x].id = 0


		self.image.blit(self.craft_result_slot.image, self.craft_result_slot.pos)
		#######################################################

		self.cursor_image.fill(PINK)
		self.cursor_image.set_colorkey(PINK)


		if temp <= -1:
			self.cursor_image.blit(ItemTypes[temp].texture, (0,0))			
		else:
			self.cursor_image.blit(BlockTypes[temp].texture[''], (0,0))
		#SLOTS
		for sl1 in self.slots:
			sl1.update(click1, click2, self.slots, 0, shift, second_slots=second_slots1)
			self.image.blit(sl1.image, sl1.pos)

		for sl2 in self.craft_slots:
			sl2.update(click1, click2, self.craft_slots, 0, shift, second_slots=self.slots)
			self.image.blit(sl2.image, sl2.pos)
		if temp_count > 1:
			self.cursor_image.blit(self.cursor_text.render(str(temp_count), 0, (250, 250, 0)), (17,20))




class State_icon():
	def __init__(self, number, path, state):
		self.texture2 = load(path+"/resources/textures/qui/"+state+"1.png")
		self.texture1 = load(path+"/resources/textures/qui/"+state+"0.png")
		self.number = number
		self.path = path
		self.image = Surface((bs,bs))
	def update(self, def_value, value):
		percent = int(float(value*2)/float(def_value)*10.0)+1
		if self.number >= int(percent):
			self.texture = self.texture1
		else:
			self.texture = self.texture2

class State_Panel():
	def __init__(self, path):
		self.sise = (600,100)
		self.image = Surface(self.sise, pygame.SRCALPHA)
#		self.hp_text = font.Font(path+"/resources/FreeSansBold.ttf", 13)
		self.state_icons = []
		for x in xrange(1, 20):
			self.state_icons.append(State_icon(x,path,"heart"))
		self.state_icons2 = []
		for x in xrange(1, 20):
			self.state_icons2.append(State_icon(x,path,"air"))
		self.state_icons3 = []
		for x in xrange(1, 20):
			self.state_icons3.append(State_icon(x,path,"hunger"))
#		self.state_icons2.append(State_icon(10,path,"air"))
	def update(self, player):
		x = 0
		x2 = 0
		x3 = 0
		self.image.fill((0,0,0,0))
#		self.image.set_colorkey(PINK)
		for icon in self.state_icons:
			icon.update(20, player.hp)
			self.image.blit(icon.texture, (x,0))
			x+=25
		if player.air < 20:
			for icon in self.state_icons2:
				icon.update(20, player.air)
				self.image.blit(icon.texture, (x2,50))
				x2+=25

		for icon in self.state_icons3:
			icon.update(20, int(player.hunger))
			self.image.blit(icon.texture, (x3,25))
			x3+=25



#		self.image.blit(self.hp_text.render(u"Здоровье: %s" % player.hp, 0, (200,0,0)), (10,10))



class DownTory():
	def __init__(self, SIZE, path, inv):
		self.sise = ((bs+2)*10,bs+4)
		self.side = (400,SIZE[1]-(bs*2)-self.sise[1])
		self.selected = 0
		self.slots = []
		self.path = path
		while len(self.slots) <= 10:
			slot0 = Slot((len(self.slots)*(bs+2), 0), self.side, path)
			self.slots.append(slot0)
		self.image = Surface(self.sise)
		self.selector = Surface((bs,2))
		self.selector.fill((255,255,0))
		self.im = Surface(self.sise)
		self.im.fill((50,50,50))
		self.inv = inv

	def update(self, up, down):
		self.image.blit(self.im, (0,0))
		if up:
			self.selected += 1
			if self.selected == 10:
				self.selected = 0
		if down:
			self.selected += -1
			if self.selected == -1:
				self.selected = 9
		for slot in self.slots:
			orig_slot = self.inv.slots[(self.slots.index(slot))]
			orig_slot.update(False, False, self.inv.slots, 1, False, 1)
			slot.image = orig_slot.image
			slot.id = orig_slot.id
			slot.count = orig_slot.count
			slot.NBTData = orig_slot.NBTData
			if slot.id != 0:
				self.image.blit(orig_slot.image, slot.pos)
		self.image.blit(self.selector, (self.selected*(bs+2)+2, 0))
	def get(self):
		give_r = self.slots[self.selected].id
		return give_r

def useitem(selectid, player, blocks_dict, selected_slot, inventory, bmp):
	if ItemTypes[selectid].eat:
		if float(player.hunger) < 20:
			if selected_slot.NBTData <= 0:
				selected_slot.count += -1
				selected_slot.NBTData = ItemTypes[selectid].durable
				if selected_slot.count <= 0:
					selected_slot.id = 0
					selected_slot.count = 0
					selected_slot.NBTData = 100
				player.hunger += ItemTypes[selectid].eat
				eated = 100
			else:
				selected_slot.NBTData += -1
	if selectid == -14:
		if bmp.id == 0:
			bmp.reset_block(13)
			selected_slot.count += -1
			if selected_slot.count <= 0:
				selected_slot.id = 0
				selected_slot.count = 0
				selected_slot.NBTData = 100



