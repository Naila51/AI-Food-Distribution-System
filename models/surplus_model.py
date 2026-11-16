"""Train, persist, and load the surplus prediction model."""

from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent / "surplus_model.pkl"


def train(dataset, path: Path | str = MODEL_PATH):
    """Fit a surplus model and save it to disk."""
    raise NotImplementedError


def load(path: Path | str = MODEL_PATH):
    """Load a trained surplus model."""
    raise NotImplementedError
