# rxnorm_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, validate_code_format, save_to_formats


def load_rxnorm_data(filepath: str) -> pd.DataFrame:
    """Load raw RxNorm data file."""
    return pd.read_csv(filepath, dtype=str)


def clean_rxnorm_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize RxNorm codes."""
    df = raw.dropna(subset=["code", "description"]).copy()
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()
    df = df.drop_duplicates()
    df["is_valid"] = df["code"].apply(lambda c: validate_code_format(c, "rxnorm"))
    return df


def main() -> None:
    import logging
    init_logging()

    raw = load_rxnorm_data("input/rxnorm_2024.txt")
    clean = clean_rxnorm_data(raw)
    save_to_formats(clean, "output/csv/rxnorm_standardized")

    logging.info("RxNorm processing completed.")


if __name__ == "__main__":
    main()
