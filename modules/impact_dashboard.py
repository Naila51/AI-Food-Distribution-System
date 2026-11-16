"""Summarize meals rescued, waste avoided, and other impact metrics."""

import pandas as pd


def summarize_impact(inventory: pd.DataFrame, distributions: pd.DataFrame | None = None) -> dict:
    """Return dashboard metrics derived from inventory and completed distributions."""
    meals_estimate = float(inventory["quantity_kg"].fillna(0).sum()) * 2.5
    return {
        "item_count": int(len(inventory)),
        "total_kg": float(inventory["quantity_kg"].fillna(0).sum()),
        "estimated_meals": round(meals_estimate, 1),
    }
