import streamlit as st
import pandas as pd
from storage import load_issues

st.title("Dashboard")

issues = load_issues()

if not issues:
    st.info("No issues.")
    st.stop()

df = pd.DataFrame(issues)
preferred_cols = [ "id", "province", "district", "category", "description", "created_at"]
cols = [c for c in preferred_cols if c in df.columns]
df = df[cols] if cols else df
st.dataframe(df, use_container_width=True)


# View Image
st.subheader("View Image")
ids = [x.get("id") for x in issues if x.get("id")]

selected_id = st.selectbox("Select Issue ID", ids)

selected = next((x for x in issues if x.get("id") == selected_id), None)

if selected:
    img_path = selected.get("image_path")
    if img_path:
        st.image(img_path, caption="Uploaded Image", use_container_width=True)
    else:
        st.caption("No image uploaded for this issue.")

