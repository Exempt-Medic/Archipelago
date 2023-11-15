from __future__ import annotations

from Options import StartInventoryPool, PerGameCommonOptions, Choice, Option

from typing import Dict


class ApeEscapeOptions(PerGameCommonOptions):
    start_inventory = StartInventoryPool

class DebugOption(Choice):
    """Choose current Debug Settings

        Off: No debug settings
        Early Items: Gadgets will be placed in first two levels
        Early Keys: Keys will be placed in the first two levels

        Supported values: off, item, key
        Default value: off
        """

    display_name = "Debug Option"
    option_off = 0x00
    option_item = 0x01
    option_key = 0x02
    default = option_off

class GoalOption(Choice):
    """Choose end goal

        first: First final boss at Monkey Madness
        second: 100% boss at Peak Point Matrix

        Supported values: first, second
        Default value: first
    """

    display_name = "Goal"
    option_first = 0x00
    option_second = 0x01
    default = option_first

apeescape_option_definitions: Dict[str, type(Option)] = {
    "debug": DebugOption,
    "goal": GoalOption
}