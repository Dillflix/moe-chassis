"""Build a separate, explicitly provisional X10DRG-Q layout study."""
from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source"))
from x10drg_q_r01.build import build

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "source/x10drg_q_r01/layout.json")
    parser.add_argument("--output", type=Path, default=ROOT / "build/x10drg-q-r01")
    args = parser.parse_args()
    build(args.config, args.output)
