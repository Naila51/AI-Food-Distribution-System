"""Load and save food inventory records."""

from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "food_inventory.csv"

REQUIRED_COLUMNS = (
    "item_id",
    "item_name",
    "category",
    "quantity_kg",
    "expiry_date",
    "location",
    "donor",
    "status",
)


class InventoryFormatError(ValueError):
    """Raised when an uploaded CSV does not match the inventory schema."""


def load_inventory(path: Path | str = DATA_PATH) -> pd.DataFrame:
    """Return inventory rows from the CSV file."""
    return pd.read_csv(path, parse_dates=["expiry_date"])


def save_inventory(df: pd.DataFrame, path: Path | str = DATA_PATH) -> None:
    """Write inventory rows back to the CSV file."""
    df.to_csv(path, index=False)


def inventory_from_upload(file) -> pd.DataFrame:
    """Parse an uploaded inventory CSV and validate required columns."""
    df = pd.read_csv(file, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise InventoryFormatError(
            "CSV is missing columns: "
            + ", ".join(missing)
            + ". Expected: "
            + ", ".join(REQUIRED_COLUMNS)
        )
    df["expiry_date"] = pd.to_datetime(df["expiry_date"], errors="coerce")
    df["quantity_kg"] = pd.to_numeric(df["quantity_kg"], errors="coerce")
    return df
