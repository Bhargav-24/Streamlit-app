import streamlit as st
import pandas as pd
import datetime

# Set page config
st.set_page_config(page_title="Student Attendance System", layout="wide")

# Custom CSS for professional yellow & white theme
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #FFD700, #FFFACD);
        color: black;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #FFD700;
        color: black;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
    }
    .stDataFrame {
        background-color: white;
        color: black;
    }
    .stTextInput>div>div>input {
        border: 2px solid #FFD700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("📚 Student Attendance System")
st.write("Efficiently track student attendance in real-time.")

# Create or load attendance records
if "attendance_data" not in st.session_state:
    st.session_state.attendance_data = pd.DataFrame(columns=["Student ID", "Name", "Date", "Status"])

# Input fields for student info
student_id = st.text_input("Enter Student ID:")
student_name = st.text_input("Enter Student Name:")

# Attendance marking
col1, col2 = st.columns(2)
with col1:
    if st.button("✅ Mark Present"):
        if student_id and student_name:
            new_entry = pd.DataFrame([[student_id, student_name, datetime.date.today(), "Present"]],
                                     columns=["Student ID", "Name", "Date", "Status"])
            st.session_state.attendance_data = pd.concat([st.session_state.attendance_data, new_entry], ignore_index=True)
            st.success(f"✅ {student_name} marked Present!")
        else:
            st.error("Please enter Student ID and Name!")

with col2:
    if st.button("❌ Mark Absent"):
        if student_id and student_name:
            new_entry = pd.DataFrame([[student_id, student_name, datetime.date.today(), "Absent"]],
                                     columns=["Student ID", "Name", "Date", "Status"])
            st.session_state.attendance_data = pd.concat([st.session_state.attendance_data, new_entry], ignore_index=True)
            st.warning(f"❌ {student_name} marked Absent!")
        else:
            st.error("Please enter Student ID and Name!")

# Display Attendance Records
st.subheader("📋 Attendance Records")
st.dataframe(st.session_state.attendance_data, use_container_width=True)

# Export Attendance DataStrean
if st.button("📂 Export to CSV"):
    st.session_state.attendance_data.to_csv("attendance_records.csv", index=False)
    st.success("📂 Attendance data saved as CSV!")

# Remove unnecessary footer and menu
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
