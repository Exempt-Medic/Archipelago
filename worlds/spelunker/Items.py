from typing import Dict, Set, List, NamedTuple, Optional
from BaseClasses import ItemClassification

class ItemData(NamedTuple):
    category: str
    code: Optional[int]
    classification: ItemClassification
    amount: int = 0

item_table: Dict[str, ItemData] = {
    "Money Bag": ItemData("Treasure", 0x696969, ItemClassification.filler),
    "Coin": ItemData("Treasure", 0x69696A, ItemClassification.filler),
    "Miracle": ItemData("Treasure", 0x69696B, ItemClassification.filler),
    "Diamond": ItemData("Treasure", 0x69696C, ItemClassification.filler),
    "Dynamite": ItemData("Equipment", 0x69696D, ItemClassification.progression, 18),
    "Flare": ItemData("Equipment", 0x69696E, ItemClassification.progression, 9),
    "Blue Key": ItemData("Equipment", 0x69696F, ItemClassification.progression, 9),
    "Red Key": ItemData("Equipment", 0x696970, ItemClassification.progression, 6),

    "1-Up": ItemData("Powerups", 0x696971, ItemClassification.useful),
    "Multiplier": ItemData("Powerups", 0x696972, ItemClassification.useful),
    "Potion": ItemData("Powerups", 0x696973, ItemClassification.useful),
    "Invincibility": ItemData("Powerups", 0x696974, ItemClassification.useful),

    "Golden Pyramid": ItemData("Events", None, ItemClassification.progression)
}

filler_items: List[str] = [
    "Money Bag",
    "Coin",
    "Diamond",
    "Miracle"
]
useful_items: List[str] = [
    "1-Up",
    "Multiplier",
    "Potion",
    "Invincibility"
]

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        if data.category != "Events":
            categories.setdefault(data.category, set()).add(name)

    return categories
