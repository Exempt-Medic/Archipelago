locations = {
    'Mushroom Zone': {'id': 0x00, 'ram_index': 0, 'type': 'level'},
    'Mushroom Zone Midway Bell': {'id': 0x00, 'ram_index': 0, 'clear_condition': ("Mushroom Zone Midway Bell", 1), 'type': 'bell'},
    'Scenic Course': {'id': 0x19, 'ram_index': 40, 'type': 'level'},
    'Tree Zone 1 - Invincibility!': {'id': 0x01, 'ram_index': 1, 'clear_condition': ("Tree Zone Progression", 1), 'type': 'level'},
    'Tree Zone 1 - Invincibility! Midway Bell': {'id': 0x01, 'ram_index': 1,  'clear_condition': ("Tree Zone 1 - Invincibility! Midway Bell", 1), 'type': 'bell'},
    'Tree Zone 2 - In the Trees': {'id': 0x02, 'ram_index': 2, 'clear_condition': ("Tree Zone Progression", 2), 'type': 'level'},
    'Tree Zone 2 - In the Trees Secret Exit': {'id': 0x02, 'ram_index': 2, 'clear_condition': ("Tree Zone Secret", 1), 'type': 'secret'},
    'Tree Zone 2 - In the Trees Midway Bell': {'id': 0x02, 'ram_index': 2, 'clear_condition': ("Tree Zone 2 - In the Trees Midway Bell", 1), 'type': 'bell'},
    'Tree Zone 3 - The Exit': {'id': 0x04, 'ram_index': 4, 'clear_condition': ("Tree Zone Progression", 3), 'type': 'level'},
    'Tree Zone 4 - Honeybees': {'id': 0x03, 'ram_index': 3, 'clear_condition': ("Tree Zone Progression", 3), 'type': 'level'},
    'Tree Zone 4 - Honeybees Midway Bell': {'id': 0x03, 'ram_index': 3, 'clear_condition': ("Tree Zone 4 - Honeybees Midway Bell", 1), 'type': 'bell'},
    'Tree Zone 5 - The Big Bird': {'id': 0x05, 'ram_index': 5, 'clear_condition': ("Tree Coin", 1), 'type': 'level'},
    'Tree Zone 5 - The Big Bird Midway Bell': {'id': 0x05, 'ram_index': 5, 'clear_condition': ("Tree Zone 5 - The Big Bird Midway Bell", 1), 'type': 'bell'},
    'Tree Zone - Secret Course': {'id': 0x1D, 'ram_index': 36, 'type': 'level'},
    'Hippo Zone': {'id': 0x11, 'ram_index': 31, 'type': 'level'},
    'Space Zone 1 - Moon Stage': {'id': 0x12, 'ram_index': 16, 'clear_condition': ("Space Zone Progression", 1), 'type': 'level'},
    'Space Zone 1 - Moon Stage Secret Exit': {'id': 0x12, 'ram_index': 16, 'clear_condition': ("Space Zone Secret", 1), 'type': 'secret'},
    'Space Zone 1 - Moon Stage Midway Bell': {'id': 0x12, 'ram_index': 16, 'clear_condition': ("Space Zone 1 - Moon Stage Midway Bell", 1), 'type': 'bell'},
    'Space Zone - Secret Course': {'id': 0x1C, 'ram_index': 41, 'type': 'level'},
    'Space Zone 2 - Star Stage': {'id': 0x13, 'ram_index': 17, 'clear_condition': ("Space Coin", 1), 'type': 'level'},
    'Space Zone 2 - Star Stage Midway Bell': {'id': 0x13, 'ram_index': 17, 'clear_condition': ("Space Zone 2 - Star Stage Midway Bell", 1), 'type': 'bell'},
    'Macro Zone 1 - The Ant Monsters': {'id': 0x14, 'ram_index': 11, 'clear_condition': ("Macro Zone Progression", 1), 'type': 'level'},
    'Macro Zone 1 - The Ant Monsters Secret Exit': {'id': 0x14, 'ram_index': 11, 'clear_condition': ("Macro Zone Secret 1", 1), 'type': 'secret'},
    'Macro Zone 1 - The Ant Monsters Midway Bell': {'id': 0x14, 'ram_index': 11, 'clear_condition': ("Macro Zone 1 - The Ant Monsters Midway Bell", 1), 'type': 'bell'},
    'Macro Zone 2 - In the Syrup Sea': {'id': 0x15, 'ram_index': 12, 'clear_condition': ("Macro Zone Progression", 2), 'type': 'level'},
    'Macro Zone 2 - In the Syrup Sea Midway Bell': {'id': 0x15, 'ram_index': 12, 'clear_condition': ("Macro Zone 2 - In the Syrup Sea Midway Bell", 1), 'type': 'bell'},
    'Macro Zone 3 - Fiery Mario-Special Agent': {'id': 0x16, 'ram_index': 13, 'clear_condition': ("Macro Zone Progression", 3), 'type': 'level'},
    'Macro Zone 3 - Fiery Mario-Special Agent Midway Bell': {'id': 0x16, 'ram_index': 13, 'clear_condition': ("Macro Zone 3 - Fiery Mario-Special Agent Midway Bell", 1), 'type': 'bell'},
    'Macro Zone 4 - One Mighty Mouse': {'id': 0x17, 'ram_index': 14, 'clear_condition': ("Macro Coin", 1), 'type': 'level'},
    'Macro Zone 4 - One Mighty Mouse Midway Bell': {'id': 0x17, 'ram_index': 14, 'clear_condition': ("Macro Zone 4 - One Mighty Mouse Midway Bell", 1), 'type': 'bell'},
    'Macro Zone - Secret Course': {'id': 0x1E, 'ram_index': 35, 'clear_condition': ("Macro Zone Secret 2", 1), 'type': 'level'},
    'Pumpkin Zone 1 - Bat Course': {'id': 0x06, 'ram_index': 6, 'clear_condition': ("Pumpkin Zone Progression", 1), 'type': 'level'},
    'Pumpkin Zone 1 - Bat Course Midway Bell': {'id': 0x06, 'ram_index': 6, 'clear_condition': ("Pumpkin Zone 1 - Bat Course Midway Bell", 1), 'type': 'bell'},
    'Pumpkin Zone 2 - Cyclops Course': {'id': 0x07, 'ram_index': 7, 'clear_condition': ("Pumpkin Zone Progression", 2), 'type': 'level'},
    'Pumpkin Zone 2 - Cyclops Course Secret Exit': {'id': 0x07, 'ram_index': 7, 'clear_condition': ("Pumpkin Zone Secret 1", 1), 'type': 'secret'},
    'Pumpkin Zone 2 - Cyclops Course Midway Bell': {'id': 0x07, 'ram_index': 7, 'clear_condition': ("Pumpkin Zone Progression", 2), 'type': 'bell'},
    'Pumpkin Zone 3 - Ghost House': {'id': 0x08, 'ram_index': 8, 'clear_condition': ("Pumpkin Zone Progression", 3), 'type': 'level'},
    'Pumpkin Zone 3 - Ghost House Secret Exit': {'id': 0x08, 'ram_index': 8, 'clear_condition': ("Pumpkin Zone Secret 2", 1), 'type': 'secret'},
    'Pumpkin Zone 3 - Ghost House Midway Bell': {'id': 0x08, 'ram_index': 8, 'clear_condition': ("Pumpkin Zone Progression", 3), 'type': 'bell'},
    "Pumpkin Zone 4 - Witch's Mansion": {'id': 0x09, 'ram_index': 9, 'clear_condition': ("Pumpkin Coin", 1), 'type': 'level'},
    "Pumpkin Zone 4 - Witch's Mansion Midway Bell": {'id': 0x09, 'ram_index': 9, 'clear_condition': ("Pumpkin Coin", 1), 'type': 'bell'},
    'Pumpkin Zone - Secret Course 1': {'id': 0x1B, 'ram_index': 38, 'type': 'level'},
    'Pumpkin Zone - Secret Course 2': {'id': 0x1F, 'ram_index': 39, 'type': 'level'},
    'Mario Zone 1 - Fiery Blocks': {'id': 0x0A, 'ram_index': 26, 'clear_condition': ("Mario Zone Progression", 1), 'type': 'level'},
    'Mario Zone 1 - Fiery Blocks Midway Bell': {'id': 0x0A, 'ram_index': 26, 'clear_condition': ("Mario Zone 1 - Fiery Blocks Midway Bell", 1), 'type': 'bell'},
    'Mario Zone 2 - Mario the Circus Star!': {'id': 0x0B, 'ram_index': 27, 'clear_condition': ("Mario Zone Progression", 2), 'type': 'level'},
    'Mario Zone 2 - Mario the Circus Star! Midway Bell': {'id': 0x0B, 'ram_index': 27, 'clear_condition': ("Mario Zone 2 - Mario the Circus Star! Midway Bell", 1), 'type': 'bell'},
    'Mario Zone 3 - Beware: Jagged Spikes': {'id': 0x0C, 'ram_index': 28, 'clear_condition': ("Mario Zone Progression", 3), 'type': 'level'},
    'Mario Zone 3 - Beware: Jagged Spikes Midway Bell': {'id': 0x0C, 'ram_index': 28, 'clear_condition': ("Mario Zone 3 - Beware: Jagged Spikes Midway Bell", 1), 'type': 'bell'},
    'Mario Zone 4 - Three Mean Pigs!': {'id': 0x0D, 'ram_index': 29, 'clear_condition': ("Mario Coin", 1), 'type': 'level'},
    'Mario Zone 4 - Three Mean Pigs! Midway Bell': {'id': 0x0D, 'ram_index': 29, 'clear_condition': ("Mario Zone 4 - Three Mean Pigs! Midway Bell", 1), 'type': 'bell'},
    'Turtle Zone 1 - Cheep Cheep Course': {'id': 0x0E, 'ram_index': 21, 'clear_condition': ("Turtle Zone Progression", 1), 'type': 'level'},
    'Turtle Zone 1 - Cheep Cheep Course Midway Bell': {'id': 0x0E, 'ram_index': 21, 'clear_condition': ("Turtle Zone 1 - Cheep Cheep Course Midway Bell", 1), 'type': 'bell'},
    'Turtle Zone 2 - Turtle Zone': {'id': 0x0F, 'ram_index': 22, 'clear_condition': ("Turtle Zone Progression", 2), 'type': 'level'},
    'Turtle Zone 2 - Turtle Zone Secret Exit': {'id': 0x0F, 'ram_index': 22, 'clear_condition': ("Turtle Zone Secret", 1), 'type': 'secret'},
    'Turtle Zone 2 - Turtle Zone Midway Bell': {'id': 0x0F, 'ram_index': 22, 'clear_condition': ("Turtle Zone 2 - Turtle Zone Midway Bell", 1), 'type': 'bell'},
    'Turtle Zone 3 - Whale Course': {'id': 0x10, 'ram_index': 23, 'clear_condition': ("Turtle Coin", 1), 'type': 'level'},
    'Turtle Zone 3 - Whale Course Midway Bell': {'id': 0x10, 'ram_index': 23, 'clear_condition': ("Turtle Zone 3 - Whale Course Midway Bell", 1), 'type': 'bell'},
    'Turtle Zone - Secret Course': {'id': 0x1A, 'ram_index': 37, 'type': 'level'}
}