"""Build small R01 PSU screw-seat fit coupons, not complete mounting plates."""
from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source/fit_checks"))
from psu_screw_seat_r01 import build


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build/psu-fit-r01")
    args = parser.parse_args()
    build(args.output)
