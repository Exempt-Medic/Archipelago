import zipfile
import os
import Utils
from typing import Dict, List, Set, Optional, TextIO, Union
from BaseClasses import MultiWorld, Tutorial, Region, Entrance, Item, ItemClassification
from Options import Accessibility
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_item_rule
from .Options import starting_weapon_names, LaMulanaOptions, StartingLocation, StartingWeapon, RandomizeCoinChests
from .WorldState import LaMulanaWorldState
from .NPCs import get_npc_checks, get_npc_entrance_room_names
from .Items import item_table, get_items_by_category, item_exclusion_order
from .Locations import get_locations_by_region
from .Regions import create_regions_and_locations
from .RcdMod import RcdMod
from .DatMod import DatMod
from .LocalConfig import LocalConfig

client_version = 1

class LaMulanaWebWorld(WebWorld):
	tutorial_en = Tutorial(
		"Multiworld Setup Tutorial",
		"A guide for how to set up La-Mulana multiworld",
		"English",
		"setup_en.md",
		"setup/en",
		["Author's-name"]
	)
	tutorials = [tutorial_en]

class LaMulanaWorld(World):
	"""
	Challenge the ruins in the 2012 remake of La-Mulana, a puzzle platformer that focuses
	on exploration and combat as much as it does on solving the puzzles and mysteries of the ruins.
	Will you discover the secret treasure of life?
	"""
	game = "La-Mulana"
	options_dataclass = LaMulanaOptions
	web = LaMulanaWebWorld()
	required_client_version = (0, 4, 0) #Placeholder version number

	worldstate: LaMulanaWorldState

	item_name_to_id = {name: data.code for name, data in item_table.items()}
	location_name_to_id = {location.name: location.code for locations in get_locations_by_region(None, None, None).values() for location in locations}
	location_name_to_id |= {location.name: location.code for locations in get_npc_checks(None, None).values() for location in locations}
	item_name_groups = get_items_by_category()

	precollected_items = {}

	def __init__(self, world : MultiWorld, player: int):
		super().__init__(world, player)
		self.precollected_items[self.player] = set()

	@classmethod
	def stage_assert_generate(cls, multiworld: MultiWorld):
		rcd_file = Utils.user_path("script.rcd")
		if not os.path.exists(rcd_file):
			raise FileNotFoundError(rcd_file)

		dat_file = Utils.user_path("script_code.dat")
		if not os.path.exists(dat_file):
			raise FileNotFoundError(dat_file)

	def generate_early(self) -> None:
		#Do stuff that can still modify settings
		self.options.local_items.value |= self.item_name_groups['ShopInventory']

		for setting_name, item_name in {('HolyGrailShuffle', 'Holy Grail'), ('MiraiShuffle', 'mirai.exe'), ('HermesBootsShuffle', 'Hermes\' Boots'), ('TextTraxShuffle', 'bunemon.exe')}:
			option = getattr(self.options, setting_name)
			if option == 'start_with':
				self.set_starting_item(item_name)
			elif option == 'own_world':
				self.options.local_items.value.add(item_name)
			elif option == 'different_world':
				self.options.non_local_items.value.add(item_name)

		starting_weapon_name = starting_weapon_names[self.options.StartingWeapon]
		main_weapons = {'Leather Whip', 'Knife', 'Key Sword', 'Axe', 'Katana'}
		if self.options.SubweaponOnly:
			#Starting subweapon incompatible with all locations reachable - switch to all items instead
			if self.options.accessibility == Accessibility.option_full:
				self.options.accessibility.value = Accessibility.option_minimal
			#Starting with a main weapon incompatible with subweapon-only setting - give a random starting subweapon instead
			if starting_weapon_name in main_weapons:
				option = self.options.StartingWeapon
				subweapon_options = [weapon_id for weapon_id, name in starting_weapon_names.items() if name not in main_weapons]
				chosen_subweapon = self.multiworld.random.choice(subweapon_options)
				option.value = chosen_subweapon
				starting_weapon_name = starting_weapon_names[chosen_subweapon]
			# Subweapon-only is incompatible with vanilla mother ankh
			if not self.options.AlternateMotherAnkh:
				self.options.AlternateMotherAnkh.value = 1

		self.set_starting_item(starting_weapon_name)

		if self.options.StartingLocation == StartingLocation.option_chamber_of_extinction:
			# Extinction start without entrance randomizer or glitch logic is blocked off on all sides
			if not self.options.RandomizeTransitions and not self.options.RandomizeBacksideDoors and not self.options.RaindropsInLogic and not self.options.LampGlitchInLogic:
				self.options.StartingLocation.value = StartingLocation.option_surface
			elif self.options.RequireFlareGun and starting_weapon_names[starting_weapon] != 'Flare Gun':
				self.set_starting_item('Flare Gun')
		if self.options.StartingLocation == StartingLocation.option_twin_labyrinths_front:
			self.set_starting_item('Twin Statue')
		elif self.options.StartingLocation == StartingLocation.option_tower_of_the_goddess:
			self.set_starting_item('Plane Model')
		elif self.options.StartingLocation in {StartingLocation.option_gate_of_illusion, StartingLocation.option_tower_of_ruin}:
			self.set_starting_item('Holy Grail')


	def create_regions(self) -> None:
		self.worldstate = LaMulanaWorldState(self, self.multiworld, self.player)
		create_regions_and_locations(self, self.multiworld, self.player, self.worldstate)

	def create_items(self) -> None:
		success = False
		self.assign_event_items()
		shop_items = self.create_shop_items()
		self.multiworld.itempool += shop_items
		self.multiworld.itempool += self.generate_item_pool(len(shop_items))
		print('Currently', len(self.multiworld.get_unfilled_locations()), 'unfilled locations in the pool, with', len(self.multiworld.itempool), 'items in the pool')

	def set_rules(self) -> None:
		self.multiworld.completion_condition[self.player] = lambda state: state.has_all({'Mother Defeated', 'NPC: Mulbruk'}, self.player)

		if self.options.RandomizeCoinChests == RandomizeCoinChests.option_include_escape_chest:
			#local progression would be a problem for the escape coin chest - if it involves another player and loops back to us, that's fine
			escape_location = self.multiworld.get_location('Twin Labyrinths - Escape Coin Chest', self.player)
			add_item_rule(escape_location, lambda item: item.player != self.player or not item.classification in {ItemClassification.progression, ItemClassification.progression_skip_balancing})

	def extend_hint_information(self, hint_data: Dict[int, Dict[int,str]]):
		hint_info = {}
		transition_display_names = self.worldstate.get_transition_spoiler_names()

		def get_transition_spoiler_name(transition_name):
			target = self.worldstate.transition_map[transition_name]
			pipe = False
			if target in {'Pipe L1', 'Pipe R1'}:
				target = self.worldstate.transition_map['Pipe R1' if target == 'Pipe L1' else 'Pipe R1']
				pipe = True
			return transition_display_names[target] + (' (Pipe)' if pipe else '')

		if self.worldstate.npc_rando and self.worldstate.npc_mapping:
			room_names = get_npc_entrance_room_names()
			npc_checks = get_npc_checks(self.multiworld, self.player)
			reverse_map = {y: x for x, y in self.worldstate.npc_mapping.items()}
			npc_transition_info = {
				'Priest Hidlyda': 'Spring D1',
				'Philosopher Giltoriyo': 'Spring D1',
				'Mr. Fishman (Original)': 'Spring D1',
				'Mr. Fishman (Alt)': 'Spring D1',
				'Mudman Qubert': 'Birth D1',
				'Priest Ashgine': 'Birth D1',
				'8-bit Elder': 'Retrosurface R1'
			}
			for npc_name, locationdata_list in npc_checks.items():
				if npc_name in reverse_map:
					door_name = reverse_map[npc_name]
					for locationdata in locationdata_list:
						if locationdata.code:
							target_transition = ''
							if self.worldstate.transition_rando and door_name in npc_transition_info:
								target_transition = f' past {get_transition_spoiler_name(npc_transition_info[door_name])}'
							hint_info[locationdata.code] = room_names[door_name] + target_transition

		if self.worldstate.transition_rando:
			check_transition_info = {
				'Spring in the Sky - Sacred Orb Chest': 'Spring D1',
				'Spring in the Sky - Map Chest': 'Spring D1',
				'Spring in the Sky - Ankh Jewel Chest': 'Spring D1',
				'Spring in the Sky - Caltrops Puzzle Reward': 'Spring D1',
				'Spring in the Sky - Glove Chest': 'Spring D1',
				'Spring in the Sky - Origin Seal Chest': 'Spring D1',
				'Spring in the Sky - Scalesphere Chest': 'Spring D1',
				'Chamber of Extinction - Map Chest': 'Extinction L2',
				'Shrine of the Mother - Death Seal Chest': 'Shrine D2',
				'Shrine of the Mother - Map Chest': 'Shrine D3',
				'Shrine of the Mother - Sacred Orb Chest': 'Shrine U1',
				'Shrine of the Mother - Crystal Skull Chest': 'Shrine U1',
				'Shrine of the Mother - Diary Chest': 'Shrine U1',
				'Shrine of the Mother - bounce.exe Chest': 'Shrine U1',
				'Gate of Illusion - Cog of the Soul Chest': 'Illusion R1',
				'Tower of Ruin - Map Chest': 'Ruin L1',
				'Chamber of Birth - Map Chest': 'Birth D1',
				'Chamber of Birth - Pochette Key Chest': 'Birth D1',
				'Chamber of Birth - Dimensional Key Chest': 'Birth D1',
				'Gate of Time (Surface) - lamulana.exe Chest': 'Retrosurface R1'
			}
			if self.options.RandomizeCoinChests:
				check_transition_info.update({
					'Spring in the Sky - Lower Path Coin Chest': 'Spring D1',
					'Shrine of the Mother - Katana Coin Chest': 'Shrine U1',
					'Chamber of Birth - Dance of Life Coin Chest': 'Birth D1'
				})
			for check_name, transition_name in check_transition_info.items():
				hint_info[self.multiworld.get_location(check_name, self.player).address] = get_transition_spoiler_name(transition_name)

		if self.worldstate.door_rando:
			check_door_info = {
				'Gate of Guidance - yagostr.exe Chest': 'Guidance Door',
				'Tower of Ruin - Djed Pillar Chest': 'Ruin Top Door',
				'Temple of the Sun - Talisman Location': 'Inferno Viy Door'
			}
			for check_name, door_name in check_door_info.items():
				target, req = self.worldstate.door_map[door_name]
				hint_info[self.multiworld.get_location(check_name, self.player).address] = f'{target} ({req})'

		if self.worldstate.cursed_chests:
			for cursed_chest_name in self.worldstate.cursed_chests:
				location = self.multiworld.get_location(cursed_chest_name, self.player)
				hint_info[location.address] = hint_info[location.address] + ' (Cursed)' if location.address in hint_info else 'Cursed'

		hint_data[self.player] = hint_info

	def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
		spoiler_handle.write(f'Cursed Chests ({len(self.worldstate.cursed_chests)}):\n')
		spoiler_handle.write(f'    - {self.worldstate.cursed_chests if len(self.worldstate.cursed_chests) else "None"}\n')

		def space_count(name):
			return ' ' * (25 - len(name))

		if self.worldstate.npc_rando and self.worldstate.npc_mapping:
			spoiler_handle.write('NPC Randomizer:\n')
			room_names = get_npc_entrance_room_names()
			reverse_map = {y: x for x, y in self.worldstate.npc_mapping.items()}
			for npc_name in self.worldstate.get_npc_hint_order():
				if npc_name in reverse_map:
					npc_door = reverse_map[npc_name]
					spoiler_handle.write(f'    - {npc_name}:{space_count(npc_name)}{room_names[npc_door]}\n')

		if self.options.RandomizeSeals:
			seal_spoilers = {value: [seal_name for seal_name, seal_val in self.worldstate.seal_map.items() if seal_val == value] for value in {1, 2, 3, 4}}
			seal_order = self.worldstate.get_seal_spoiler_order()
			for seal_val, seal_name in [(1, 'Origin Seal'), (2, 'Birth Seal'), (3, 'Life Seal'), (4, 'Death Seal')]:
				spoiler_handle.write(f'{seal_name}:\n')
				for seal_location in seal_order:
					if self.worldstate.seal_map[seal_location] == seal_val:
						spoiler_handle.write(f'    - {seal_location}\n')

		def arrows(source, dest, base_length, inner_text=None, display_names=None) -> str:
			oneways = {'Endless L1'}
			oneway_dests = {'Inferno W1', 'Goddess W1', 'Moonlight L1', 'Ruin L1', 'Endless One-way Exit', 'Guidance Door', 'Ruin Top Door'}
			if not self.options.RaindropsInLogic:
				oneway_dests |= {'Extinction L2', 'Dimensional D1', 'Illusion R1'}
			if not self.options.LampGlitchInLogic:
				oneway_dests.add('Inferno Viy Door')
			arrow_len = base_length - len(display_names[source]) if display_names and source in display_names else base_length - len(source)
			if inner_text:
				arrow_len -= 2 + len(inner_text)
				mid_str = ('=' * int((arrow_len / 2) + (arrow_len % 2))) + f'({inner_text})' + ('=' * int(arrow_len / 2))
			else:
				mid_str = '=' * arrow_len
			if source in oneways or dest in oneway_dests:
				return ' =' + mid_str + '> '
			if source in oneway_dests or dest in oneways:
				return ' <' + mid_str + '= '
			return ' <' + mid_str + '> '

		if self.worldstate.transition_rando:
			transition_display_names = self.worldstate.get_transition_spoiler_names()
			spoiler_handle.write('Transition Randomizer\n')
			for source in self.worldstate.get_transition_spoiler_order():
				if source not in self.worldstate.transition_map or source in {'Pipe L1', 'Pipe R1'}:
					continue
				dest = self.worldstate.transition_map[source]
				pipe = None
				if dest in {'Pipe L1', 'Pipe R1'}:
					pipe = 'pipe'
					dest = self.worldstate.transition_map['Pipe L1' if dest == 'Pipe R1' else 'Pipe R1']
				spoiler_handle.write(f'    - {transition_display_names[source]}{arrows(source,dest,59,pipe,transition_display_names)}{transition_display_names[dest]}\n')

		if self.worldstate.door_rando:
			doors_included = set()
			spoiler_handle.write('Door Randomizer\n')
			for source, (dest, requirement) in self.worldstate.door_map.items():
				if dest not in doors_included:
					doors_included.add(source)
					spoiler_handle.write(f'    - {source}{arrows(source,dest,40,requirement)}{dest}\n')

	def fill_slot_data(self) -> Dict[str, object]:
		slot_data : Dict[str, object] = self.options.as_dict(
			'ShopDensity',
			'RandomizeCoinChests',
			'RandomizeTrapItems',
			'RandomizeCursedChests',
			'CursedChestCount',
			'RandomizeNPCs',
			'RandomizeDracuetsShop',
			'HellTempleReward',
			'RandomizeSeals',
			'StartingLocation',
			'StartingWeapon',
			'HolyGrailShuffle',
			'MiraiShuffle',
			'HermesBootsShuffle',
			'TextTraxShuffle',
			'RandomizeTransitions',
			'RandomizeBacksideDoors',
			'RequireIceCape',
			'RequireFlareGun',
			'RequireKeyFairyCombo',
			'AutoScanGrailTablets',
			'GuardianSpecificAnkhJewels',
			'AlternateMotherAnkh',
			'AncientLaMulaneseLearned',
			'HardCombatLogic',
			'SubweaponOnly',
			'RaindropsInLogic',
			'CatPausingInLogic',
			'LampGlitchInLogic'
		)
		slot_data['cursed_chests'] = self.worldstate.cursed_chests
		if self.worldstate.npc_rando:
			slot_data['npc_locations'] = self.worldstate.npc_mapping
		if self.options.RandomizeSeals:
			slot_data['seal_data'] = self.worldstate.seal_map
		if self.worldstate.transition_rando:
			slot_data['transition_data'] = self.worldstate.transition_map
		if self.worldstate.door_rando:
			slot_data['door_data'] = self.worldstate.door_map
		return slot_data

	def set_starting_item(self, item_name: str):
		self.multiworld.push_precollected(self.create_item(item_name))
		self.precollected_items[self.player].add(item_name)

	def assign_event_items(self):
		for location in self.multiworld.get_locations(self.player):
			if location.address is None:
				item_name = location.name
				if 'Lamp Recharge' in location.name:
					item_name = 'Lamp Recharge'
				item = Item(item_name, ItemClassification.progression, None, self.player)
				location.place_locked_item(item)

	# Place specific shop items that must be present at an early shop (weights, subweapon ammo) and weights in Little Brother's shop
	# Determine which shop slots will contain local ShopInventory items and add rules to all locations to enforce that
	# Create these ShopInventory items, returning a list with them
	def create_shop_items(self):
		item_list: List[Item] = []

		starting_weapon = starting_weapon_names[self.options.StartingWeapon]

		if starting_weapon in {'Shuriken', 'Rolling Shuriken', 'Flare Gun', 'Earth Spear', 'Bomb', 'Chakram', 'Caltrops', 'Pistol'}:
			required_subweapon_ammo = starting_weapon + ' Ammo'
		else:
			required_subweapon_ammo = None

		if self.options.StartingLocation == StartingLocation.option_chamber_of_extinction and self.options.RequireFlareGun and starting_weapon != 'Flare Gun':
			required_subweapon_ammo_2 = 'Flare Gun Ammo'
		else:
			required_subweapon_ammo_2 = None

		shop_locations: Set[str] = self.worldstate.get_shop_location_names()

		#Little Brother needs weights
		lil_bro_slot = self.multiworld.random.choice(['Yiegah Kungfu Shop Item 1', 'Yiegah Kungfu Shop Item 2', 'Yiegah Kungfu Shop Item 3'])
		self.place_locked_item(lil_bro_slot, '5 Weights')
		shop_locations.remove(lil_bro_slot)

		if self.worldstate.is_surface_start:
			if self.worldstate.npc_rando:
				surface_shop_slots = []
				npc_checks = get_npc_checks(self.multiworld, self.player)
				if self.worldstate.npc_mapping['Former Mekuri Master'] == 'Elder Xelpud':
					if starting_weapon in {'Shuriken', 'Chakram', 'Pistol', 'Earth Spear'}:
						#Case: Xelpud is at Former Mekuri Master and starting subweapon that can break the wall - WorldState made sure a shop was at Xelpud
						possible_shop_npcs = {'Elder Xelpud'}
					else:
						#Case: main weapon that breaks mekuri wall, since WorldState makes sure other subweapons don't get Xelpud there
						possible_shop_npcs = {'Elder Xelpud', 'Nebur', 'Sidro', 'Modro', 'Moger', 'Hiner'}
				else:
					#Case: Xelpud is vanilla
					possible_shop_npcs = {'Nebur', 'Sidro', 'Modro', 'Moger', 'Hiner'}
				for surface_npc_door in possible_shop_npcs:
					npc_name = self.worldstate.npc_mapping[surface_npc_door]
					if npc_name in npc_checks:
						for location in npc_checks[npc_name]:
							if location.name in shop_locations:
								surface_shop_slots.append(location.name)
			else:
				surface_shop_slots = ['Nebur Shop Item 1', 'Nebur Shop Item 2', 'Nebur Shop Item 3', 'Sidro Shop Item 1', 'Sidro Shop Item 2', 'Sidro Shop Item 3', 'Modro Shop Item 1', 'Modro Shop Item 2', 'Modro Shop Item 3']
			if len(surface_shop_slots) > 0:
				weight_slot = self.multiworld.random.choice(surface_shop_slots)
				self.place_locked_item(weight_slot, '5 Weights')
				shop_locations.remove(weight_slot)
				if required_subweapon_ammo and len(surface_shop_slots) > 1:
					surface_shop_slots.remove(weight_slot)
					ammo_slot = self.multiworld.random.choice(surface_shop_slots)
					self.place_locked_item(ammo_slot, required_subweapon_ammo)
					shop_locations.remove(ammo_slot)
		else:
			starting_shop_slots = ['Starting Shop Item 1', 'Starting Shop Item 2', 'Starting Shop Item 3']
			weight_slot = self.multiworld.random.choice(starting_shop_slots)
			
			self.place_locked_item(weight_slot, '5 Weights')
			starting_shop_slots.remove(weight_slot)
			shop_locations.remove(weight_slot)

			if required_subweapon_ammo:
				subweapon_slot = self.multiworld.random.choice(starting_shop_slots)
				self.place_locked_item(subweapon_slot, required_subweapon_ammo)
				starting_shop_slots.remove(subweapon_slot)
				shop_locations.remove(subweapon_slot)
			if required_subweapon_ammo_2:
				subweapon_slot = self.multiworld.random.choice(starting_shop_slots)
				self.place_locked_item(subweapon_slot, required_subweapon_ammo_2)
				shop_locations.remove(subweapon_slot)

		slot_amount = len(shop_locations) - self.options.ShopDensity

		#Guaranteed minimum amounts per ammo type and weights
		shop_items: List[str] = ['5 Weights', '5 Weights']
		ammo_types = ['Shuriken Ammo', 'Rolling Shuriken Ammo', 'Earth Spear Ammo', 'Flare Gun Ammo', 'Bomb Ammo', 'Chakram Ammo', 'Caltrops Ammo', 'Pistol Ammo']
		for ammo_name in ammo_types:
			shop_items.extend([ammo_name, ammo_name])
		if slot_amount >= 19:
			shop_items.extend(self.multiworld.random.choices(ammo_types + ['5 Weights'], k=slot_amount - len(shop_items)))

		local_shop_inventory_list = self.multiworld.random.sample(list(shop_locations), slot_amount)

		shop_inventory_ids = {item_table[item_name].code for item_name in self.item_name_groups['ShopInventory']}
		for location in self.multiworld.get_unfilled_locations(self.player):
			if location.name in local_shop_inventory_list:
				add_item_rule(location, lambda item: item.player == self.player and item.code in shop_inventory_ids)
			else:
				add_item_rule(location, lambda item: item.code not in shop_inventory_ids)

		already_created = set()
		for item_name in shop_items:
			item_list.append(self.create_item(item_name, already_created))
			already_created.add(item_name)

		return item_list

	def get_excluded_items(self) -> Set[str]:
		#103 base locations (chests + NPC checks) + 27 coin chests + escape chest + 4 trap items + number of randomized items in shops + 1 Hell Temple check
		location_pool_size = 103 + (27 if self.options.RandomizeCoinChests else 0) + (1 if self.options.RandomizeCoinChests == RandomizeCoinChests.option_include_escape_chest else 0) + (4 if self.options.RandomizeTrapItems else 0) + self.options.ShopDensity + (1 if self.options.HellTempleReward else 0)

		item_pool_size = 126
		if self.options.AlternateMotherAnkh:
			item_pool_size += 1

		if self.options.SubweaponOnly:
			item_pool_size -= 6

		if not self.options.HellTempleReward:
			item_exclusion_order.append('guild.exe')

		for item_name, amt in self.options.start_inventory.value.items():
			if item_name == 'Ankh Jewel':
				if not self.options.GuardianSpecificAnkhJewels:
					item_pool_size -= min(amt, 9 if self.options.AlternateMotherAnkh else 8)
			elif item_name == 'Ankh Jewel (Mother)':
				if self.options.GuardianSpecificAnkhJewels and self.options.AlternateMotherAnkh:
					item_pool_size -= 1
			elif item_name in {'Ankh Jewel (Amphisbaena)', 'Ankh Jewel (Sakit)', 'Ankh Jewel (Ellmac)', 'Ankh Jewel (Bahamut)', 'Ankh Jewel (Viy)', 'Ankh Jewel (Palenque)', 'Ankh Jewel (Baphomet)', 'Ankh Jewel (Tiamat)'}:
				if self.options.GuardianSpecificAnkhJewels:
					item_pool_size -= 1
			else:
				item_pool_size -= min(amt, item_table[item_name].count)
			if item_name in item_exclusion_order:
				item_exclusion_order.remove(item_name)

		pool_diff = item_pool_size - location_pool_size
		if pool_diff <= 0:
			return None

		return set(item_exclusion_order[:pool_diff])

	def generate_item_pool(self, shop_item_amt: int) -> List[Item]:
		item_pool: List[Item] = []
		excluded_items = self.get_excluded_items()

		for name, data in item_table.items():
			if excluded_items and name in excluded_items:
				continue
			if data.category == 'MainWeapon' and self.options.SubweaponOnly:
				continue
			item_count = data.count
			if name in self.precollected_items[self.player]:
				item_count -= 1
			if name in self.options.start_inventory.value:
				item_count -= self.options.start_inventory.value[name]

			for _ in range(max(item_count, 0)):
				item = self.create_item(name)
				item_pool.append(item)

		if self.options.GuardianSpecificAnkhJewels:
			guardians = {'Amphisbaena', 'Sakit', 'Ellmac', 'Bahamut', 'Viy', 'Palenque', 'Baphomet', 'Tiamat'}
			if self.options.AlternateMotherAnkh:
				guardians.add('Mother')
			for guardian in guardians:
				jewel_name = f'Ankh Jewel ({guardian})'
				if jewel_name not in self.options.start_inventory.value:
					item_pool.append(self.create_item(jewel_name))
		else:
			ankh_jewel_amt = 9 if self.options.AlternateMotherAnkh else 8
			if 'Ankh Jewel' in self.options.start_inventory.value:
				ankh_jewel_amt -= self.options.start_inventory.value['Ankh Jewel']
			for _ in range(ankh_jewel_amt):
				item_pool.append(self.create_item('Ankh Jewel'))

		filler_pool_size = len(self.multiworld.get_unfilled_locations(self.player)) - shop_item_amt - len(item_pool)

		for i in range(filler_pool_size):
			item_pool.append(self.create_item(self.get_filler_item(i)))

		return item_pool

	def create_item(self, name: str, exclude_shop_progression:Set[str]=None) -> Item:
		data = item_table[name]

		if data.category == 'ShopInventory' and data.progression:
			if exclude_shop_progression and name in exclude_shop_progression:
				classification = ItemClassification.filler
			else:
				classification = ItemClassification.progression_skip_balancing
		elif data.progression:
			classification = ItemClassification.progression
		elif data.useful:
			classification = ItemClassification.useful
		elif data.trap:
			classification = ItemClassification.trap
		else:
			classification = ItemClassification.filler

		item = Item(name, classification, data.code, self.player)

		if not item.advancement:
			return item

		if name == 'guild.exe' and not self.options.HellTempleReward:
			item.classification = ItemClassification.filler
		elif name == 'miracle.exe' and not self.options.RandomizeNPCs and not self.options.RequireKeyFairyCombo:
			item.classification = ItemClassification.useful
		elif name == 'mekuri.exe' and not self.options.RequireKeyFairyCombo:
			item.classification = ItemClassification.useful
		elif name == 'Mulana Talisman' and len(self.worldstate.cursed_chests) == 0:
			item.classification = ItemClassification.filler

		return item

	def get_filler_item(self, k: Optional[int]):
		# Temporary placeholder for filler items until more involved RCD edits can be implemented and tested
		return 'Shell Horn'
		if k == 0:
			return '200 coins'
		elif k and k <= 2:
			return '100 coins'
		return self.multiworld.random.choices(['50 coins', '30 coins', '10 coins', '1 Weight'], weights=[1, 4, 6, 2], k=1)[0]

	def place_locked_item(self, location_name: str, item_name: str):
		self.multiworld.get_location(location_name, self.player).place_locked_item(self.create_item(item_name))

	def start_inventory_as_list(self) -> List[str]:
		out = []
		for item_name, count in self.options.start_inventory.value.items():
			for _ in range(count):
				out.append(item_name)
		return out

	def generate_output(self, output_directory: str) -> None:
		local_config = LocalConfig(self.multiworld, self.player)
		rcd_mod = RcdMod("script.rcd", local_config)
		dat_mod = DatMod("script_code.dat", local_config)

		dat_mod.rewrite_xelpud_flag_checks()
		dat_mod.rewrite_xelpud_mulana_talisman_conversation()
		dat_mod.rewrite_xelpud_talisman_conversation()
		dat_mod.rewrite_xelpud_pillar_conversation()

		locations = self.multiworld.get_locations(self.player)

		for location in locations:
			item = item_table.get(location.item.name)
			if (item is None and location.item.player == self.player) or location.address is None:
				continue

			item_id = item.game_code if item is not None and location.item.player == self.player else 83
			if location.file_type == 'rcd':
				rcd_mod.place_item_in_location(item, item_id, location)
			elif location.file_type == 'dat':
				dat_mod.place_item_in_location(item, item_id, location)

		rcd_mod.give_starting_items(self.start_inventory_as_list() + list(self.precollected_items[self.player]))
		rcd_mod.rewrite_diary_chest()
		rcd_mod.add_diary_chest_timer()
		if self.options.AutoScanGrailTablets:
			rcd_mod.create_grail_autoscans()

		output_path = os.path.join(output_directory, f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.get_file_safe_player_name(self.player)}_{Utils.__version__}.zip")
		with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED, True, 9) as output_zip:
			output_zip.writestr("script.rcd", rcd_mod.write_file())
			output_zip.writestr("script_code.dat", dat_mod.write_file())
			output_zip.writestr("lamulana-config.toml", local_config.write_file())