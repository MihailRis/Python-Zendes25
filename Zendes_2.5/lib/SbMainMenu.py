#-*- coding: utf-8 -*-
import sys
import os
import pygame
import random
import time
import collections
import webbrowser

from SbInterface import *
from SbDev import sb_output
import SbLanguage
from SbConstants import *

#CONSTAINS:
#colors:
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
BLUELIGHT = (100,200,255)







path = sys.path[0][:-4]
_sh_format = 'png'
selected_lang = "english.dat"

def version_convert(version):
	version = int(version)
	v1 = int(version/100)
	v2 = int(version/10)-v1*10
	v3 = str(version)[-1]
	return "%s.%s.%s" % (v1,v2,v3)

if os.path.isdir("%s/settings/" % path):
	if os.path.isfile("%s/settings/language.dat" % path):
		with open("%s/settings/language.dat" % path, 'r') as langSettFile1:
			langSettFile = langSettFile1.readline()
			if langSettFile.endswith("\n"):
				langSettFile = langSettFile[:-1]
			selected_lang = langSettFile
	else:
		lfile = open("%s/settings/language.dat" % path, 'w')
		lfile.write(selected_lang)
		lfile.close()
else:
	os.mkdir("%s/settings/" % path)
rls = open("%s/resources/languages/%s" % (path, selected_lang), 'r')
langdata = rls.readlines()
rls.close()
LANGUAGE = SbLanguage.load(langdata)

del rls
del langdata

class MMenu():
	def __init__(self, SIZE, version, versize):
		self.face = pygame.Surface(SIZE)
		self.SIZE = SIZE
		self.version = version
		self.versize = versize

	def start(self, mode="menu"):
		wname = "new_world"

		versize = self.versize
		seed = random.randint(1000000000, 9999999999)
		window = pygame.display.get_surface()
		done = True
		bg = pygame.transform.scale(pygame.image.load(path+"/resources/textures/qui/background.png"), (SIZE[0]-2*bs, SIZE[1]-2*bs))
		bg.convert()
		pygame.font.init()
		splash = pygame.font.Font(path+"/resources/%s.ttf" % FONTNAME, 22)

		worlds = pygame.Surface((resz(500),resz(500)))
		worlds.set_alpha(100)

		langs = pygame.Surface((resz(500),resz(500)))
		langs.set_alpha(100)

		widgets_0 = []
		widgets_1 = []
		widgets_2 = []
		widgets_3 = []

		if mode == "menu":
			butt0_1 = Button(("start_menu", resz(32), 80, 0), (resz(520),reszy(250)), (resz(300),reszy(30)), "start")
			butt0_2 = Button(("quit_the_game", resz(32), 80, 0), (resz(520),reszy(400)), (resz(300),reszy(30)), "_exit_")
		elif mode == "pause":
			butt0_1 = Button(("continue", resz(32), 80, 0), (resz(520),reszy(250)), (resz(300),reszy(30)), "continue")
			butt0_2 = Button(("save_and_quit_to_menu", resz(32), 10, 0), (resz(470),reszy(400)), (resz(400),reszy(30)), "save_and_quit_to_menu")

		butt0_3 = Button(("settings", resz(32), 80, 0), (resz(520),reszy(300)), (resz(300),reszy(30)), "settings")
		butt0_4 = Button(("about", resz(32), 80, 0), (resz(520),reszy(350)), (resz(300),reszy(30)), "about")

		widgets_0.append(butt0_1)
		widgets_0.append(butt0_2)
		widgets_0.append(butt0_3)
		widgets_0.append(butt0_4)

		butt1_1 = Button(("load_world", resz(32), 80, 0), (resz(700),reszy(180)), (resz(300),reszy(30)), "load_game")
		butt1_1.freeze = True
		butt1_2 = Button(("back_to_menu", resz(32), 80, 0), (resz(700),reszy(150)), (resz(300),reszy(30)), "back_to_menu")
		butt1_3 = Button(("new_world", resz(32), 80, 0), (resz(880),reszy(260)), (resz(300),reszy(30)), "new_game")
		wrt_str1 = WriteString("world_name", resz(25), (resz(610),reszy(400)), resz(400), "world_name")
		wrt_str2 = WriteString("world_seed", resz(25), (resz(610),reszy(450)), resz(400), "seed", mode="INT")

		butt3_2 = Button(("game_site", resz(32), 80, 0), (resz(700),reszy(200)), (resz(300),reszy(30)), "game_site")

		font_1_1 = pygame.font.Font(path+"/resources/%s.ttf" % FONTNAME, resz(13))
		standartFont = pygame.font.Font(path+"/resources/%s.ttf" % FONTNAME, resz(20))
		standartFontSmall = pygame.font.Font(path+"/resources/%s.ttf" % FONTNAME, resz(15))

		versiontext = standartFont.render(str(self.version), 1, (WHITE))
		versiontext0 = standartFont.render(str(self.version), 1, (BLACK))
		versiontext1 = standartFontSmall.render("python 2.7.9        game written by Mihail_Ris", 1, (BLACK))
		versiontext2 = standartFontSmall.render("python 2.7.9        game written by Mihail_Ris", 1, (YELLOW))

		widgets_1.append(butt1_1)
		widgets_1.append(butt1_2)
		widgets_1.append(butt1_3)
		widgets_1.append(wrt_str1)
		widgets_1.append(wrt_str2)

		widgets_3.append(butt1_2)
		widgets_3.append(butt3_2)

		widgets_2.append(butt1_2)
		w_textes = []
		l_textes = []
		menu = 0

		widgets = widgets_0 + widgets_1 + widgets_2 + widgets_3
		wss1 = os.listdir("%s/worlds" % path)
		wss = {}
		for ws in wss1:
			if os.path.isfile("%s/worlds/%s/last_open.dat" % (path, ws)):
				date = open("%s/worlds/%s/last_open.dat" % (path, ws)).read().split("\n")[0]
				wss[date] = ws
			else:
				wss[0] = ws

		dss = list(wss)
		dss.sort()
		dss = dss[::-1]


		credits_list = (
		u"$!Главный разработчик:",
		u"Михаил Багазов",
		u" ",
		u"$!Программирование:",
		u"Михаил Багазов",
		u"Денис Неделяев",
		u"Даниил Яранцев",
		u" ",
		u"$!Перевод:",
		u"Александр Слюсарь",
		u" ",
		u"$!Идеи и поддержка",
		u"Дмитрий Рыков",
		u"Сева Винников",
		u"Дмитрий Седиков",
		u"Данил Андрюшин",
		u"Эдуард Рачковский",
		u"Роман Софронов",
		u"Максим Капелянович",
		u"Tverdokhleb Igor",
		u"Тимофей Багазов",
		u"Антония Коробейникова",
		u" ",
		u"$!И все участники", 
		u"$!группы игры. https://vk.com/zendes25/",
		)

		wow_size = (resz(350),reszy(700))
		credits = Surface(wow_size, pygame.SRCALPHA)
		stf = pygame.font.Font(path+"/resources/%s.ttf" % FONTNAME, resz(15))
		y = 0
		for line in credits_list:
			color = (50,50,50)
			if "$" in line:
				color = (0,0,0)
			lname = stf.render(line.split("!")[-1], 1, color)
			lsize = lname.get_size()
			x = wow_size[0]//2-lsize[0]//2

			credits.blit(lname, (x,y))

			y += 22
			
			

		indx = 0
		for world_saved in wss:
			world_saved = wss[dss[indx]]
			try:
				fff = open("%s/worlds/%s/version.dat" % (path, world_saved))
				vvv = int(fff.read().split("\n")[0])
				fff.close()
				vvv = str(vvv)
			except ValueError:
				vvv = "0"
			except IOError:
				vvv = "0"
			wtext = pygame.font.Font(path+"/resources/%s.ttf" % FONTNAME, resz(13))
			if int(vvv) == versize:
				tcolor = (255,255,255)
			elif int(vvv) > versize:
				tcolor = (255,120,100)
			elif int(vvv) < versize:
				tcolor = (255,200,100)
			
			wtext_1 = wtext.render(str(world_saved).decode("UTF-8")+u" "*(80-len(str(world_saved).decode("UTF-8"))-len(vvv)-len(" version: "))+u" version: %s" % \
			 (version_convert(vvv)), 1, tcolor)
			w_textes.append((wtext_1, world_saved))
			indx+=1

		for languag in os.listdir("%s/resources/languages" % path):
			language_pack = SbLanguage.load(open("%s/resources/languages/%s" % (path, languag), 'r').readlines())
			ltext = pygame.font.Font(path+"/resources/%s.ttf" % FONTNAME, resz(13))
			ltext_1 = ltext.render(language_pack["info_text"].decode("UTF-8"), 1, (255,255,255))
			l_textes.append((ltext_1, language_pack, languag))



		try:
			splashes = open("%s/resources/text/splashes.txt" % path, 'r').readlines()
			splash_text = splashes[random.randint(0, len(splashes)-1)][:-1].decode('UTF-8')
		except KeyError:
			splash_text = "no splashes :("

		worldsy = -1000
		langsy = -1000
		selected = None
		selected_lang = None

		splr = splash.render(splash_text, 0, (255,255,0))
		clock = pygame.time.Clock()




		surrf = pygame.Surface((resz(500),reszy(20)))
		surrf.fill((100,100,0))
		surrf3 = pygame.Surface((resz(500),reszy(20)))
		surrf3.fill((0,100,0))

		surrf = pygame.Surface((resz(500),reszy(20)))
		surrf.fill((100,100,0))
		surrf2 = pygame.Surface((resz(500),reszy(20)))
		surrf2.fill((0,100,0))
		last_menu = 0
		while done:
			click = False
			mpos = pygame.mouse.get_pos()
			events = pygame.event.get()
			for e in events:
				if e.type == pygame.QUIT:
					done = False
					pygame.quit()
					quit()
				if e.type == pygame.MOUSEBUTTONDOWN:
					if e.button == 1:
						click = True
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_F5:
						sh_numb = 0
						while True:
							sh_numb += 1
							if not os.path.isfile(path+"/screenshots/screenshot_%s.%s" % (sh_numb, _sh_format)):
								break		
						pygame.image.save(window, path+"/screenshots/screenshot_%s.%s" % (sh_numb, _sh_format))

			window.blit(bg, (0,0))
			window.blit(versiontext0, (resz(352), reszy(102)))
			window.blit(versiontext, (resz(350), reszy(100)))
			window.blit(versiontext1, (resz(2), self.SIZE[1]-reszy(20)))
			window.blit(splr, (self.SIZE[0]/2-splr.get_size()[0]/2, reszy(100)))
			for w4 in widgets:
				if w4.type == "BT":
					w4.string = LANGUAGE[w4.language_key].decode("utf-8")
				if w4.type == "WS":
					w4.pretext = LANGUAGE[w4.language_key].decode("utf-8")



			if menu == 0:
				for widget in widgets_0:
					widget.update(click, events)
					window.blit(widget.image, widget.side)
					if widget.func:
						if widget.funcTxt == "start":
							menu = 1
						if widget.funcTxt == "continue":
							return None
						if widget.funcTxt == "save_and_quit_to_menu":
							return "menu"
						if widget.funcTxt == "settings":
							menu = 2
						if widget.funcTxt == "about":
							menu = 3
						widget.func = False
			if menu == 1:
				if wrt_str1.string == "":
					wname = "World_%s" % str(time.time()).replace(".", "_")
				else:
					wname = wrt_str1.string
				#__________________
				for widget1 in widgets_1:
					widget1.update(click, events)
					window.blit(widget1.image, widget1.side)
					if widget1.func:
						if widget1.funcTxt == "back_to_menu":
							menu = 0
						if widget1.funcTxt == "load_game":
							if selected != None:
								wname = selected
								sb_output(path, "loading world %s" % wname)
								return wname

							
						if widget1.funcTxt == "seed":
							try:
								seed = int(widget1.string)
							except ValueError:
								seed = random.randint(1000000000, 9999999999)

						if widget1.funcTxt == "new_game":
							if not os.path.isdir("%s/worlds/%s" % (path, wname)):
								os.mkdir("%s/worlds/%s" % (path, wname))
							with open("%s/worlds/%s/seed.txt" % (path, wname), 'w') as seedfile:
								seedfile.write(str(seed))
							return wname
							sb_output(path, "creating world %s with ganeration key %s" % (wname, seed))
							done = False
							break

					widget1.func = False

				#___________________
				worlds.fill((0,0,0))
				y = reszy(10)

				worlds.blit(surrf2, (0, worldsy))
				for w in w_textes:
					if mpos[0] > resz(110) and mpos[0] < resz(600) and mpos[1] > resz(150)+y and mpos[1] < resz(150)+y+resz(20):
						worlds.blit(surrf, (0,y))
						if click:
							worldsy = y
							selected = w[1]
							butt1_1.freeze = False
					worlds.blit(w[0], (10, y))
					y += reszy(20)


				window.blit(worlds, (resz(100),reszy(150)))
				rendered1 = font_1_1.render(LANGUAGE["world_spoiler_text"].decode("utf-8").replace("%s1", wname).replace("%s2", str(seed)), 1, (255,255,200))
				window.blit(rendered1, (resz(700),reszy(300)))

			if menu == 2:
				for widget2 in widgets_2:
					widget2.update(click, events)
					window.blit(widget2.image, widget2.side)
					if widget2.func:
						if widget2.funcTxt == "back_to_menu":
							menu = 0
						if widget2.funcTxt == "settings":
							menu = 2
						widget2.func = False

				langs.fill((0,0,0))
				y1 = reszy(10)

				langs.blit(surrf3, (0, langsy))
				for lang2 in l_textes:
					if mpos[0] > 110 and mpos[0] < 600 and mpos[1] > 150+y1 and mpos[1] < 150+y1+20:
						langs.blit(surrf, (0,reszy(y1)))
						if click:
							langsy = y1
							selected_lang = lang2[2]
							global LANGUAGE
							LANGUAGE = lang2[1]
							with open("%s/settings/language.dat" % path, 'w') as ffilef:
								ffilef.write(selected_lang)
						
					langs.blit(lang2[0], (10, y1))
					y1 += reszy(20)

				window.blit(langs, (resz(100),reszy(150)))

			if menu == 3:
				for widget3 in widgets_3:
					widget3.update(click, events)
					window.blit(widget3.image, widget3.side)
					if widget3.func:
						if widget3.funcTxt == "back_to_menu":
							menu = 0
						if widget3.funcTxt == "game_site":
							webbrowser.open("https://vk.com/zendes25",0,True)
						widget3.func = False
				window.blit(credits, (resz(200),reszy(150)))
			pygame.display.flip()
#			clock.tick(1000)
#			print clock.get_fps()

