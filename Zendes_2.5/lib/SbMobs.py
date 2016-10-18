# -*- coding: utf-8 -*-
from os import makedirs
from os.path import isdir, isfile
from pygame import Surface, image, mouse, transform
from SbAnimation import Animation
from SbConstants import *
from pygame.time import Clock
from SbDev import region_get, dist
import time

STANDART_PLAYER_DAMAGE_TIMER = 10


fleber = {"type": "agres", "name":"fleber", "hp":15, "sise":(40,40), "texture": "main.png", "damage": 1, "player_damage_delay": STANDART_PLAYER_DAMAGE_TIMER}
fall_sand = {"type": "block", "name": "fall_sand", "hp": 1000, "sise": (bs,bs), "texture": "main.png", "damage": 0, "player_damage_delay": STANDART_PLAYER_DAMAGE_TIMER, "set_block":5}
item = {"type": "item", "name": "item", "hp": 1, "sise": (20,20), "texture": "main.png", "damage": 0, "player_damage_delay": STANDART_PLAYER_DAMAGE_TIMER}

MOBS = {fleber["name"]:fleber, fall_sand["name"]:fall_sand, item["name"]:item}

PINK = (255,0,255)
BLACK = (0,0,0)








class Mob():
	def __init__(self, name, path, pos, wname, item=(0,0,0)):
		from SbDev import Collide, Delay
		self.data = MOBS[name]
		self.path = path
		self.image = Surface(self.data["sise"])
		self.id = 0
		self.count = 0
		self.NBTData = 0
		if self.data["type"] != "item":
			self.texture = transform.scale(image.load("%s/resources/textures/mobs/%s/%s" % (path, self.data["name"], self.data["texture"])),(bs,bs))
			self.image.blit(self.texture, (0,0))
		else:
			self.id = item[0]
			self.count = item[1]
			self.NBTData = item[2]
			if self.id >= 0:
				self.texture = transform.scale(BlockTypes[self.id].texture[''], (int(self.data["sise"][0]*sz),int(self.data["sise"][1]*sz)))
			else:
				self.texture = transform.scale(ItemTypes[self.id].texture, (int(self.data["sise"][0]*sz),int(self.data["sise"][1]*sz)))
			self.image = self.texture.copy()

		self.x = pos[0]
		self.y = pos[1]
		self.visible = True
		self.xvel = 0
		self.yvel = 0
		self.onground = False
		self.started = False
		self.timer = Delay()
		self.wname = wname
		self.right = True
		self.dt = 0
		self.clock = Clock()
		self.damage_texture = image.load("%s/resources/textures/mobs/%s/damage.png" % (path, self.data["name"]))
		self.damage_timer = 0
		self.player_damage_timer = 0
		try:
			self.hp
		except AttributeError:
			self.hp = self.data["hp"]
		if self.data["type"] == "agres":
			self.rightanim = Animation((image.load("%s/resources/textures/mobs/%s/rightw.png" % (path, self.data["name"])), 
										image.load("%s/resources/textures/mobs/%s/rightw2.png" % (path, self.data["name"])),
										image.load("%s/resources/textures/mobs/%s/main.png" % (path, self.data["name"]))), 150)
			self.leftanim = Animation((image.load("%s/resources/textures/mobs/%s/leftw.png" % (path, self.data["name"])), 
										image.load("%s/resources/textures/mobs/%s/leftw2.png" % (path, self.data["name"])),
										image.load("%s/resources/textures/mobs/%s/left.png" % (path, self.data["name"]))), 150)

		if self.data["type"] == "block":
			self.yvel = 5.0

	def damage(self, hp=0):
		if hp >= 1:
			self.hp += -hp
		if self.damage_timer == 0:
			self.yvel = -4.0
			self.hp -= 3
		self.damage_timer = 15

	# Нанесение урона персонажу
	def damage_player(self, player, camfunced, damage, dist_to_player):
		camfunced1 = (camfunced[0]-1*bs, camfunced[1]-1*bs)
		if damage != 0:
			if dist_to_player < 2*bs:
				player.hp += -damage
				player.yvel = -2
				if self.x > player.x:
					player.xvel += -10
				else:
					player.xvel += 10
		return dist_to_player

	def mob_move(self, player, dist_to_player):
		tick = self.timer.get()
		# Передвижение моба
		if tick == 1:
			if dist_to_player < 6*bs:
				if player.x > self.x:
					if self.xvel < 3.0:
						self.xvel += 0.5
					self.right = True
				else:
					if self.xvel > -3.0:
						self.xvel += -0.5
					self.right = False
			else:
				if (self.dt//50+int(time.time())/5) % 2:
					direction = 1
				else:
					direction = -1
				if direction > 0:
					if self.xvel < 1.0:
						self.xvel += 0.5
					self.right = True
				else:
					if self.xvel > -1.0:
						self.xvel += -0.5
					self.right = False
			self.timer.remove()

	# Сохранение данных моба
	def save(self):
		path = "%s/worlds/%s/mobs" % (self.path, self.wname)
		if not isdir(path):
			makedirs(path)
		reg = region_get(int(self.x/bs), int(self.y/bs))
		data = (str(int(self.x))+"#"+str(int(self.y)))+"#"
		if isfile(path+"/region%s.reg" % reg):
			ls = ""
			regfile = open(path+"/region%s.reg" % reg, 'r')
			reglines = regfile.readlines()
			saved = False
			for l in reglines:
				if data in l:
					ls += data+"%s#%s#%s#%s#%s#%s#%s\n" % (self.data["name"], self.hp, self.xvel, self.yvel, self.id, self.count, self.NBTData) # name, hp, xvel, yvel
					regfile.close()
					saved = True
				else:
					ls += l
			if not saved:
				ls += data+"%s#%s#%s#%s#%s#%s#%s\n" % (self.data["name"], self.hp, self.xvel, self.yvel, self.id, self.count, self.NBTData) # name, hp, xvel, yvel
				regfile.close()
				regfile = open(path+"/region%s.reg" % reg, 'w')
				regfile.write(ls)
				regfile.close()

		else:
			regfile = open(path+"/region%s.reg" % reg, 'w')
			regfile.write(data+"%s#%s#%s#%s#%s#%s#%s\n" % (self.data["name"], self.hp, self.xvel, self.yvel, self.id, self.count, self.NBTData))
			regfile.close()
		try:regfile.close()
		except:pass
				
	# Обновление моба. (всё его поведение)
	def update(self, mobs, blocks, player, camfunced, SIZE, selectid, click, inv, dw_tory_select):
		camfunced1 = (camfunced[0]-1*bs, camfunced[1]-1*bs)
		from SbDev import Collide, Delay

		dist_to_player = int(dist(player.x, self.x, player.y, self.y))
		if self.player_damage_timer == 0:
			self.damage_player(player, camfunced, self.data["damage"], dist_to_player)
			self.player_damage_timer = self.data["player_damage_delay"]
		else:
			self.player_damage_timer -= 1

		if (camfunced[0] < -self.data["sise"][0] or camfunced[0] > SIZE[0]
		or  camfunced[1] < -self.data["sise"][1] or camfunced[1] > SIZE[1]):
			self.save()
			self.end(mobs)
		if self.hp <= 0:
			self.end(mobs)

		# падающий блок
		if self.data["type"] == "block":
			coordsdata = str(int(self.x/bs))+"_"+str(int(self.y/bs)+1)
			coordsdata2 = str(int(self.x/bs))+"_"+str(int(self.y/bs))
			try:
				bbl = blocks[coordsdata]
				bbl2 = blocks[coordsdata2]
				collide_m = False
				for mob in mobs:
					if mob.data["type"] == "block":
						if self.y + self.data["sise"][1] > mob.y:
							if self.y + self.data["sise"][1] < mob.y + mob.data["sise"][1]:
								collide_m = True
								break
				if not collide_m:
					self.y += self.yvel
					self.yvel += 0.055
				if bbl.id != 0 and bbl.id != 11:
					if self.y + self.data["sise"][1] >= bbl.y:
						bbl2.reset_block(self.data["set_block"])
						self.end(mobs)
			except KeyError:
#				print (self.x)//bs, (self.y)//bs,
#				print blocks.keys()[0]
				pass

		# Агрессивный моб
		if self.data["type"] == "agres":
			mpos = mouse.get_pos()
			try:
				rd_block = blocks[str(int((self.x+10)/bs)+1)+"_"+str(int((self.y+10)/bs)+1)]
				ld_block = blocks[str(int((self.x-bs*0.8)/bs))+"_"+str(int((self.y+10)/bs)+1)]
				if rd_block.id == 11:
					self.xvel = 0
				if ld_block.id == 11:
					self.xvel = 0
			except KeyError:
				pass
			self.timer.update()
			self.rightanim.update(self.dt)
			self.leftanim.update(self.dt)
			if self.damage_timer >= 1:
				self.damage_timer = int(self.damage_timer)-1



			# Выбор спрайта для отрисовки моба
			def draw_sp_r(self):
				self.image = self.rightanim.get_sprite()
			def draw_sp_l(self):
				self.image = self.leftanim.get_sprite()

			self.mob_move(player, dist_to_player)
			if self.right:
				draw_sp_r(self)
			else:
				draw_sp_l(self)

			if click and self.damage_timer == 0:
				if dist_to_player <= 4*bs:
					if mpos[0] > camfunced1[0] and mpos[0] < camfunced1[0]+self.data["sise"][0]   and   mpos[1] > camfunced1[1] and mpos[1] < camfunced1[1]+self.data["sise"][1]:
						if selectid in ItemTypes:
							itm = ItemTypes[selectid]
						else:
							itm = EMPTY_ITEM
						self.damage(itm.damage)
						selslot = inv.slots[dw_tory_select]
						if selslot.data.tool and not selslot.data.eat:
							selslot.NBTData += -1
						if self.x > player.x:
							self.xvel = 2.0
						else:
							self.xvel = -2.0

			try:
				Collide(self, mobs, blocks)
					
			except KeyError:
				pass

			if self.damage_timer != 0:
				self.image = self.damage_texture

		# Предмет.
		if self.data["type"] == "item":
			try:
				down_block = blocks[str(int((self.x+10)/bs)) +"_"+ str(int((self.y+bs*0.5)/bs))]
				up_block = blocks[str(int((self.x+10)/bs)) +"_"+ str(int((self.y-10)/bs))]

				left_block = blocks[str(int((self.x-self.data['sise'][0]+2)/bs)) +"_"+ str(int((self.y)/bs))]
				right_block = blocks[str(int((self.x+self.data['sise'][0]+2)/bs)) +"_"+ str(int((self.y)/bs))]

				head_block = blocks[str(int((self.x)/bs)) +"_"+ str(int((self.y+self.data["sise"][0]/2.0)/bs))]
				if down_block.data.collable and int(self.y+self.data['sise'][1]+2) > down_block.y:
					self.y = down_block.y-self.data["sise"][1]
					self.xvel = self.xvel*0.9
				else:
					self.yvel += 0.3


				if up_block.data.collable and not head_block.data.collable and self.y < up_block.y+bs:
					self.y = up_block.y+bs+10
					self.yvel = 0.0

				if left_block.data.collable and self.x < left_block.x+bs:
					self.x = left_block.x+bs-10
					self.xvel = 2.0

				if right_block.data.collable and self.x+self.data["sise"][0] > right_block.x:
					self.x = right_block.x-self.data['sise'][0]-11
					self.xvel = -2.0

#				if head_block.data.collable:
#					self.x = float(self.x)*0.95+float(player.x)*0.05
#					self.y = float(self.y)*0.95+float(player.y)*0.05

				if dist(self.x, player.x+15, self.y, player.y+70) <= bs:
					resss = inv.add(self.id, self.count, self.NBTData)
					if resss <= 0:
						self.end(mobs)
						self.count = 0
						return None
					else:
						self.count = resss
				if self.count <= 0:
					try:self.end(mobs)
					except:return None

				if down_block.id == 11:
					self.yvel += -0.4
				self.x += int(self.xvel*sz)
				self.y += int(self.yvel*sz)

				if self.yvel > 4.0*sz:
					self.yvel = 4.0*sz

				self.xvel = self.xvel*0.99
			except KeyError:
				pass
		# Добавление времени к таймеру спрайтов
		self.dt = self.clock.tick(60)


	def __str__(self):
		return "SbMob %s x.%s y.%s" % (self.data["name"], self.x, self.y)

	def __repr__(self):
		return self.__str__()
			
	def end(self, mobs):
		mobs.remove(self)
