# -*- coding: utf-8 -*-

#######################
#THE 2D SANDBOX GAME
#CREATED BY MIHAIL RIS 
#https://vk.com/zendes25
#######################
#   /\__/\	zendes 2.5
#  | ^ ^ \	started in 18th May of 2016 year
#  \  -  \	powered by python 2.7.9, python library: pygame
###########################################################
import time
import pygame
import os
import sys
import random
from time import sleep

#CONSTAINS:

GamePath = sys.path[0]
LibPath = GamePath+"/lib"
OutPutPath = GamePath+"/output"
sys.path.insert(0, LibPath)

WorldName = "Zendes25"


if not os.path.isdir(GamePath+"/screenshots"):
	os.mkdir(GamePath+"/screenshots")
if not os.path.isdir(GamePath+"/worlds"):
	os.mkdir(GamePath+"/worlds")


print "loading libraries..."
lllt = time.time()
from SbDev import *
from SbTerrain import *
from SbGenerator import generation
from SbInterface import *
from SbPlayer import Player
from SbMenus import *
from SbMobs import *
from SbMainMenu import MMenu
from SbProfile import Profiler
from SbEffects import *

from SbConstants import *
print "libraries loaded in %s seconds" % (time.time()-lllt)


slot_get(Slot)

del lllt

pygame.mixer.init()

# Version data
versiondata = {"type": "beta", "num1": 1, "num2": 0, "num3": 3, "stade": "test"}
versize = versiondata["num3"]+versiondata["num2"]*10+versiondata["num1"]*100
version = "%s_%s.%s.%s %s" % (versiondata["type"], versiondata["num1"], versiondata["num2"], versiondata["num3"], versiondata["stade"])
#"alpha_0.6.1"


#SIZE = (33*32, 20*32)


def resize(size):
	global camera
	global screen, SIZE, window
	screen = pygame.Surface((size[0]-bs, size[1]-bs))
	window = pygame.display.set_mode((size[0]-2*bs, size[1]-2*bs), pygame.HWSURFACE|pygame.HWACCEL)
	SIZE = size
	try:
		clear()
		fill()
	except NameError:
		pass


#создаём окно
icon = pygame.image.load(GamePath+"/resources/textures/blocks/grass.png")
resize(SIZE)
pygame.display.set_caption("Zendes 2.5       "+version)
pygame.display.set_icon(icon)


#OUTPUT
sb_output(GamePath, "")
sb_output(GamePath, "starting game")
sb_output(GamePath, "starting main cycle")
timer = pygame.time.Clock()

pygame.font.init()
fps_font = pygame.font.Font(GamePath+"/resources/%s.ttf" % FONTNAME, 12)
pygame.mouse.set_visible(True)
visers_text = False



s_panel = State_Panel(GamePath)
MainMenu = MMenu((30*bs, 17*bs), version, versize)

# Спавн моба (pos - позиция моба, name - Имя моба (id), item - данные для моба предмета. (id, count, NBT(durability)))
def spawn_mob(pos, name, item=None):
	global GamePath, WorldName
	mob = Mob(name, GamePath, pos, WorldName, item)
	mobs.append(mob)

# Округление чисел. По-умолчанию размер блока.
def bround(value, toround=bs):
	return int(int(value/toround)*toround)



def clear():
	blocks_dict.clear()
	for block_03 in sprites:
		sprites.remove(block_03)

def drop_all(inv, player):

	for slot in inv.slots:
		force = random.uniform(-25.0*sz, 100.0*sz)
		yforce = -abs(force)
		if slot.id != 0:
			spawn_mob((player.x, player.y), "item", (slot.id, slot.count, slot.NBTData))
			mob = mobs[-1]
			mob.x += force
			mob.y += yforce

			mob.xvel = force*0.1
			mob.yvel = yforce*0.1

			slot.id = 0
			slot.count = 0
			slot.NBTData = 100



# Main
if True: # Ya razreshayu zapusk igri
	skybox = Surface(SIZE)
	sky_texture = pygame.transform.scale(pygame.image.load(GamePath+"/resources/textures/ambient/sky.png"), SIZE)
	skybox.blit(sky_texture, (0,0))
	selector = pygame.transform.scale(pygame.image.load("%s/resources/textures/qui/selector.png" % GamePath), (bs,bs))
	while True:
		if RELOAD_LIBS:
			from SbTerrain import *
			from SbGenerator import generation
			from SbInterface import *

		WorldName = MainMenu.start()
		tttm = time.time()
		inv = Inventory(GamePath, WorldName)
		dw_tory = DownTory(SIZE, GamePath, inv)
		block_inv = None
		with open("%s/worlds/%s/last_open.dat" % (GamePath, WorldName), 'w') as last_open_file:
			last_open_file.write(str(time.time()))
		play = True
		sprites = pygame.sprite.Group()
		try:
			with open("%s/worlds/%s/version.dat" % (GamePath, WorldName), 'r') as versfile:
				verss = int(versfile.read().split("\n")[0])
				versfile.close()
		except IOError:
			verss = versize

		if verss > versize:
			continue

		blocks_dict = {}

		mobs = []



		if isfile("%s/worlds/%s/seed.txt" % (GamePath, WorldName)):
			with open("%s/worlds/%s/seed.txt" % (GamePath, WorldName)) as seed_file:
				line = seed_file.readline()
				if line[-1] != "\n":
					seed = int(line)
				else:
					seed = int(line[0:-1])
		else:
			seed = random.randint(1000000000, 9999999999)

		if isfile("%s/worlds/%s/tig.dat" % (GamePath, WorldName)):
			with open("%s/worlds/%s/tig.dat" % (GamePath, WorldName)) as tig_file:
				line = tig_file.readline()
				if line[-1] != "\n":

					TIG = int(line)
				else:
					TIG = int(line[:-1])
		else:
			TIG = 0


		pygame.display.set_caption("Zendes 2.5       "+version+" "*10+"seed: %s" % seed)
		gen_type = "optim#normal"
		player = Player(0*bs,100*bs, GamePath, WorldName)

		def fill():
			x = bround(int((player.x)/bs)*bs-SIZE[0]/2)
			y = bround(int((player.y)/bs)*bs-SIZE[1]/2)

			for row in range(1, SIZE[0]/bs+1):
				for col in range(1, SIZE[1]/bs+1):
					try:
						blocks_dict[str(int(x/bs))+"_"+str(int(y/bs))]
					except KeyError:
						x,y = (bround(x), bround(y))
						bl = Block(GamePath, x, y, generation(seed, gen_type, x, y), WorldName, blocks=blocks_dict)
						sprites.add(bl)
						#print str(int(x/bs))+"_"+str(int(y/bs))
						blocks_dict[str(int(x/bs))+"_"+str(int(y/bs))] = bl
					y += bs
				x += bs
				y = 0
		fill()


#				print mobs

		def tp(pos):
			clear()
			player.x = pos[0]
			player.y = pos[1]
			fill()
			player.started = False

		def save_game():
			global play
			sb_output(GamePath, "\nSaving game:")
			sb_output(GamePath, "    saving player")
			player.save_data()
			sb_output(GamePath, "    saving mobs")
			for mob in mobs:
				mob.save()
			sb_output(GamePath, "    saving inventory")
			inv.save()
			sb_output(GamePath, "    saving generation key (seed)")
			with open("%s/worlds/%s/seed.txt" % (GamePath, WorldName), 'w') as seedfile:
				seedfile.write(str(seed))
			with open("%s/worlds/%s/version.dat" % (GamePath, WorldName), 'w') as versfile:
				versfile.write(str(versize))
			with open("%s/worlds/%s/tig.dat" % (GamePath, WorldName), 'w') as tigfile:
				tigfile.write(str(TIG))
			sb_output(GamePath, "game successfully saved")
			play = False

		def ZError(string):
			save_game()
			sys.stderr.write("Zendes25_Error: %s.\n" % string)
			sys.exit(1)



		selectid = 1
		click = False
		click2 = False
		#########################################
		game_speed = 60
		#########################################

#		pygame.mixer.music.play(-1)
		up = right = left = False
		camera = Camera(player)
		inv_visual = False

		mouse_up = mouse_down = False

		fly = False
		TMR = True


		shift = False
		print time.time()-tttm, 1101
		while play:
			try:
				PROFILE = Profiler()
				prof = False




				tbl = 0

				mouse_up = mouse_down = False
				mp = pygame.mouse.get_pos()
				block_sise = 0
				#ОБРАБОТКА СОБЫТИЙ
				for e in pygame.event.get():
					if e.type == pygame.QUIT:
						save_game()
						sb_output(GamePath, "quit the game")
						sys.exit()
					if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
						click = True
					if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
						click2 = True

					if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
						click = False
					if e.type == pygame.MOUSEBUTTONUP and e.button == 3:
						click2 = False

					if e.type == pygame.MOUSEBUTTONDOWN and e.button == 4:
						mouse_up = True
					if e.type == pygame.MOUSEBUTTONDOWN and e.button == 5:
						mouse_down = True

					if e.type == pygame.KEYDOWN:
						if e.key == pygame.K_F1:
							sb_output(GamePath, "OS: %s\nPython version: %s" % (sys.platform, sys.version))

						if e.key == pygame.K_F2:
							save_game()
							break

						if e.key == pygame.K_UP:
							up = True
						if e.key == pygame.K_RIGHT:
							right = True
						if e.key == pygame.K_LEFT:
							left = True
						if e.key == pygame.K_0:
							fly = True

						if e.key == pygame.K_p:
							prof = True

						if e.key == pygame.K_F4:
							visers_text = toogle(visers_text)

						if e.key == pygame.K_F5:
							sh_numb = 0
							while True:
								sh_numb += 1
								if not os.path.isfile(GamePath+"/screenshots/screenshot_%s.%s" % (sh_numb, sh_format)):
									break
							pygame.image.save(window, GamePath+"/screenshots/screenshot_%s.%s" % (sh_numb, sh_format))
						if e.key == pygame.K_TAB:
							if not block_inv is None:
								block_inv.save(GamePath, WorldName)
							block_inv = None
							inv_visual = toogle(inv_visual)
#						if e.key == pygame.K_t:
#							inv.add(12, 1, 100)
#							inv.add(-11, 1, 100)
#							inv.add(13, 10, 100)
#							inv.add(20, 1, 100)
#							inv.add(21, 1, 100)
#							inv.add(22, 1, 100)
#							inv.add(25, 1, 100)
#							inv.add(BLOCK_LEAD, 10, 100)
						if e.key == pygame.K_m:
							spawn_mob((player.x, player.y), "fleber")
						if e.key == pygame.K_i:
							spawn_mob((player.x, player.y), "item", item=(random.randint(1, 16), 1, 100))

						if e.key == pygame.K_F8:
							give_get = raw_input("enter >'id count': ")
							give_get = give_get.split()
							inv.add(int(give_get[0]), int(give_get[1]), 100)
						if e.key == pygame.K_q:
							slot = inv.slots[dw_tory.selected]
							if slot.count == 0:
								slot.id = 0
							if slot.count >= 1:
								if player.right:
									side_q = 55
								else:
									side_q = -25
								spawn_mob((player.x+side_q, player.y), "item", item=(slot.id, 1, slot.NBTData))

								slot.count += -1
								mobs[-1].yvel += -10
								if player.right:
									mobs[-1].xvel = 6
								else:
									mobs[-1].xvel = -6

							else:
								slot.id = 0
								slot.count = 0
								slot.NBTData = 100
						if e.key == pygame.K_LSHIFT:
							shift = True
						if e.key == pygame.K_ESCAPE:
							if inv_visual:
								inv_visual = False
								if not block_inv is None:
									block_inv.save(GamePath, WorldName)
							else:
								result_pause = MainMenu.start(mode="pause")
								if result_pause == "menu":
									save_game()
									break
					if e.type == pygame.KEYUP:
						if e.key == pygame.K_UP:
							up = False
						if e.key == pygame.K_RIGHT:
							right = False
						if e.key == pygame.K_LEFT:
							left = False
						if e.key == pygame.K_SPACE:
							fly = False
						if e.key == pygame.K_LSHIFT:
							shift = False

				PROFILE.add_point("events")

				screen.blit(skybox, (bs,bs))

				PROFILE.add_point("sky")

				#####SPRITES____________________

				for ee in sprites:
					for mobdata in ee.spawnmobs:
						spawn_mob(mobdata[0], mobdata[1], mobdata[-1])
						mob = mobs[-1]
						try:
							if not mobdata[2] is None:
								mob.hp = mobdata[2]
						except:
							pass
						mob.xvel = mobdata[3][0]
						mob.yvel = mobdata[3][1]
					ee.spawnmobs = []


					posi_block_in_screen = camera_func(camera, (ee.x, ee.y), SIZE)
					if ee.data.visible and player.started:
						screen.blit(ee.image, posi_block_in_screen)

					if not inv_visual:
						if not ee.id in (0,):
							BLresult = ee.update(mobs, blocks_dict, selectid, click2, inv, TIG, player)
							if type(BLresult) in (tuple, list):
								if BLresult[0] == "mob":
									if True:
										spawn_mob(BLresult[1], BLresult[2])
										mobs[-1].hp = BLresult[3]
					coords_data = str(ee.x/bs)+"_"+str(ee.y/bs)
					blocks_dict[coords_data] = ee
					#DELETE FOR LEFT SIDE IN SCREEN
					if posi_block_in_screen[0] < -bs:
						#Я понял
						sprites.remove(ee)
						try:
							blocks_dict[str(int((ee.x+SIZE[0])/bs))+"_"+str(int(ee.y/bs))]
						except KeyError:
							bl = Block(GamePath, bround(ee.x+SIZE[0]), bround(ee.y), generation(seed, gen_type, bround(ee.x+SIZE[0]+bs), bround(ee.y)), WorldName, mode="in_game", blocks=blocks_dict)
							sprites.add(bl)
							coords_data1 = str(bl.x/bs)+"_"+str(bl.y/bs)
							blocks_dict[coords_data1] = bl
						try:
							del blocks_dict[coords_data]
						except KeyError:
							pass


					#DELETE FOR RIGHT SIDE IN SCREEN
					if posi_block_in_screen[0] > SIZE[0]:
						sprites.remove(ee)
						try:
							blocks_dict[str(int((ee.x-SIZE[0])/bs))+"_"+str(int(ee.y/bs))]
						except KeyError:
							bl = Block(GamePath, bround(ee.x-SIZE[0]), bround(ee.y), generation(seed, gen_type, bround(ee.x-SIZE[0]), ee.y), WorldName, mode="in_game", blocks=blocks_dict)
							sprites.add(bl)
							coords_data1 = str(bround(bl.x))+"_"+str(bround(bl.y))
							blocks_dict[coords_data1] = bl
						try:
							del blocks_dict[coords_data]
						except KeyError:
							pass

					#DELETE FOR UP SIDE IN SCREEN
					if posi_block_in_screen[1] < -bs:
						sprites.remove(ee)
						try:
							blocks_dict[str(int(ee.x/bs))+"_"+str(int((ee.y+SIZE[1])/bs))]
						except KeyError:
							bl = Block(GamePath, bround(ee.x), bround(ee.y+SIZE[1]), generation(seed, gen_type, ee.x, bround(ee.y+SIZE[1])), WorldName, mode="in_game", blocks=blocks_dict)
							sprites.add(bl)
							coords_data1 = str(bround(bl.x))+"_"+str(bround(bl.y))
							blocks_dict[coords_data1] = bl
						try:
							del blocks_dict[coords_data]
						except KeyError:
							pass

					#DELETE FOR DOWN SIDE IN SCREEN
					if posi_block_in_screen[1] > SIZE[1]:
						sprites.remove(ee)
						try:
							blocks_dict[str(int(ee.x/bs))+"_"+str(int((ee.y-SIZE[1])/bs))]
						except KeyError:
							bl = Block(GamePath, bround(ee.x), bround(ee.y-SIZE[1]), generation(seed, gen_type, ee.x, bround(ee.y-SIZE[1])), WorldName, mode="in_game", blocks=blocks_dict)
							sprites.add(bl)
							coords_data1 = str(bround(bl.x))+"_"+str(bround(bl.y))
							blocks_dict[coords_data1] = bl
						try:
							del blocks_dict[coords_data]
						except KeyError:
							pass




					if visers_text:
						#block_sise += (sys.getsizeof(ee))
						if not ee.id == 0:
								tbl += 1
				PROFILE.add_point("blocks")
				for mob in mobs:
					cf = camera_func(camera, (mob.x, mob.y), SIZE)
					mob.update(mobs, blocks_dict, player, cf, SIZE, selectid, click, inv, dw_tory.selected)
					screen.blit(mob.image, cf)

				if click2:
					try:
						if selectid < 0:
							mpos = pygame.mouse.get_pos()
							cmpos = unc_func(camera)
							bmp = blocks_dict[cmpos]
							useitem(selectid, player, blocks_dict, inv.slots[dw_tory.selected], inv, bmp)
					except KeyError:
						pass
				try:
					if not inv_visual:
						eee = blocks_dict[unc_func(camera)]
						if click == True:
							eeeid = eee.id
							reided = eee.reid()
							if reided:
								if BlockTypes[eeeid].inv:
									if eee.inventory_string != "E":
										inv_string = eee.inventory_string.split("I")[-1].split("$")
										for slot in inv_string:
											sldata = slot.split("!")
											spawn_mob((eee.x, eee.y), "item", item=(int(sldata[0]),int(sldata[1]),int(sldata[2])))
										eee.inventory_string = "E"
								if inv.slots[dw_tory.selected].data.tool and eeeid != 0:
									selslot = inv.slots[dw_tory.selected]
									selslot.NBTData = int(selslot.NBTData)
									if selslot.data.material == BlockTypes[eeeid].material:
										selslot.NBTData += -1
									else:
										selslot.NBTData += -2
									if inv.slots[dw_tory.selected].NBTData <= 0:
										inv.slots[dw_tory.selected].id = 0
										inv.slots[dw_tory.selected].count = 0
						if click2 == True:
							eeue = eee.id
							lock = False
							if selectid:
								for mob in mobs:
									mpos = unc2_func(camera)
									cpos = (mob.x, mob.y)
									ccpos = camera_func(camera, cpos, SIZE)
									if mob.data["name"] == "sand":
										eev = int(mpos[0]/bs) == int((ccpos[0]+1)/bs) and int(mpos[1]/bs/2) == int(((ccpos[1]+1)/bs)/2)
									else:
										eev = mpos[0] > cpos[0] and mpos[0] < cpos[0]+mob.data["sise"][0]  and  mpos[1] > cpos[1] and mpos[1] < cpos[1]+mob.data["sise"][1]

									if eev:
										lock = True
								if not lock and eee.data.replacement:
									if selectid != 0:
										if selectid > 0:
											new_id = selectid
										else:
											new_id  = ItemTypes[selectid].set_block
										if new_id != 0:
											if new_id < 0:
												ZError("attribute set_block with value=%s in ItemType object with id=%s not is block" % (new_id, selectid))
											rest = eee.reset_block(new_id)
											if rest is None:
												if BlockTypes[eeue].replacement:
													if inv.slots[dw_tory.selected].count <= 1:
														inv.slots[dw_tory.selected].id = 0
														selectid = 0
														inv.slots[dw_tory.selected].id = 0
														inv.slots[dw_tory.selected].count = 0

													else:
														inv.slots[dw_tory.selected].count += -1
							if eee.data.inv:
								block_inv = BlockInv(eee, eee.data.inv)
								inv_visual = True

							if eee.id == 12:
								if selectid == -15:
									explode(eee.x, eee.y, blocks_dict, mobs, player)
								
						else:
							if eee.start_clicked == 1:
								eee.start_clicked = 2
										
				except KeyError:
					pass

				PROFILE.add_point("clicks")



				if inv_visual:
					player.update(GamePath, blocks_dict, False, False, False, fly)
				else:
					player.update(GamePath, blocks_dict, up, left, right, fly)
				if player.hp <= 0:
					player.hp = 20
					player.hunger = 20
					player.xvel = 0
					player.yvel = 0
					
					drop_all(inv, player)

					tp(player.spawnpoint)

				player_pos_in_screen = camera_func(camera, player.get_pos(), SIZE)
				screen.blit(player.image, player_pos_in_screen)

				# отображение экрана

				PROFILE.add_point("not_inv")


				if player.started:
					unc1 = unc2_func(camera)
					unced = camera_func(camera, (int(unc1[0]/bs)*bs, int(unc1[1]/bs)*bs), SIZE)
					screen.blit(selector, unced)

				dw_tory.update(mouse_up, mouse_down)
				window.blit(screen, (-bs, -bs))
				second_slots = None
				if not block_inv is None:
					second_slots = block_inv.slots
				if inv_visual:
					inv.update(click,click2, shift, second_slots)
					window.blit(inv.image, inv.pos)
					if not block_inv is None:
						block_inv.update(click,click2, shift, inv.slots)
						window.blit(block_inv.image, block_inv.pos)
					window.blit(inv.cursor_image, mp)
				else:
					s_panel.update(player)
					window.blit(s_panel.image, (SIZE[0]-s_panel.sise[0], 0))
				window.blit(dw_tory.image, dw_tory.side)
				selectid = dw_tory.get()

				PROFILE.add_point("inv")



				if visers_text:
					window.blit(fps_font.render(u"Fps:" + str(int(timer.get_fps()))+u"      Выбранный id: "+str(selectid)+u"   Видимых блоков: "+str(tbl)\
					+u"   x=%s y=%s" % (int(player.x/bs), int(player.y/bs)), 1, (250,250,220)), (0, 0))
				else:
					window.blit(fps_font.render(u"Fps:" + str(int(timer.get_fps()))+u"      v. %s" % version, 0, (250,250,220)), (0, 0))
				#обновление окна

				PROFILE.add_point("text")

				PROFILE.add_line("start", "events")
				PROFILE.add_line("events", "sky")
				PROFILE.add_line("sky", "blocks")
				PROFILE.add_line("blocks", "clicks")
				PROFILE.add_line("clicks", "not_inv")
				PROFILE.add_line("not_inv", "inv")
				PROFILE.add_line("inv", "text")

				PROFILE.add_point("pre_display")




				timer.tick(game_speed)
				pygame.display.flip()


				PROFILE.end()
				PROFILE.add_line("pre_display", "end")
				if prof:
					PROFILE.get()

				TIG += timer.get_time()/10
			except:
				save_game()
				raise
