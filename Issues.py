import streamlit as st
import datetime as dt
import pandas as pd
from storage import add_issue, save_uploaded_image



st.title("📝 Disaster Issue Reporter")

category = st.selectbox(        "Category",
        ["flood", "rain", "cyclone", "tsunami", "other", "wind", "fire"]
    )

province_to_districts = {
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

province = st.selectbox("Province", list(province_to_districts.keys()))
district = st.selectbox("District", province_to_districts[province])

description = st.text_area(
        "Disaster Issue Description (max 100 characters)",
        max_chars=100,
        height=180,
    )

uploaded_file = st.file_uploader(
    "Upload Image", type=["jpg","jpeg","png","JPG","JPEG","PNG"]
)
if uploaded_file:
    st.image(uploaded_file)

    # Date/time (not in the future)
now = dt.datetime.now()
now_date = now.date()
now_time = now.time().replace(second=0, microsecond=0)

incident_date = st.date_input(
        "Incident Date",
        value=now_date,
        max_value=now_date,
        key="incident_date"
    )

incident_time = st.time_input(
        "Incident Time",
        value=now_time,
        key="incident_time"
    )

    # If today, block future time (auto-reset)
if st.session_state["incident_date"] == now_date and st.session_state["incident_time"] > now_time:
        st.warning("Time cannot be in the future for today's date. Resetting to current time.")
        st.session_state["incident_time"] = now_time

if st.button("Submit"):
        if not description.strip():
            st.error("Please enter an issue description.")
        else:
            incident_datetime = dt.datetime.combine(
                st.session_state["incident_date"],
                st.session_state["incident_time"]
            )

            if incident_datetime > now:
                st.error("Incident date/time cannot be in the future.")
            else:
                image_path = save_uploaded_image(uploaded_file)

                issue = {
                "id": dt.datetime.now().strftime("%Y%m%d%H%M%S"),  # simple id
                "category": category,
                "province": province,
                "district": district,
                "description": description.strip(),
                "incident_datetime": incident_datetime.isoformat(timespec="minutes"),
                "created_at": dt.datetime.now().isoformat(timespec="seconds"),
                "image_path": image_path,  # e.g. data/images/xxxx.png
            }

                add_issue(issue)

                st.success("Saved")
                st.write(issue)
