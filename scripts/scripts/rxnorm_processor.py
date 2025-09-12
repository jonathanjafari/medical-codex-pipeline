# rxnorm_processor.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, save_to_formats

def load_rxnorm_data(filepath: str) -> pd.DataFrame:
    """Load RxNorm RXNCONSO.RRF file (pipe-delimited, no header)."""
    df = pd.read_csv(
        filepath,
        sep="|",
        header=None,          # don’t assume exact column names
        dtype=str,
        engine="python",
        on_bad_lines="skip"
    )
    # According to RxNorm docs: RXCUI = column 0, STR = column 14
    df = df[[0, 14]].rename(columns={0: "code", 14: "description"})
    return df

def clean_rxnorm_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize RxNorm codes."""
    df = raw.dropna(subset=["code", "description"]).copy()
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()
    df = df.drop_duplicates()
    return df[["code", "description"]]

def main() -> None:
    import logging
    init_logging()

    try:
        raw = load_rxnorm_data("input/RXNCONSO.RRF")
        clean = clean_rxnorm_data(raw)
        save_to_formats(clean, "output/csv/rxnorm_standardized")
        logging.info("RxNorm processing completed.")
    except Exception as e:
        logging.error(f"RxNorm processing failed: {e}")

if __name__ == "__main__":
    main()
