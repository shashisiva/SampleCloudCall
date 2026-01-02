import streamlit as st
import pandas as pd


st.title("Dashboard")

data = [
    {"ID": "1", "Province" : "Western", "District": "Colombo", "Category": "Flooding"},
    {"ID": "2", "Province" : "Northern", "District": "Jaffna",  "Category": "Winds"},
]

df = pd.DataFrame(data)

st.dataframe(
    df
)

