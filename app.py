from pathlib import Path

import pandas as pd
import streamlit as st

from modules.food_inventory import (
    REQUIRED_COLUMNS,
    InventoryFormatError,
    inventory_from_upload,
    load_inventory,
    save_inventory,
)
from modules.impact_dashboard import summarize_impact

st.set_page_config(page_title="FoodLoop AI", page_icon="🥗", layout="wide")

_THEME_CSS = Path(__file__).with_name("static") / "quayside.css"
if _THEME_CSS.exists():
    st.markdown(f"<style>{_THEME_CSS.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

st.title("FoodLoop AI")
st.caption("Surplus prediction, categorization, organization matching, and distribution.")

page = st.sidebar.radio(
    "Module",
    [
        "Inventory",
        "Surplus prediction",
        "Food categorization",
        "Organization matching",
        "Distribution recommendations",
        "Impact",
    ],
)


def current_inventory() -> pd.DataFrame:
    if "inventory" not in st.session_state:
        try:
            st.session_state["inventory"] = load_inventory()
        except FileNotFoundError:
            st.session_state["inventory"] = pd.DataFrame()
    return st.session_state["inventory"]


inventory = current_inventory()

if page == "Inventory":
    st.subheader("Food inventory")
    uploaded = st.file_uploader(
        "Upload CSV",
        type=["csv"],
        help="Use the inventory template columns listed below.",
    )
    st.caption("Required columns: " + ", ".join(REQUIRED_COLUMNS))

    if uploaded is not None:
        file_key = (uploaded.name, uploaded.size)
        if st.session_state.get("_upload_key") != file_key:
            try:
                uploaded.seek(0)
                uploaded_inventory = inventory_from_upload(uploaded)
                st.session_state["inventory"] = uploaded_inventory
                st.session_state["_upload_key"] = file_key
                save_inventory(uploaded_inventory)
                st.session_state["_upload_message"] = (
                    f"Uploaded {len(uploaded_inventory)} items from {uploaded.name}"
                )
                st.session_state["_upload_error"] = None
            except InventoryFormatError as error:
                st.session_state["_upload_error"] = str(error)
                st.session_state["_upload_message"] = None
            except (OSError, UnicodeDecodeError, pd.errors.ParserError, ValueError) as error:
                st.session_state["_upload_error"] = f"Could not read that CSV: {error}"
                st.session_state["_upload_message"] = None

        inventory = current_inventory()

    if st.session_state.get("_upload_error"):
        st.error(st.session_state["_upload_error"])
    elif st.session_state.get("_upload_message"):
        st.success(st.session_state["_upload_message"])

    if inventory.empty:
        st.info("Upload a CSV or add rows to data/food_inventory.csv to get started.")
    else:
        st.dataframe(inventory, width="stretch")
elif page == "Impact":
    st.subheader("Impact")
    metrics = summarize_impact(inventory)
    col1, col2, col3 = st.columns(3)
    col1.metric("Items", metrics["item_count"])
    col2.metric("Total kg", f"{metrics['total_kg']:.1f}")
    col3.metric("Estimated meals", metrics["estimated_meals"])
else:
    st.subheader(page)
    st.info(
        f"{page} is scaffolded and ready to implement. "
        "See the matching file in modules/ or models/."
    )
    if not inventory.empty:
        st.dataframe(inventory.head(), width="stretch")
