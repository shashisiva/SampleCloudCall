import streamlit as st

dashboard = st.Page("pages/Dashboard.py", title="Dashboard", default=True, icon="📊")
alert     = st.Page("pages/Alert.py", title="Alert An Issue")
about     = st.Page("pages/About.py", title="About This Application")
issues     = st.Page("pages/Issues.py", title="Report A Disaster Issue")

pg = st.navigation([dashboard, alert,issues, about ])
pg.run()