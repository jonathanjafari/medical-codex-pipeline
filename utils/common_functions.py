import pandas as pd
import logging
from datetime import datetime

def save_to_formats(df: pd.DataFrame, base_filename: str) -> None:
    """Save DataFrame to CSV format"""
    try:
        df.to_csv(f"{base_filename}.csv", index=False)
        logging.info(f"Saved {base_filename}.csv")
    except Exception as e:
        logging.error(f"Error saving file: {e}")

def get_timestamp() -> str:
    """Return current UTC timestamp"""
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

