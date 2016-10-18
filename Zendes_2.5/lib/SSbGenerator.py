# -*- coding: utf-8 -*-
#WORLD GENERATION

# seeds 707
import noise
from SbDev import sb_output
from SbDev import divis_get
#import SbRandom as random
import random
#import math

bs = 45
bsInv = 1.0/float(bs)
wdm = 45*bs*0
wum = 30*bs*0

gs = 15*bs #GenerationSise
ogs = int(gs*bsInv) #GenerationSise in blocks

PlainsB = (235*bs+wdm, 230*bs+wum, 3, 50, 100) # world_down, world_up, up_blocks, Trees, chance
DesertB = (225*bs+wdm, 220*bs+wum, 5, 0, 60)
MountainsB = (210*bs+wdm, 200*bs+wum, 1, 90, 70)
ForestB = (250*bs+wdm, 230*bs+wum, 3, 4, 100)
SeaB = (268*bs+wdm, 264*bs+wum, 5, 0, 50)

BIOMS0 = [PlainsB, DesertB, MountainsB, ForestB, SeaB]
BIOMS = []

for BIOM in BIOMS0:
	maked = 0
	to_make = BIOM[4]
	while maked < to_make:
		maked += 1
		BIOMS.append(BIOM)



def FuncLine(left, right, point, lsise, rsise):
	allsise = right-left+1

	rperc = float(right-point)/allsise
	lperc = float(point-left)/allsise

	return lsise*rperc+rsise*lperc





def generation(seed, mode, x, y, flatdata=10):
	if mode == "flat":
		if y*bsInv - 6 >= flatdata:
			a = random.randint(0,1000)
			z = False
			if a < 35 and a > 20:
				return 4
				z = True
			if not z and a < 20 and a > 10 and y*bsInv > flatdata+10:
				return 9
				z = True
			if not z:
				return 1
		if y*bsInv - 2 >= flatdata:
			return 2
		if y*bsInv - 1 >= flatdata:
			return 3
		if y*bsInv - 4 < flatdata:
			return 0
	if mode == "empty":
		return 0

	if mode == "interstellar":
		r = seed*x*y
		if divis_get(r, 2):
			return(0)
		else:
			return(1)

	if mode == "normal":

		left_point = int(x*lh_DIVggs)*gs
		random.seed(seed)
		random.seed(int((left_point*100.0)*bsInv*lh_DIVggs/random.randint(4, 30)))
		left_biom = BIOMS[random.randint(0, len(BIOMS)-1)]

		right_point = (int(x*lh_DIVggs)*gs)+gs
		random.seed(seed)
		random.seed(int((right_point*100.0)*bsInv*lh_DIVggs/random.randint(4, 30)))
		right_biom = BIOMS[random.randint(0, len(BIOMS)-1)]

		if int(left_point*bsInv*bsInv) == 0:
			left_biom = PlainsB

		if int(right_point*bsInv*bsInv) == 0:
			right_biom = PlainsB

		#определение высот 2-х основных точек, левой и правой
		random.seed(seed*left_point*gs)
		left_point_H = int(random.randint(left_biom[1], left_biom[0])*bsInv)*bs
		random.seed(seed*right_point*gs)
		right_point_H = int(random.randint(right_biom[1], right_biom[0])*bsInv)*bs
		biom = PlainsB
		#если блок совподает с левой точкой
		if int(left_point*bsInv)*bs == int(x*bsInv)*bs:
			point_hight = left_point_H
			biom = left_biom
		#если блок совподает с правой точкой
		if int(right_point*bsInv)*bs == int(x*bsInv)*bs:
			point_hight = right_point_H
			biom = right_biom
		left_percent = float(float(x-left_point)*lh_DIVggs)
		right_percent = float(float(right_point-x)*lh_DIVggs)
		try:
			point_hight
		except NameError:
			rsn = 0
			point_hight = (left_point_H*right_percent)+(right_point_H*left_percent)

			random.seed(seed+x+y+point_hight)
			if random.randint(-(int(left_point_H*left_percent*100)), int(right_point_H*right_percent*100)) >= 0:
				biom = left_biom
			else:
				biom = right_biom

		if y > point_hight:
			if int(y*bsInv) == int(point_hight*bsInv):
				return 6
			if y - 6*bs <= point_hight:
				return biom[2]
			else:
				random.seed(seed+x+y+seed-point_hight+biom[0]-biom[1]*x*y*x**2)
				rand = random.randint(0,20000)
				to_id = 1
				if rand < 250:
					to_id = 4
				if rand < 40 and point_hight+(20*bs) < y:
					to_id = 9
				if rand < 5 and point_hight+(100*bs) < y:
					to_id = 6
				return to_id
		else:
			random.seed(seed+x)
			if biom[3] != 0:
				done_1 = False
				if random.randint(0, biom[3]) == 0:
					if int(y*bsInv) == int(point_hight*bsInv):
						return 7
						done_1 = True
					if int(y*bsInv)+1 == int(point_hight*bsInv):
						return 7
						done_1 = True
					if int(y*bsInv)+2 == int(point_hight*bsInv):
						return 7
						done_1 = True
					if int(y*bsInv)+3 == int(point_hight*bsInv):
						return 7
						done_1 = True
					if int(y*bsInv)+4 == int(point_hight*bsInv):
						return 7
						done_1 = True
					if int(y*bsInv)+5 == int(point_hight*bsInv):
						return 8
					if int(y*bsInv)+6 == int(point_hight*bsInv):
						return 8
						done_1 = True

				random.seed(seed+x+bs)
				if not done_1 and random.randint(0, biom[3]) == 0:
					if int(y*bsInv)+1 == int(point_hight*bsInv):
						return 8
						done_1 = True
					if int(y*bsInv)+2 == int(point_hight*bsInv):
						return 8
						done_1 = True
					if int(y*bsInv)+3 == int(point_hight*bsInv):
						return 8
						done_1 = True
					if int(y*bsInv)+4 == int(point_hight*bsInv):
						return 8
						done_1 = True
				random.seed(seed+x-bs)
				if not done_1 and random.randint(0, biom[3]) == 0:
					if int(y*bsInv)+1 == int(point_hight*bsInv):
						return 8
						done_1 = True
					if int(y*bsInv)+2 == int(point_hight*bsInv):
						return 8
						done_1 = True
					if int(y*bsInv)+3 == int(point_hight*bsInv):
						return 8
						done_1 = True
					if int(y*bsInv)+4 == int(point_hight*bsInv):
						return 8
						done_1 = True
				random.seed(seed+x+bs*2)
				if not done_1 and random.randint(0, biom[3]) == 0:
					if int(y*bsInv)+2 == int(point_hight*bsInv):
						return 8
						done_1 = True
					if int(y*bsInv)+3 == int(point_hight*bsInv):
						return 8
						done_1 = True
					if int(y*bsInv)+4 == int(point_hight*bsInv):
						return 8
						done_1 = True
				random.seed(seed+x-bs*2)
				if not done_1 and random.randint(0, biom[3]) == 0:
					if int(y*bsInv)+2 == int(point_hight*bsInv):
						return 8
						done_1 = True
					if int(y*bsInv)+3 == int(point_hight*bsInv):
						return 8
						done_1 = True
					if int(y*bsInv)+4 == int(point_hight*bsInv):
						return 8
						done_1 = True

			if int(y*bsInv) >= 251:
				return 11
		return 0
#		x_left_rasn = float(ogs/(x-left_point+0.1))


	if mode == "islands#beta":
		ggss = 5
		if True:
			sis = noise.pnoise3(float(x*bsInv*0.1), float(y*bsInv*0.1), seed, 3)
			sis = float(float(sis)*100)

			if True:
				sss = 5
				if sis > sss:
					if sis > sss+3:
						if int(sis) == 39:
							if int(sis) > 40:
								return 11
							return 6
						return 1
					elif sis > sss+1:
						return 3
				else:
					sis2 = noise.pnoise3(float(x*bsInv*0.07), float(y*bsInv*0.07), seed, 1)
					sis2 = float(float(sis2)*100)
					if sis2 > 30 and sis > sss-10:
						if sis2 > 45:
							return 7
						return 8
					return 0
			return 0

	if mode == "new#normal#beta":
		global nbiom, bsInv
		nbiom1 = noise.pnoise2(x*0.00002, seed, 2)
		nbiom = int(abs(nbiom1*40))

		def get_biom():
			global nbiom, bsInv
			if int(y*bsInv) < 80+sis*0.3:
				if int(y*bsInv) < 110+sis*0.3:
					return 19

				if sis3 > 13 and int(y*bsInv) > sis+200:
					return 6
				if sis2 < -12:
					return 9
				if sis2 > 10:
					return 4
				return 1
			if nbiom == 0:
				return 5
			return 3

		seed = seed*0.0006567568

		sism = noise.pnoise2(float(x*bsInv*0.005), seed, 5)
		sism = float(float(sism)*120)+100

		sis2 = noise.pnoise3(float(x*bsInv*0.2), float(y*bsInv*0.2), seed, 1)
		sis2 = float(float(sis2*18))

		sis3 = noise.pnoise3(float(x*bsInv*0.1), float(y*bsInv*0.1), seed+1, 1)
		sis3 = float(float(sis3*19))

		sis = noise.pnoise2(float(x*bsInv*0.002), seed, 5)
		aaa = float(nbiom1)
		bbb = (float(float(sis)*600)+200)
		sis = ((bbb*0.5+((bbb)*(aaa+2))*0.9)*0.35)+20

		get_biom()

		ol = 270



		if int(y*bsInv) > sis:
			if int(y*bsInv) > sis+10:
				if sis3 > 13 and int(y*bsInv) > sis+250:
					return 6
				if sis2 < -12:
					return 9
				if sis2 > 10:
					return 4
				return 1
			if int(y*bsInv) >= ol-int(sis/29):
				return 5
			else:
				return get_biom()
		if int(y*bsInv) >= ol:
			return 11
		return 0

		


	if mode == "optim#normal":
		lh_DIVggs = 1.0/float(gs)
		

		left_point = int(x*lh_DIVggs)*gs
		random.seed(seed)
		random.seed(int((left_point*100.0)*bsInv*lh_DIVggs/random.randint(4, 30)))
		left_biom = BIOMS[random.randint(0, len(BIOMS)-1)]

		right_point = (int(x*lh_DIVggs)*gs)+gs
		random.seed(seed)
		random.seed(int((right_point*100.0)*bsInv*lh_DIVggs/random.randint(4, 30)))
		right_biom = BIOMS[random.randint(0, len(BIOMS)-1)]

		if int(left_point*bsInv*bsInv) == 0:
			left_biom = PlainsB

		if int(right_point*bsInv*bsInv) == 0:
			right_biom = PlainsB

		#определение высот 2-х основных точек, левой и правой
		random.seed(seed*left_point*gs)
		left_point_H = int(random.randint(left_biom[1], left_biom[0])*bsInv)*bs
		random.seed(seed*right_point*gs)
		right_point_H = int(random.randint(right_biom[1], right_biom[0])*bsInv)*bs
		biom = PlainsB

		#если блок совподает с левой точкой
		if int(left_point*bsInv)*bs == int(x*bsInv)*bs:
			point_hight = left_point_H
			biom = left_biom

		#если блок совподает с правой точкой
		if int(right_point*bsInv)*bs == int(x*bsInv)*bs:
			point_hight = right_point_H
			biom = right_biom
		left_percent = float(x-left_point)*lh_DIVggs
		right_percent = float(right_point-x)*lh_DIVggs

		lpecented = left_point_H*right_percent
		rpercented = right_point_H*left_percent
		try:
			point_hight
		except NameError:
			rsn = 0
			point_hight = lpecented+rpercented

			random.seed(seed+x+y+point_hight)
			if random.randint(-(int(lpecented*100)), int(rpercented*100)) >= 0:
				biom = left_biom
			else:
				biom = right_biom

		if y > point_hight:
			if int(y*bsInv) == int(point_hight*bsInv):
				return 6
			if y - 6*bs <= point_hight:
				return biom[2]
			else:
				random.seed(seed+x+y+seed-point_hight+biom[0]-biom[1]*x*y*x**2)
				rand = random.randint(0,20000)
				to_id = 1
				if rand < 250:
					to_id = 4
				if rand < 40 and point_hight+(20*bs) < y:
					to_id = 9
				if rand < 5 and point_hight+(100*bs) < y:
					to_id = 6
				return to_id
		else:
			if int(y*bsInv) >= 251:
				return 11
		return 0








































