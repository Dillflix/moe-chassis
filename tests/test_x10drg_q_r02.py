"""Check R02 routing, physical joint clearances and P1S placement limits."""
from copy import deepcopy
from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source"))
from x10drg_q_r01.build import box, overlap
from x10drg_q_r02.build import make_layout, placement_report, validate_config


class R02GeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((ROOT / "source/x10drg_q_r02/layout.json").read_text())
        cls.parts, _, cls.kinds, cls.datums = make_layout(
            cls.config, cls.config["chassis"]["variants"]["extended"])

    def test_each_passive_card_has_its_own_full_fan_keepout(self):
        dedicated = {n: p for n, p in self.parts.items() if n.startswith("DEDICATED_FAN")}
        self.assertEqual(len(dedicated), 3)
        self.assertEqual(set(self.datums["passive_duct_inlet_areas_mm2"].values()), {14400})
        for slot, (x, z) in self.config["r02"]["fan_routes"].items():
            name = f"DEDICATED_FAN_SLOT{slot}_FULL_KEEP_OUT"
            y = self.config["chassis"]["variants"]["extended"] - self.config["fans"]["duct_rear_offset_from_depth"]
            self.assertAlmostEqual(overlap(dedicated[name], box(x - 1, y + 1, z - 1, 2, 2, 2)), 8)

    def test_spigot_clearance_is_present_in_actual_solid_geometry(self):
        r = self.config["r02"]
        wall = self.config["ducts"]["wall"]
        for i, slot in enumerate((8, 6, 4)):
            cx, z0 = r["route_middle_centers_x"][i], r["route_middle_bottom_z"][i]
            male = self.parts[f"SLOT{slot}_GPU_HALF_PROTOTYPE"]
            female = self.parts[f"SLOT{slot}_FAN_HALF_PROTOTYPE"]
            self.assertLess(overlap(male, female), .001)
            # Independent geometric probes inside the specified 0.3mm radial gap,
            # then inside the neighboring spigot and receiver walls.
            x_outer = cx + r["route_middle_width"] / 2
            y, z = r["joint_y"] + r["spigot_length"] / 2, z0 + r["route_middle_height"] / 2
            gap = box(x_outer - wall - r["radial_clearance"] + .05, y, z, .2, 1, 1)
            self.assertLess(overlap(male, gap), .001)
            self.assertLess(overlap(female, gap), .001)
            male_probe = box(x_outer - wall - r["radial_clearance"] - .5, y, z, .2, 1, 1)
            female_probe = box(x_outer - wall + .2, y, z, .2, 1, 1)
            self.assertAlmostEqual(overlap(male, male_probe), .2, places=5)
            self.assertAlmostEqual(overlap(female, female_probe), .2, places=5)

    def test_ducts_and_clamps_leave_blower_intake_clear(self):
        blower = [p for n, p in self.parts.items() if "BLOWER" in n and self.kinds[n] == "reservation"]
        self.assertTrue(blower)
        for n, shape in self.parts.items():
            if self.kinds[n] == "prototype":
                for keepout in blower:
                    self.assertLess(overlap(shape, keepout), .001, n)

    def test_exclusion_and_default_height_are_enforced_separately_from_body_cap(self):
        printer = deepcopy(self.config["printer"])
        printer["bed_xyz"] = [256, 256, 256]  # Relax project cap; machine limits still apply.
        report = placement_report({"xlen": 230, "ylen": 230, "zlen": 240}, printer)
        self.assertTrue(report["within_profile_volume"])
        self.assertTrue(report["intersects_cutter_exclusion"])
        self.assertFalse(report["placement_pass"])
        report = placement_report({"xlen": 120, "ylen": 120, "zlen": 251}, printer)
        self.assertFalse(report["within_profile_volume"])
        self.assertFalse(report["placement_pass"])
        report = placement_report({"xlen": 120, "ylen": 120, "zlen": 200}, self.config["printer"])
        self.assertTrue(report["placement_pass"])

    def test_invalid_joint_or_release_configuration_is_rejected(self):
        for mode in ("zero_clearance", "blocked_airway", "production", "missing_fan"):
            c = deepcopy(self.config)
            if mode == "zero_clearance":
                c["r02"]["radial_clearance"] = 0
            elif mode == "blocked_airway":
                c["r02"]["spigot_wall"] = 20
            elif mode == "production":
                c["production_ready"] = True
            else:
                del c["r02"]["fan_routes"]["4"]
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                validate_config(c)


if __name__ == "__main__":
    unittest.main()
