import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.common_functions import init_logging, validate_code_format, save_to_formats, get_timestamp


def load_snomed_data(filepath: str) -> pd.DataFrame:
    """
    Load raw SNOMED CT description file (tab-delimited).
    The SCT2 file has many columns; we only need id and term.
    """
    # The SCT2 description files are tab-delimited with headers
    cols = ["id", "effectiveTime", "active", "moduleId", "conceptId",
            "languageCode", "typeId", "term", "caseSignificanceId"]

    return pd.read_csv(filepath, sep="\t", names=cols, header=0, dtype=str)


def clean_snomed_data(raw: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize SNOMED CT codes.
    We map conceptId → code and term → description.
    """
    df = raw.rename(columns={"conceptId": "code", "term": "description"}).copy()
    df = df.dropna(subset=["code", "description"])
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()
    df = df.drop_duplicates(subset=["code", "description"])
    df = df[["code", "description"]]
    return df


def main() -> None:
    import logging
    init_logging()

    try:
        raw = load_snomed_data("input/sct2_Description_Full-en_US1000124_20250901.txt")
        clean = clean_snomed_data(raw)
        save_to_formats(clean, "output/csv/snomed_standardized")

        logging.info("SNOMED CT processing completed.")
    except Exception as e:
        logging.error(f"SNOMED CT processing failed: {e}")


if __name__ == "__main__":
    main()
