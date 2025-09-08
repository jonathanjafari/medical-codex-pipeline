# loinc processor
# this script loads loinc file, cleans data, validates codes,
# adds timestamp, and saves to csv

import pandas as pd
import logging
import sys, os
from pathlib import Path

# so python can find utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp


def load_loinc_data(filepath: str) -> pd.DataFrame:
    # load the raw loinc csv
    df = pd.read_csv(filepath, dtype=str)
    logging.info(f"loaded {len(df)} loinc records")
    return df


def clean_loinc_data(df: pd.DataFrame) -> pd.DataFrame:
    # keep only code and description
    df = df[['code', 'description']].copy()

    # strip spaces and fill missing
    df['code'] = df['code'].str.strip()
    df['description'] = df['description'].fillna("no description").str.strip()

    # validate: loinc format like 1234-5
    df = df[df['code'].str.match(r'^\d{1,5}-\d$')]

    # add last_updated column
    df['last_updated'] = get_timestamp()
    return df


def main():
    logging.basicConfig(level=logging.INFO)

    input_file = Path("input/loinc_sample.csv")
    output_file = Path("output/csv/loinc_cleaned")

    raw = load_loinc_data(input_file)
    clean = clean_loinc_data(raw)
    save_to_formats(clean, output_file)


if __name__ == "__main__":
    main()

