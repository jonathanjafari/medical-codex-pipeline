# icd-10-cm processor
# this script loads the icd-10-cm file, cleans it, validates codes,
# adds a timestamp, and saves as csv

import pandas as pd
import logging
import sys, os
from pathlib import Path

# so python can find utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp


def load_icd10cm_data(filepath: str) -> pd.DataFrame:
    # load raw file (pipe-delimited)
    df = pd.read_csv(filepath, sep="|", dtype=str)
    logging.info(f"loaded {len(df)} icd-10-cm records")
    return df


def clean_icd10cm_data(df: pd.DataFrame) -> pd.DataFrame:
    # keep only code and description
    df = df[['code', 'description']].copy()

    # strip spaces and fix missing
    df['code'] = df['code'].str.strip().str.upper()
    df['description'] = df['description'].fillna("no description").str.strip()

    # validate: icd-10 format like A00, Z99.2
    df = df[df['code'].str.match(r'^[A-Z][0-9]{2}(\.[0-9A-Z]{1,4})?$')]

    # add timestamp
    df['last_updated'] = get_timestamp()
    return df


def main():
    logging.basicConfig(level=logging.INFO)

    input_file = Path("input/icd10cm_sample.txt")
    output_file = Path("output/csv/icd10cm_cleaned")

    raw = load_icd10cm_data(input_file)
    clean = clean_icd10cm_data(raw)
    save_to_formats(clean, output_file)


if __name__ == "__main__":
    main()

