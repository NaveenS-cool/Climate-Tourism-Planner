import streamlit as st

from ui.intro import show_intro

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
    show_intro()

elif st.session_state["current_page"] == "dashboard":
    # Placeholder: the Dashboard page will be built in a future module.
    st.markdown(
        f"""
        <div style="display:flex;flex-direction:column;align-items:center;
                     justify-content:center;min-height:80vh;text-align:center;
                     font-family:'Segoe UI',sans-serif;">
            <h1 style="color:#2d6a4f;">🌍 Dashboard</h1>
            <p style="color:#555;font-size:1.2rem;max-width:500px;">
                Planning trip to <strong>{st.session_state['destination']}</strong>.
                <br>The dashboard will be built next.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("← Back to start"):
        st.session_state["current_page"] = "intro"
        st.rerun()
