from SbConstants import *

def crafts():

	stick_craft = ((0,0),(0,0),(0,0),  (0,0),(20,1),(0,0),  (0,0),(20,1),(0,0),  (-1,4, False)) #craft items, craft data give id and count, any pos





#	stick_craftANY = ((0,0),(0,0),(0,0),  (0,0),(0,0),(0,0),  (0,0),(0,0),(0,0),  (-1,4, False))
#	CRAFTS1.append(stick_craftANY)

	wood_craft = ((7,1),(0,0),(0,0),  (0,0),(0,0),(0,0),  (0,0),(0,0),(0,0),  (20,4, False))
	pickaxe_craft = ((22,1),(22,1),(22,1),  (0,0),(-1,1),(0,0),  (0,0),(-1,1),(0,0),  (-2,1, False))
	lead_craft = ((-1,1),(0,0),(-1,1),  (0,0),(-1,1),(0,0),  (-1,1),(0,0),(-1,1),  (BLOCK_LEAD,1, False))
	Ipickaxe_craft = ((-10,1),(-10,1),(-10,1),  (0,0),(-1,1),(0,0),  (0,0),(-1,1),(0,0),  (-3,1, False))
	Dpickaxe_craft = ((-6,1),(-6,1),(-6,1),  (0,0),(-1,1),(0,0),  (0,0),(-1,1),(0,0),  (-4,1, False))
	lopata_craft = ((0,0),(22,1),(0,0),  (22,1),(-1,1),(22,1),  (0,0),(-1,1),(0,0),  (-7,1, False))
	Dlopata_craft = ((0,0),(-6,1),(-6,0),  (-6,1),(-1,1),(-6,1),  (0,0),(-1,1),(0,0),  (-9,1, False))
	iron_ingot = ((9,1),(0,0),(0,0),  (0,0),(0,0),(0,0),  (0,0),(0,0),(0,0),  (-10,1, False))
	flour = ((0,0),(0,0),(0,0),  (0,0),(0,0),(0,0),  (-12,1),(-12,1),(-12,1),  (-13,3, False)) #muka
	bread = ((-13,1),(-13,1),(-13,1),  (0,0),(0,0),(0,0),  (0,0),(0,0),(0,0),  (-11,1, False))
	seeds = ((-12,1),(0,0),(0,0),  (0,0),(0,0),(0,0),  (0,0),(0,0),(0,0),  (ITEM_WHEAT_SEEDS,3, False))
	torch = ((0,0),(0,0),(0,0),  (0,0),(-16,1),(0,0),  (0,0),(-1,1),(0,0),  (ITEM_TORCH,4, False))
	stone_axe = ((22,1),(22,1),(0,0),  (22,1),(-1,1),(0,0),  (0,0),(-1,1),(0,0),  (ITEM_STONE_AXE,1, False))
	iron_axe = ((-10,1),(-10,1),(0,0),  (-10,1),(-1,1),(0,0),  (0,0),(-1,1),(0,0),  (ITEM_IRON_AXE,1, False))
	chest_craft = ((20,1),(20,1),(20,1),  (20,1),(22,1),(20,1),  (20,1),(20,1),(20,1),  (BLOCK_CHEST,1, False))
	planks_craft = ((0,0),(0,0),(0,0),  (0,0),(7,1),(0,0),  (0,0),(0,0),(0,0),  (BLOCK_PLANKS,4, False))
	stone_sword = ((0,0),(22,1),(0,0),  (0,0),(22,1),(0,0),  (0,0),(-1,1),(0,0),  (ITEM_STONE_SWORD,1, False))
	mega_crystall_block_craft = ((ITEM_MEGA_CRYSTAL,1),(ITEM_MEGA_CRYSTAL,1),(ITEM_MEGA_CRYSTAL,1),  (ITEM_MEGA_CRYSTAL,1),(ITEM_MEGA_CRYSTAL,1),(ITEM_MEGA_CRYSTAL,1),  (ITEM_MEGA_CRYSTAL,1),(ITEM_MEGA_CRYSTAL,1),(ITEM_MEGA_CRYSTAL,1),  (BLOCK_MEGA_CRYSTAL,1, False))
	sandstone_craft = ((BLOCK_SAND,1),(BLOCK_SAND,1),(0,0),  (BLOCK_SAND,1),(BLOCK_SAND,1),(0,0),  (0,0),(0,0),(0,0),  (BLOCK_SANDSTONE,4, False))


	tnt_craft = ((ITEM_STONE_COAL,1),(BLOCK_PLANKS,1),(ITEM_STONE_COAL,1),  (BLOCK_PLANKS,1),(ITEM_DIAMOND,1),(BLOCK_PLANKS,1),  (ITEM_STONE_COAL,1),(BLOCK_PLANKS,1),(ITEM_STONE_COAL,1),  (BLOCK_TNT,4, False))

	print BLOCK_LEAD



	CRAFTS1 = {
				 BLOCK_LEAD:lead_craft,
				-ITEM_STICK:stick_craft,
				20:planks_craft,
				-2:pickaxe_craft,
				-3:Ipickaxe_craft,
				-4:Dpickaxe_craft,
				-7:lopata_craft,
				-9:Dlopata_craft,
				-10:iron_ingot,
				-12:bread,
				-13:flour,
				-14:seeds,
				-15:torch,
				-17:stone_axe,
				 21:chest_craft,
				 ITEM_STONE_SWORD:stone_sword,
				 BLOCK_TNT:tnt_craft,
				 BLOCK_MEGA_CRYSTAL:mega_crystall_block_craft,
				 BLOCK_SANDSTONE:sandstone_craft
				}




	return CRAFTS1
