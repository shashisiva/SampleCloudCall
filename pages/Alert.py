import streamlit as st
from storage import load_issues
import pandas as pd

st.title("Alert")

CATEGORIES = ["flood", "rain", "cyclone", "tsunami", "wind", "fire"]

PROVINCE_TO_DISTRICTS = {
    "Western": ["Colombo", "Gampaha", "Kalutara"],
    "Central": ["Kandy", "Matale", "Nuwara Eliya"],
    "Southern": ["Galle", "Matara", "Hambantota"],
    "Northern": ["Jaffna", "Kilinochchi", "Mannar", "Mullaitivu", "Vavuniya"],
    "Eastern": ["Trincomalee", "Batticaloa", "Ampara"],
    "North Western": ["Kurunegala", "Puttalam"],
    "North Central": ["Anuradhapura", "Polonnaruwa"],
    "Uva": ["Badulla", "Monaragala"],
    "Sabaragamuwa": ["Ratnapura", "Kegalle"],
}

# Province + Category (saved in session automatically via keys)
selected_provinces = st.multiselect(
    "Province",
    list(PROVINCE_TO_DISTRICTS.keys()),
    key="selected_provinces",
)

selected_categories = st.multiselect(
    "Category",
    CATEGORIES,
    key="selected_categories",
)

# District options depend on provinces
all_districts = sorted({d for ds in PROVINCE_TO_DISTRICTS.values() for d in ds})
if selected_provinces:
    district_options = sorted({d for p in selected_provinces for d in PROVINCE_TO_DISTRICTS[p]})
else:
    district_options = all_districts

# ✅ Keep previous districts if still valid (don’t wipe everything)
if "selected_districts" not in st.session_state:
    st.session_state["selected_districts"] = []

st.session_state["selected_districts"] = [
    d for d in st.session_state["selected_districts"] if d in district_options
]

selected_districts = st.multiselect(
    "District",
    district_options,
    key="selected_districts",
)

st.divider()

st.subheader("Send An Alert SMS Message")
phone = st.text_input("Phone number to alert (just for display)", value="")

if st.button("Send alert"):
    st.success("Alert sent: True")
    st.write("**To:**", phone if phone.strip() else "(no phone entered)")

