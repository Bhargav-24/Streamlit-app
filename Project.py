import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Dummy faculty credentials
FACULTY_CREDENTIALS = {"admin": "password123"}

# Dummy student list
students = {"101": "Alice", "102": "Bob", "103": "Charlie", "104": "David"}

def load_attendance():
    try:
        return pd.read_csv("attendance.csv", index_col=[0])
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Roll Number", "Name", "Status"])

def save_attendance(attendance_df):
    attendance_df.to_csv("attendance.csv")

def faculty_login():
    st.title("Faculty Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in FACULTY_CREDENTIALS and FACULTY_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def attendance_page():
    st.title("Attendance Management")
    attendance_df = load_attendance()
    
    # Date selection (no future dates)
    today = datetime.date.today()
    date = st.date_input("Select Date", today, min_value=datetime.date(2024, 1, 1), max_value=today)
    
    # Load previous attendance if available
    if date in attendance_df["Date"].values:
        existing_data = attendance_df[attendance_df["Date"] == str(date)]
    else:
        existing_data = pd.DataFrame(columns=["Roll Number", "Name", "Status"])
    
    st.subheader(f"Attendance for {date}")
    attendance = {}
    for roll, name in students.items():
        prev_status = existing_data[existing_data["Roll Number"] == roll]["Status"].values
        default_status = prev_status[0] if len(prev_status) > 0 else "Absent"
        attendance[roll] = st.selectbox(f"{roll} - {name}", ["Present", "Absent"], index=0 if default_status == "Present" else 1)
    
    if st.button("Submit Attendance"):
        # Remove existing entries for the selected date
        attendance_df = attendance_df[attendance_df["Date"] != str(date)]
        # Add new entries
        new_data = pd.DataFrame({"Date": date, "Roll Number": list(attendance.keys()), "Name": list(students.values()), "Status": list(attendance.values())})
        attendance_df = pd.concat([attendance_df, new_data], ignore_index=True)
        save_attendance(attendance_df)
        st.success("Attendance submitted successfully!")
        st.experimental_rerun()

def attendance_report():
    st.title("Attendance Report")
    attendance_df = load_attendance()
    
    if attendance_df.empty:
        st.warning("No attendance data available.")
        return
    
    attendance_df["Date"] = pd.to_datetime(attendance_df["Date"])
    
    # Attendance percentage calculation
    total_days = attendance_df["Date"].nunique()
    if total_days == 0:
        st.warning("No sufficient data for analysis.")
        return
    
    attendance_summary = attendance_df.groupby("Date")["Status"].apply(lambda x: (x == "Present").sum())
    
    st.subheader("Attendance Percentage")
    attendance_percentage = (attendance_summary / len(students)) * 100
    st.line_chart(attendance_percentage)
    
    # Graph of student attendance over days
    fig, ax = plt.subplots()
    ax.plot(attendance_summary.index, attendance_summary.values, marker='o', linestyle='-')
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Students Present")
    ax.set_title("Daily Attendance Trend")
    st.pyplot(fig)

# Sidebar Navigation
st.sidebar.title("Navigation")
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    faculty_login()
else:
    page = st.sidebar.radio("Go to", ["Take Attendance", "View Report", "Logout"])
    if page == "Take Attendance":
        attendance_page()
    elif page == "View Report":
        attendance_report()
    elif page == "Logout":
        st.session_state["logged_in"] = False
        st.experimental_rerun()
