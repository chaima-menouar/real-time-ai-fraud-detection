import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.processing.data_splitter import clean_dataframe, save_splits


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean and split a private labelled dataset")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    raw = pd.read_csv(args.input)
    cleaned = clean_dataframe(raw)
    save_splits(cleaned, args.output_dir)
    print(f"Prepared {len(cleaned)} unique examples in {args.output_dir}")


if __name__ == "__main__":
    main()
