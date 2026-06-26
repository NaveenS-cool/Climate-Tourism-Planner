import streamlit as st

from ui.intro import show_intro
from ui.dashboard import show_dashboard


# SESSION STATE INITIALISATION
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "intro"

if "destination" not in st.session_state:
    st.session_state["destination"] = ""


# PAGE CONFIG (must be the first Streamlit command)

st.set_page_config(
    page_title="Climate Tourism Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ROUTER

if st.session_state["current_page"] == "intro":
    with st.container(key="intro_container"):
        show_intro()

elif st.session_state["current_page"] == "dashboard":
    with st.container(key="dashboard_container"):
        show_dashboard()
