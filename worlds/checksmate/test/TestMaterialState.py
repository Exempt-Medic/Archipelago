from . import CMTestBase
from .. import determine_difficulty, CMOptions


class MaterialStateTestBase(CMTestBase):

    def world_setup(self):
        self.options["goal"] = "single"
        super().world_setup()

        # this class ultimately isn't trying to test this relatively simple function
        self.difficulty = determine_difficulty(self.world.options)

    def test_basic_fill(self):
        # this is mostly to demonstrate that collect fundamentally acquires the items and to show that setUp sets up
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Progressive Pawn"])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Material"])
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)
        self.assertEqual(
            len([item for item in self.multiworld.itempool if item.name == "Progressive Pawn"]),
            self.multiworld.state.prog_items[self.player]["Progressive Pawn"])


class TestSimpleMaterial(MaterialStateTestBase):
    """
    Checks that goal can be reached based on the math performed by collect()

    If this fails, it's not necessarily the fault of collect(), it might be that the generator isn't adding enough items
    """
    def test_no_options(self):
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)
        past_material = self.multiworld.state.prog_items[self.player]["Material"]
        self.assertLessEqual(4050 * self.difficulty, past_material)
        self.assertGreaterEqual(4650 * self.difficulty, past_material)


class TestCyclicMaterial(MaterialStateTestBase):
    """Removes all material, then adds it back again. This tests remove() via sledgehammer method"""
    def test_no_options(self):
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)
        past_material = self.multiworld.state.prog_items[self.player]["Material"]
        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])
        self.assertLessEqual(4050 * self.difficulty, past_material)
        self.assertGreaterEqual(4650 * self.difficulty, past_material)

        for item in list(self.multiworld.state.prog_items[self.player].keys()):
            self.remove_by_name(item)
        # self.assertEqual(0, self.multiworld.state.prog_items[self.player])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Progressive Pawn"])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Material"])
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)

        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])

    """Same as before, but backward, to test "children" logic"""
    def test_backward(self):
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)
        past_material = self.multiworld.state.prog_items[self.player]["Material"]
        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])
        self.assertLessEqual(4050 * self.difficulty, past_material)
        self.assertGreaterEqual(4650 * self.difficulty, past_material)

        items = list(self.multiworld.state.prog_items[self.player].keys())
        items.reverse()
        for item in items:
            self.remove_by_name(item)
        # self.assertEqual(0, self.multiworld.state.prog_items[self.player])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Progressive Pawn"])
        self.assertEqual(0, self.multiworld.state.prog_items[self.player]["Material"])
        self.collect_all_but("Progressive Pocket Gems", self.multiworld.state)

        self.assertEqual(past_material, self.multiworld.state.prog_items[self.player]["Material"])
