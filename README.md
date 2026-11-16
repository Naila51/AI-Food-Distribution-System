# AI Food Distribution System

An AI-powered system for food surplus prediction, categorization, organization matching, and optimized food distribution.

## Project layout

- `app.py` — Streamlit entry point
- `modules/` — inventory, prediction, matching, distribution, and impact logic
- `models/` — surplus model train/load helpers
- `data/food_inventory.csv` — sample inventory used during development
- `notebooks/experiments.ipynb` — exploration notebook

## Setup

Requires Python 3.11 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

## Run the app

```powershell
streamlit run app.py
```

The UI opens at [http://localhost:8501](http://localhost:8501).

## Notebooks

```powershell
jupyter notebook notebooks/experiments.ipynb
```

## Next work

The Streamlit shell and inventory loader run today. Implement the remaining module stubs:

- `modules/surplus_prediction.py`
- `modules/food_categorization.py`
- `modules/organization_matching.py`
- `modules/distribution_recommendations.py`
- `models/surplus_model.py`
