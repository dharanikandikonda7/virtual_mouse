import streamlit as st
import subprocess
import sys
import os

# Initialize process in session state
if "process" not in st.session_state:
    st.session_state.process = None


def start_finalvm():
    if st.session_state.process is None:
        # Camera permission
        if not st.session_state.camera_permission:
            st.warning("Camera access not allowed.")
            return
        st.session_state.process = subprocess.Popen(
            [sys.executable, "finalvm.py"],
            cwd=os.getcwd()
        )
        st.success("Virtual Gesture Controller started.")
    else:
        st.info("Virtual Gesture Controller is already running.")


def stop_finalvm():
    if st.session_state.process:
        st.session_state.process.terminate()
        st.session_state.process = None
        st.success("Virtual Gesture Controller stopped.")
    else:
        st.info("Virtual Gesture Controller is not running.")


def exit_app():
    stop_finalvm()
    st.stop()


# ---------------- UI ----------------
st.set_page_config(page_title="Virtual Gesture Controller", layout="centered")

st.title("Virtual Gesture Controller")

st.session_state.camera_permission = st.checkbox(
    "Allow camera access to start?"
)

st.button("Start", on_click=start_finalvm)
st.button("Stop", on_click=stop_finalvm)
st.button("Exit", on_click=exit_app)
