# rxnorm_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, save_to_formats, get_timestamp


def load_rxnorm_data(filepath: str) -> pd.DataFrame:
    """Load raw RxNorm data from RXNCONSO.RRF (pipe-delimited)."""
    cols = [
        "RXCUI","LAT","TS","LUI","STT","SUI","ISPREF","RXAUI",
        "SAUI","SCUI","SDUI","SAB","TTY","CODE","STR","SRL",
        "SUPPRESS","CVF"
    ]
    df = pd.read_csv(filepath, sep="|", header=None, dtype=str, engine="python")

    # Drop trailing empty col if present
    if df.shape[1] > len(cols):
        df = df.iloc[:, :len(cols)]

    df.columns = cols
    return df


def clean_rxnorm_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize RxNorm codes."""
    df = raw[(raw["LAT"] == "ENG") & (raw["SAB"] == "RXNORM")].copy()

    # Keep only RXCUI and STR
    df = df.rename(columns={"RXCUI": "code", "STR": "description"})
    df = df[["code", "description"]].dropna().drop_duplicates()

    # Strip whitespace
    df.loc[:, "code"] = df["code"].str.strip()
    df.loc[:, "description"] = df["description"].str.strip()

    # Add last_updated
    if not df.empty:
        df.loc[:, "last_updated"] = get_timestamp()

    return df


def main() -> None:
    import logging
    init_logging()

    raw = load_rxnorm_data("input/RXNCONSO.RRF")
    clean = clean_rxnorm_data(raw)
    save_to_formats(clean, "output/csv/rxnorm_standardized")

    logging.info("RxNorm processing completed.")


if __name__ == "__main__":
    main()
