# rxnorm processor
# this script loads the rxnorm file, cleans it, validates codes,
# adds a timestamp, and saves as csv

import pandas as pd
import logging
import sys, os
from pathlib import Path

# so python can find utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp


def load_rxnorm_data(filepath: str) -> pd.DataFrame:
    # load the raw rxnorm csv
    df = pd.read_csv(filepath, dtype=str)
    logging.info(f"loaded {len(df)} rxnorm records")
    return df


def clean_rxnorm_data(df: pd.DataFrame) -> pd.DataFrame:
    # keep only code and description
    df = df[['code', 'description']].copy()

    # strip spaces and fill missing
    df['code'] = df['code'].str.strip()
    df['description'] = df['description'].fillna("no description").str.strip()

    # validate: rxnorm codes are numeric only
    df = df[df['code'].str.match(r'^\d+$')]

    # add last_updated column
    df['last_updated'] = get_timestamp()
    return df


def main():
    logging.basicConfig(level=logging.INFO)

    input_file = Path("input/rxnorm_sample.csv")
    output_file = Path("output/csv/rxnorm_cleaned")

    raw = load_rxnorm_data(input_file)
    clean = clean_rxnorm_data(raw)
    save_to_formats(clean, output_file)


if __name__ == "__main__":
    main()
