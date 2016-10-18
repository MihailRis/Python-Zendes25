from SbConstants import *
from pygame import mixer



def explode(x,y, blocks, mobs, player):
	mixer.init()
	SOUNDS["BOMB"].play()
	for block in blocks:
		block = blocks[block]
		distance = dist(x,block.x,y,block.y)
		if distance <= 6*bs:
			if True:
				if block.id == 12:
					block.id = 0
					explode(block.x,block.y, blocks, mobs, player)
				block.reset_block(0)

	for mob in mobs:
		if abs(x-mob.x) + abs(y-mob.y) <= 200:
			distance = dist(x,mob.x,y,mob.y)
			if distance <= 10*bs:
				mob.damage((10-distance)*5)

	distance = dist(x,player.x,y,player.y)
	if distance <= 10*bs:
#		print -int(10-distance)*2
		player.hp += -abs(int(10*bs-distance))*0.04

		speed = 100.0
		if distance >= 5*bs:
			if player.x > x:
				player.xvel += speed
			if player.x < x:
				player.xvel += -speed

		player.yvel += -float(speed/200)
		player.y += -10
