import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Dummy faculty credentials
FACULTY_CREDENTIALS = {"admin": "password123"}

# Dummy student list: roll number mapped to name
students = {"101": "Alice", "102": "Bob", "103": "Charlie", "104": "David"}

DATA_FILE = "attendance.csv"

def load_attendance():
    try:
        return pd.read_csv(DATA_FILE, index_col=[0])
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Roll Number", "Name", "Status"])

def save_attendance(attendance_df):
    attendance_df.to_csv(DATA_FILE)

def faculty_login():
    st.title("Faculty Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in FACULTY_CREDENTIALS and FACULTY_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid username or password")

def initialize_attendance_state(date_str):
    attendance_df = load_attendance()
    if date_str in attendance_df["Date"].values:
        existing = attendance_df[attendance_df["Date"] == date_str]
        for roll in students.keys():
            if roll in existing["Roll Number"].astype(str).values:
                st.session_state[f"attendance_{roll}"] = existing[existing["Roll Number"].astype(str) == roll]["Status"].values[0]
            else:
                st.session_state[f"attendance_{roll}"] = "Unmarked"
    else:
        for roll in students.keys():
            st.session_state[f"attendance_{roll}"] = "Unmarked"

def attendance_page():
    st.title("Take Attendance")
    attendance_df = load_attendance()

    today = datetime.date.today()
    date = st.date_input("Select Date", today, min_value=datetime.date(2024, 1, 1), max_value=today)
    date_str = str(date)

    if "last_date" not in st.session_state or st.session_state.get("last_date") != date_str:
        initialize_attendance_state(date_str)
        st.session_state["last_date"] = date_str

    st.subheader(f"Attendance for {date_str}")

    for roll, name in students.items():
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            st.write(f"**{roll} - {name}**")
            st.write(f"Current Status: **{st.session_state[f'attendance_{roll}']}**")
        with col2:
            if st.button("Mark Present", key=f"{roll}_present"):
                st.session_state[f"attendance_{roll}"] = "Present"
                st.rerun()
        with col3:
            if st.button("Mark Absent", key=f"{roll}_absent"):
                st.session_state[f"attendance_{roll}"] = "Absent"
                st.rerun()

    if st.button("Submit Attendance"):
        attendance_df = attendance_df[attendance_df["Date"] != date_str]
        new_records = []
        for roll, name in students.items():
            new_records.append({
                "Date": date_str,
                "Roll Number": roll,
                "Name": name,
                "Status": st.session_state[f"attendance_{roll}"]
            })
        new_df = pd.DataFrame(new_records)
        attendance_df = pd.concat([attendance_df, new_df], ignore_index=True)
        save_attendance(attendance_df)
        st.success("Attendance submitted successfully!")
        st.rerun()

def todays_attendance_page():
    st.title("Today's Attendance")
    attendance_df = load_attendance()
    today_str = str(datetime.date.today())
    today_data = attendance_df[attendance_df["Date"] == today_str].copy()
    
    if today_data.empty:
        st.info("No attendance data for today.")
    else:
        # Ensure that Roll Number is string type in both DataFrames
        today_data["Roll Number"] = today_data["Roll Number"].astype(str)
        df = pd.DataFrame({"Roll Number": list(students.keys()), "Name": list(students.values())})
        df["Roll Number"] = df["Roll Number"].astype(str)
        df = df.merge(today_data[["Roll Number", "Status"]], on="Roll Number", how="left")
        df["Status"] = df["Status"].fillna("Unmarked")
        st.table(df)

def attendance_report():
    st.title("Attendance Report")
    attendance_df = load_attendance()

    if attendance_df.empty:
        st.warning("No attendance data available.")
        return

    attendance_df["Date"] = pd.to_datetime(attendance_df["Date"])
    summary = attendance_df.groupby("Date")["Status"].apply(lambda x: (x == "Present").sum())
    
    st.subheader("Daily Attendance Overview")
    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(summary.index, summary.values, color="skyblue")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Students Present")
    ax.set_title("Daily Attendance")
    st.pyplot(fig)

st.sidebar.markdown("<h1 style='text-align: center; color: #4CAF50;'>Dashboard</h1>", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    faculty_login()
else:
    page = st.sidebar.radio("Navigation", ["Take Attendance", "Today's Attendance", "View Report", "Logout"])
    if page == "Take Attendance":
        attendance_page()
    elif page == "Today's Attendance":
        todays_attendance_page()
    elif page == "View Report":
        attendance_report()
    elif page == "Logout":
        st.session_state["logged_in"] = False
        st.rerun()
