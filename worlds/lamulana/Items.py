from typing import Dict, Set, Tuple, NamedTuple, Optional

class ItemData(NamedTuple):
	category: str
	code: int
	progression: bool = False
	useful: bool = False
	trap: bool = False
	count: int = 1
	game_code: int = 0
	cost: Optional[int] = None
	quantity: int = 1
	obtain_flag: Optional[int] = None
	obtain_value: Optional[int] = None

item_table: Dict[str, ItemData] = {
	'Leather Whip':                     ItemData('MainWeapon', 2359000, progression=True, count=0), #Cannot be sent, only as a starting item
	'Chain Whip':                       ItemData('MainWeapon', 2359001, progression=True, game_code=1),
	'Flail Whip':                       ItemData('MainWeapon', 2359002, progression=True, game_code=2),
	#gonna reserve 2359003 in case we ever implement progressive whips
	'Knife':                            ItemData('MainWeapon', 2359004, progression=True, game_code=3),
	'Key Sword':                        ItemData('MainWeapon', 2359005, progression=True, game_code=4),
	'Axe':                              ItemData('MainWeapon', 2359006, progression=True, game_code=5),
	'Katana':                           ItemData('MainWeapon', 2359007, progression=True, game_code=6),
	'Shuriken':                         ItemData('Subweapon', 2359008, progression=True, game_code=8),
	'Rolling Shuriken':                 ItemData('Subweapon', 2359009, progression=True, game_code=9),
	'Earth Spear':                      ItemData('Subweapon', 2359010, progression=True, game_code=10),
	'Flare Gun':                        ItemData('Subweapon', 2359011, progression=True, game_code=11),
	'Bomb':                             ItemData('Subweapon', 2359012, progression=True, game_code=12),
	'Chakram':                          ItemData('Subweapon', 2359013, progression=True, game_code=13),
	'Caltrops':                         ItemData('Subweapon', 2359014, progression=True, game_code=14),
	'Pistol':                           ItemData('Subweapon', 2359015, progression=True, game_code=15),
	'Buckler':                          ItemData('Subweapon', 2359016, useful=True, game_code=16),
	'Fake Silver Shield':               ItemData('Subweapon', 2359017, game_code=75),
	'Silver Shield':                    ItemData('Subweapon', 2359018, progression=True, game_code=17),
	'Angel Shield':                     ItemData('Subweapon', 2359019, progression=True, game_code=18),
	'Ankh Jewel':                       ItemData('Subweapon', 2359020, progression=True, count=0, game_code=19), #Adjust ankh jewel amount based on settings
	'Ankh Jewel (Amphisbaena)':         ItemData('Subweapon', 2359021, progression=True, count=0, game_code=19),
	'Ankh Jewel (Sakit)':               ItemData('Subweapon', 2359022, progression=True, count=0, game_code=19),
	'Ankh Jewel (Ellmac)':              ItemData('Subweapon', 2359023, progression=True, count=0, game_code=19),
	'Ankh Jewel (Bahamut)':             ItemData('Subweapon', 2359024, progression=True, count=0, game_code=19),
	'Ankh Jewel (Viy)':                 ItemData('Subweapon', 2359025, progression=True, count=0, game_code=19),
	'Ankh Jewel (Palenque)':            ItemData('Subweapon', 2359026, progression=True, count=0, game_code=19),
	'Ankh Jewel (Baphomet)':            ItemData('Subweapon', 2359027, progression=True, count=0, game_code=19),
	'Ankh Jewel (Tiamat)':              ItemData('Subweapon', 2359028, progression=True, count=0, game_code=19),
	'Ankh Jewel (Mother)':              ItemData('Subweapon', 2359029, progression=True, count=0, game_code=19),
	'Hand Scanner':                     ItemData('Usable', 2359030, progression=True, game_code=20),
	'Djed Pillar':                      ItemData('Usable', 2359031, progression=True, game_code=21),
	'Mini Doll':                        ItemData('Usable', 2359032, progression=True, game_code=22),
	'Magatama Jewel':                   ItemData('Usable', 2359033, progression=True, game_code=23),
	'Cog of the Soul':                  ItemData('Usable', 2359034, progression=True, game_code=24),
	'Lamp of Time':                     ItemData('Usable', 2359035, progression=True, game_code=25),
	'Pochette Key':                     ItemData('Usable', 2359036, progression=True, game_code=26),
	'Dragon Bone':                      ItemData('Usable', 2359037, progression=True, game_code=27),
	'Crystal Skull':                    ItemData('Usable', 2359038, progression=True, game_code=28),
	'Vessel':                           ItemData('Usable', 2359039, progression=True, game_code=29),
	'Medicine of the Mind':             ItemData('Usable', 2359040, progression=True, count=0, game_code=77), #Optionally swap counts with Vessel if a QoL option to skip the medicine process is added
	'Pepper':                           ItemData('Usable', 2359041, progression=True, game_code=30),
	'Woman Statue':                     ItemData('Usable', 2359042, progression=True, game_code=31),
	'Maternity Statue':                 ItemData('Usable', 2359043, progression=True, count=0, game_code=81), #Optionally swap counts with woman statue if a QoL option is added
	'Key of Eternity':                  ItemData('Usable', 2359044, progression=True, game_code=32),
	'Serpent Staff':                    ItemData('Usable', 2359045, progression=True, game_code=33),
	'Talisman':                         ItemData('Usable', 2359046, progression=True, game_code=34),
	'Diary':                            ItemData('Usable', 2359047, progression=True, game_code=72),
	'Mulana Talisman':                  ItemData('Usable', 2359048, progression=True, game_code=73),
	'Waterproof Case':                  ItemData('Inventory', 2359049, game_code=36),
	'Heatproof Case':                   ItemData('Inventory', 2359050, game_code=37),
	'Shell Horn':                       ItemData('Inventory', 2359051, game_code=38),
	'Glove':                            ItemData('Inventory', 2359052, useful=True, game_code=39),
	'Holy Grail':                       ItemData('Inventory', 2359053, progression=True, game_code=40),
	'Isis\' Pendant':                   ItemData('Inventory', 2359054, progression=True, game_code=41),
	'Crucifix':                         ItemData('Inventory', 2359055, useful=True, game_code=42),
	'Helmet':                           ItemData('Inventory', 2359056, progression=True, game_code=43),
	'Grapple Claw':                     ItemData('Inventory', 2359057, progression=True, game_code=44),
	'Bronze Mirror':                    ItemData('Inventory', 2359058, progression=True, game_code=45),
	'Eye of Truth':                     ItemData('Inventory', 2359059, progression=True, game_code=46),
	'Ring':                             ItemData('Inventory', 2359060, progression=True, game_code=47),
	'Scalesphere':                      ItemData('Inventory', 2359061, progression=True, game_code=48),
	'Gauntlet':                         ItemData('Inventory', 2359062, useful=True, game_code=49),
	'Anchor':                           ItemData('Inventory', 2359063, progression=True, game_code=50),
	'Plane Model':                      ItemData('Inventory', 2359064, progression=True, game_code=51),
	'Philosopher\'s Ocarina':           ItemData('Inventory', 2359065, progression=True, game_code=52),
	'Feather':                          ItemData('Inventory', 2359066, progression=True, game_code=53),
	'Book of the Dead':                 ItemData('Inventory', 2359067, progression=True, game_code=54),
	'Fairy Clothes':                    ItemData('Inventory', 2359068, useful=True, game_code=55),
	'Scriptures':                       ItemData('Inventory', 2359069, useful=True, game_code=56),
	'Hermes\' Boots':                   ItemData('Inventory', 2359070, progression=True, game_code=57),
	'Fruit of Eden':                    ItemData('Inventory', 2359071, progression=True, game_code=58),
	'Twin Statue':                      ItemData('Inventory', 2359072, progression=True, game_code=59),
	'Bracelet':                         ItemData('Inventory', 2359073, useful=True, game_code=60),
	'Perfume':                          ItemData('Inventory', 2359074, useful=True, game_code=61),
	'Spaulder':                         ItemData('Inventory', 2359075, game_code=62),
	'Dimensional Key':                  ItemData('Inventory', 2359076, progression=True, game_code=63),
	'Ice Cape':                         ItemData('Inventory', 2359077, progression=True, game_code=64),
	'Origin Seal':                      ItemData('Inventory', 2359078, progression=True, game_code=65),
	'Birth Seal':                       ItemData('Inventory', 2359079, progression=True, game_code=66),
	'Life Seal':                        ItemData('Inventory', 2359080, progression=True, game_code=67),
	'Death Seal':                       ItemData('Inventory', 2359081, progression=True, game_code=68),
	'Sacred Orb':                       ItemData('Inventory', 2359082, progression=True, count=10, game_code=69),
	'Treasures':                        ItemData('Inventory', 2359083, progression=True, game_code=71),
	'Mobile Super X2':                  ItemData('Inventory', 2359084, useful=True, game_code=76),
	'Provocative Bathing Suit':         ItemData('Inventory', 2359085, game_code=74),
	'reader.exe':                       ItemData('Software', 2359086, progression=True, game_code=85),
	'xmailer.exe':                      ItemData('Software', 2359087, game_code=86),
	'yagomap.exe':                      ItemData('Software', 2359088, progression=True, game_code=87),
	'yagostr.exe':                      ItemData('Software', 2359089, progression=True, game_code=88),
	'bunemon.exe':                      ItemData('Software', 2359090, useful=True, game_code=89),
	'bunplus.com':                      ItemData('Software', 2359091, game_code=90),
	'torude.exe':                       ItemData('Software', 2359092, progression=True, game_code=91),
	'guild.exe':                        ItemData('Software', 2359093, progression=True, game_code=92), #progression only if Hell Temple on
	'mantra.exe':                       ItemData('Software', 2359094, progression=True, game_code=93),
	'emusic.exe':                       ItemData('Software', 2359095, game_code=94),
	'beolamu.exe':                      ItemData('Software', 2359096, game_code=95),
	'deathv.exe':                       ItemData('Software', 2359097, useful=True, game_code=96),
	'randc.exe':                        ItemData('Software', 2359098, useful=True, game_code=97),
	'capstar.exe':                      ItemData('Software', 2359099, game_code=98),
	'move.exe':                         ItemData('Software', 2359100, useful=True, game_code=99),
	'mekuri.exe':                       ItemData('Software', 2359101, progression=True, game_code=100), #progression if key fairy combo
	'bounce.exe':                       ItemData('Software', 2359102, game_code=101),
	'miracle.exe':                      ItemData('Software', 2359103, progression=True, game_code=102), #progression if key fairy combo or NPC rando
	'mirai.exe':                        ItemData('Software', 2359104, progression=True, game_code=103),
	'lamulana.exe':                     ItemData('Software', 2359105, useful=True, game_code=104),
	'Map (Surface)':                    ItemData('Map', 2359106, game_code=70, obtain_flag=0xd1, obtain_value=2),
	'Map (Gate of Guidance)':           ItemData('Map', 2359107, game_code=70, obtain_flag=0xd2, obtain_value=2),
	'Map (Mausoleum of the Giants)':    ItemData('Map', 2359108, game_code=70, obtain_flag=0xd3, obtain_value=2),
	'Map (Temple of the Sun)':          ItemData('Map', 2359109, game_code=70, obtain_flag=0xd4, obtain_value=2),
	'Map (Spring in the Sky)':          ItemData('Map', 2359110, game_code=70, obtain_flag=0xd5, obtain_value=2),
	'Map (Inferno Cavern)':             ItemData('Map', 2359111, game_code=70, obtain_flag=0xd6, obtain_value=2),
	'Map (Chamber of Extinction)':      ItemData('Map', 2359112, game_code=70, obtain_flag=0xd7, obtain_value=2),
	'Map (Twin Labyrinths)':            ItemData('Map', 2359113, game_code=70, obtain_flag=0xd8, obtain_value=2),
	'Map (Endless Corridor)':           ItemData('Map', 2359114, game_code=70, obtain_flag=0xd9, obtain_value=2),
	'Map (Shrine of the Mother)':       ItemData('Map', 2359115, progression=True, game_code=70, obtain_flag=0xda, obtain_value=2),
	'Map (Gate of Illusion)':           ItemData('Map', 2359116, game_code=70, obtain_flag=0xdb, obtain_value=2),
	'Map (Graveyard of the Giants)':    ItemData('Map', 2359117, game_code=70, obtain_flag=0xdc, obtain_value=2),
	'Map (Temple of Moonlight)':        ItemData('Map', 2359118, game_code=70, obtain_flag=0xdd, obtain_value=2),
	'Map (Tower of the Goddess)':       ItemData('Map', 2359119, game_code=70, obtain_flag=0xde, obtain_value=2),
	'Map (Tower of Ruin)':              ItemData('Map', 2359120, game_code=70, obtain_flag=0xdf, obtain_value=2),
	'Map (Chamber of Birth)':           ItemData('Map', 2359121, game_code=70, obtain_flag=0xe0, obtain_value=2),
	'Map (Dimensional Corridor)':       ItemData('Map', 2359122, game_code=70, obtain_flag=0xe1, obtain_value=2),
	'Shuriken Ammo':                    ItemData('ShopInventory', 2359123, count=0, progression=True, game_code=107, quantity=10, cost=10),
	'Rolling Shuriken Ammo':            ItemData('ShopInventory', 2359124, count=0, progression=True, game_code=108, quantity=10, cost=10),
	'Earth Spear Ammo':                 ItemData('ShopInventory', 2359125, count=0, progression=True, game_code=109, quantity=10, cost=20),
	'Flare Gun Ammo':                   ItemData('ShopInventory', 2359126, count=0, progression=True, game_code=110, quantity=10, cost=40),
	'Bomb Ammo':                        ItemData('ShopInventory', 2359127, count=0, progression=True, game_code=111, quantity=10, cost=80),
	'Chakram Ammo':                     ItemData('ShopInventory', 2359128, count=0, progression=True, game_code=112, quantity=2, cost=55),
	'Caltrops Ammo':                    ItemData('ShopInventory', 2359129, count=0, progression=True, game_code=113, quantity=10, cost=30),
	'Pistol Ammo':                      ItemData('ShopInventory', 2359130, count=0, progression=True, game_code=114, quantity=1, cost=350),
	'5 Weights':                        ItemData('ShopInventory', 2359131, count=0, game_code=105, quantity=5, cost=10),
	'200 coins':                        ItemData('Resource', 2359132, count=0, game_code=-10, quantity=200),
	'100 coins':                        ItemData('Resource', 2359133, count=0, game_code=-10, quantity=100),
	'50 coins':                         ItemData('Resource', 2359134, count=0, game_code=-10, quantity=50),
	'30 coins':                         ItemData('Resource', 2359135, count=0, game_code=-10, quantity=30),
	'10 coins':                         ItemData('Resource', 2359136, count=0, game_code=-10, quantity=10),
	'1 Weight':                         ItemData('Resource', 2359137, count=0, game_code=-9, quantity=1),
	#Gap in IDs for other possible items in pool before trap items
	'Bat Trap':                         ItemData('Trap', 2359160, trap=True, count=0),
	'Explosive Trap':                   ItemData('Trap', 2359161, trap=True, count=0),
}

def get_items_by_category():
	categories: Dict[str, Set[str]] = {}
	for name, data in item_table.items():
		categories.setdefault(data.category, set()).add(name)
	return categories

item_exclusion_order = ['Map (Surface)', 'Map (Gate of Guidance)', 'Map (Mausoleum of the Giants)', 'Map (Temple of the Sun)', 'Map (Spring in the Sky)', 'Map (Inferno Cavern)', 'Map (Chamber of Extinction)', 'Map (Twin Labyrinths)', 'Map (Endless Corridor)', 'Map (Gate of Illusion)', 'Map (Graveyard of the Giants)', 'Map (Temple of Moonlight)', 'Map (Tower of the Goddess)', 'Map (Tower of Ruin)', 'Map (Chamber of Birth)', 'Map (Dimensional Corridor)', 'beolamu.exe', 'emusic.exe', 'bunplus.com', 'xmailer.exe', 'Waterproof Case', 'Heatproof Case', 'bounce.exe', 'capstar.exe', 'Fake Silver Shield', 'Shell Horn']