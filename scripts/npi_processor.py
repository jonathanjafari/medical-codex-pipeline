# npi processor
# this script loads the npi file, cleans it, checks that codes are valid,
# adds a timestamp, and saves the result as a csv

import pandas as pd
import logging
import sys, os
from pathlib import Path

# so python can find the utils folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.common_functions import save_to_formats, get_timestamp


def load_npi_data(filepath: str) -> pd.DataFrame:
    # load the raw npi data
    df = pd.read_csv(filepath, dtype=str)
    logging.info(f"loaded {len(df)} npi records")
    return df


def clean_npi_data(df: pd.DataFrame) -> pd.DataFrame:
    # keep only code and description
    df = df[['NPI', 'Provider Organization Name (Legal Business Name)']].copy()
    df.rename(columns={'NPI': 'code', 
                       'Provider Organization Name (Legal Business Name)': 'description'}, inplace=True)

    # strip spaces and fill missing descriptions
    df['code'] = df['code'].str.strip()
    df['description'] = df['description'].fillna("no description").str.strip()

    # validate: npi must be 10 digits
    df = df[df['code'].str.match(r'^\d{10}$')]

    # add last_updated timestamp
    df['last_updated'] = get_timestamp()
    return df


def main():
    logging.basicConfig(level=logging.INFO)

    # input file (sample)
    input_file = Path("input/npidata_sample.csv")

    # output file
    output_file = Path("output/csv/npi_cleaned")

    raw = load_npi_data(input_file)
    clean = clean_npi_data(raw)
    save_to_formats(clean, output_file)


# only run main if this file is executed directly
if __name__ == "__main__":
    main()

