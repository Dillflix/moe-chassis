"""Regression checks for the layout findings and exported fit-sample geometry."""
from copy import deepcopy
from pathlib import Path
import json
import math
import sys
import tempfile
import unittest

import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source"))
from x10drg_q_r01.build import bounds, box, build, make_layout, mesh_report, overlap, validate_config
from fit_checks.psu_screw_seat_r01 import seat_sample


class LayoutRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_path = ROOT / "source/x10drg_q_r01/layout.json"
        cls.config = json.loads(cls.config_path.read_text())
        cls.layouts = {name: make_layout(cls.config, depth) for name, depth in
                       cls.config["chassis"]["variants"].items()}

    def cable_collisions(self, parts):
        return [(a, b) for a, p in parts.items() if "CABLE_RESERVATION" in a
                for b, q in parts.items() if b.startswith("DUCT_SLOT") and overlap(p, q) > .01]

    def test_extra_depth_resolves_the_two_identified_cable_collisions(self):
        self.assertEqual(len(self.cable_collisions(self.layouts["compact"][0])), 2)
        self.assertEqual(self.cable_collisions(self.layouts["extended"][0]), [])

    def test_deeper_psus_are_not_implicitly_declared_clear(self):
        config = deepcopy(self.config)
        config["psus"]["body_depth_x"] = 220
        parts, *_ = make_layout(config, config["chassis"]["variants"]["extended"])
        self.assertTrue(self.cable_collisions(parts))

    def test_collision_model_includes_fan_rotor_volume(self):
        parts, _, kinds, _ = self.layouts["extended"]
        fans = [p for name, p in parts.items() if kinds[name] == "fan_keepout"]
        self.assertEqual(len(fans), 10)
        for fan in fans:
            b = bounds(fan)
            rotor_obstruction = box((b["xmin"] + b["xmax"]) / 2 - 1,
                                    b["ymin"] + 1,
                                    (b["zmin"] + b["zmax"]) / 2 - 1, 2, 2, 2)
            self.assertAlmostEqual(overlap(fan, rotor_obstruction), 8)

    def test_anchor_coverage_changes_with_board_placement(self):
        self.assertTrue(self.layouts["extended"][3]["old_y350_duct_anchors_covered_by_board"])
        config = deepcopy(self.config)
        config["board"]["origin_xy"][1] = 0
        *_, datums = make_layout(config, config["chassis"]["variants"]["extended"])
        self.assertFalse(any(a["covered_by_board"] for a in datums["baseline_y350_duct_anchor_checks"]))

    def test_saved_mesh_reports_real_dimensions_after_tessellation(self):
        with tempfile.TemporaryDirectory() as directory:
            for label, length in (("compact", 240.6), ("extended", 290.6)):
                parts, _, kinds, _ = self.layouts[label]
                for name, shape in parts.items():
                    if kinds[name] != "concept_duct":
                        continue
                    shape = shape.rotate((0, 0, 0), (1, 0, 0), -90)
                    before = bounds(shape)
                    shape.tessellate(.06, .12)
                    self.assertEqual(before, bounds(shape))
                    shape = shape.translate(tuple(-before[k] for k in ("xmin", "ymin", "zmin")))
                    path = Path(directory) / f"{label}-{name}.stl"
                    cq.exporters.export(shape, str(path), tolerance=.06, angularTolerance=.12)
                    report = mesh_report(path)
                    for key in ("watertight_edges", "consistent_winding", "positive_signed_volume",
                                "on_bed", "nonnegative_coordinates"):
                        self.assertTrue(report[key], f"{label}/{name}: {key}")
                    self.assertAlmostEqual(report["bounds_mm"]["zlen"], length, places=3)
                    self.assertAlmostEqual(report["bounds_mm"]["ylen"], 240, places=3)

    def test_concept_cannot_silently_become_a_mounting_release(self):
        for key in ("production", "holes", "nvlink"):
            config = deepcopy(self.config)
            if key == "production":
                config["production_ready"] = True
            elif key == "holes":
                config["board"]["mounting_holes"] = [[0, 0]]
            else:
                config["gpus"]["nvlink"]["pairs"] = [[8, 4], [6, 2]]
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_config(config)

    def test_existing_build_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / "keep.txt"
            sentinel.write_text("prior output")
            with self.assertRaises(SystemExit):
                build(self.config_path, directory)
            self.assertEqual(sentinel.read_text(), "prior output")

    def test_psu_coupon_retains_specified_land_on_correct_face(self):
        # A probe in the screw-bearing annulus measures actual retained material.
        probe = cq.Solid.makeCylinder(.1, 6, cq.Vector(18, 15, 0))
        for thickness in (2, 5):
            sample = seat_sample(thickness)
            measured = sample.intersect(probe).Volume() / (math.pi * .1**2)
            self.assertAlmostEqual(measured, thickness, places=5)


if __name__ == "__main__":
    unittest.main()
