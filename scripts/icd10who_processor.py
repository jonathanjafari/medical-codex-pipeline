# icd-10 who processor
# this script loads the icd-10 who file, cleans it, validates codes,
# adds a timestamp, and saves it as csv

import pandas as pd
import logging
import sys, os
from pathlib import Path

# so python can find utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp


def load_icd10who_data(filepath: str) -> pd.DataFrame:
    # load the raw file (it is pipe-delimited, so we use sep="|")
    df = pd.read_csv(filepath, sep="|", dtype=str)
    logging.info(f"loaded {len(df)} icd-10 who records")
    return df


def clean_icd10who_data(df: pd.DataFrame) -> pd.DataFrame:
    # keep only code and description
    df = df[['code', 'description']].copy()

    # strip spaces and handle missing descriptions
    df['code'] = df['code'].str.strip().str.upper()
    df['description'] = df['description'].fillna("no description").str.strip()

    # validate: icd-10 who format like A00, B20, Z99.8
    df = df[df['code'].str.match(r'^[A-Z][0-9]{2}(\.[0-9A-Z]{1,4})?$')]

    # add last_updated column
    df['last_updated'] = get_timestamp()
    return df


def main():
    logging.basicConfig(level=logging.INFO)

    # input sample file
    input_file = Path("input/icd10who_sample.txt")

    # output cleaned file
    output_file = Path("output/csv/icd10who_cleaned")

    # run the steps
    raw = load_icd10who_data(input_file)
    clean = clean_icd10who_data(raw)
    save_to_formats(clean, output_file)


# run the script
if __name__ == "__main__":
    main()
