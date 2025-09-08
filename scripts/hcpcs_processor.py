# hcpcs processor
# this script loads the hcpcs file, cleans it, validates codes,
# adds a timestamp, and saves it as csv

import pandas as pd
import logging
import sys, os
from pathlib import Path

# so python can find utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp


def load_hcpcs_data(filepath: str) -> pd.DataFrame:
    # load the raw hcpcs file (pipe-delimited)
    df = pd.read_csv(filepath, sep="|", dtype=str)
    logging.info(f"loaded {len(df)} hcpcs records")
    return df


def clean_hcpcs_data(df: pd.DataFrame) -> pd.DataFrame:
    # keep only code and description
    df = df[['code', 'description']].copy()

    # strip spaces and fill missing
    df['code'] = df['code'].str.strip().str.upper()
    df['description'] = df['description'].fillna("no description").str.strip()

    # validate: hcpcs codes are 5 characters (letter A–V + 4 digits)
    df = df[df['code'].str.match(r'^[A-V][0-9]{4}$')]

    # add last_updated column
    df['last_updated'] = get_timestamp()
    return df


def main():
    logging.basicConfig(level=logging.INFO)

    # input sample file
    input_file = Path("input/hcpcs_sample.txt")

    # output cleaned file
    output_file = Path("output/csv/hcpcs_cleaned")

    # run the steps
    raw = load_hcpcs_data(input_file)
    clean = clean_hcpcs_data(raw)
    save_to_formats(clean, output_file)


# run the script
if __name__ == "__main__":
    main()
