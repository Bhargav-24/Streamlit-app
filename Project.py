import streamlit as st
import pandas as pd
import datetime
import altair as alt
import calendar

# Dummy faculty credentials
FACULTY_CREDENTIALS = {"admin": "password123"}

# 25 students with Indian names: roll number mapped to name
students = {
    "101": "Aarav", "102": "Aditi", "103": "Akhil", "104": "Ananya", "105": "Arjun",
    "106": "Bhavya", "107": "Chirag", "108": "Diya", "109": "Esha", "110": "Farhan",
    "111": "Gaurav", "112": "Himani", "113": "Ishaan", "114": "Jhanvi", "115": "Kiran",
    "116": "Lavanya", "117": "Manav", "118": "Nidhi", "119": "Omkar", "120": "Pranav",
    "121": "Riya", "122": "Sakshi", "123": "Tanmay", "124": "Utkarsh", "125": "Vanya"
}

DATA_FILE = "attendance.csv"


def load_attendance():
    try:
        return pd.read_csv(DATA_FILE, index_col=[0])
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Roll Number", "Name", "Status"])


def save_attendance(attendance_df):
    attendance_df.to_csv(DATA_FILE)


def faculty_login():
    st.markdown("<h1 style='text-align: center;'>Faculty Login</h1>", unsafe_allow_html=True)
    st.subheader("Please provide your credentials to continue.")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_button"):
        if username in FACULTY_CREDENTIALS and FACULTY_CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid username or password. Please try again.")


def initialize_attendance_state(date_str):
    attendance_df = load_attendance()
    if date_str in attendance_df["Date"].values:
        existing = attendance_df[attendance_df["Date"] == date_str]
        for roll in students.keys():
            if roll in existing["Roll Number"].astype(str).values:
                st.session_state[f"attendance_{roll}"] = \
                    existing[existing["Roll Number"].astype(str) == roll]["Status"].values[0]
            else:
                st.session_state[f"attendance_{roll}"] = "Unmarked"
    else:
        for roll in students.keys():
            st.session_state[f"attendance_{roll}"] = "Unmarked"


def attendance_page():
    st.title("Take Attendance")
    attendance_df = load_attendance()

    today = datetime.date.today()
    date = st.date_input("Select Date", today, min_value=datetime.date(2024, 1, 1), max_value=today,
                         key="attendance_date")
    date_str = str(date)

    if "last_date" not in st.session_state or st.session_state.get("last_date") != date_str:
        initialize_attendance_state(date_str)
        st.session_state["last_date"] = date_str

    st.subheader(f"Attendance for {date_str}")

    # Display each student with unique widget keys
    for roll, name in students.items():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**{roll} - {name}**")
            st.write(f"Current Status: **{st.session_state.get(f'attendance_{roll}', 'Unmarked')}**")
        with col2:
            if st.button("Present", key=f"{roll}_present_button"):
                st.session_state[f"attendance_{roll}"] = "Present"
                st.rerun()
        with col3:
            if st.button("Absent", key=f"{roll}_absent_button"):
                st.session_state[f"attendance_{roll}"] = "Absent"
                st.rerun()

    # Add vertical spacing before the button
    st.markdown("<br>", unsafe_allow_html=True)

    # Center and enlarge the submit button with extra spacing
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Submit Attendance", key="submit_attendance_button", help="Click to submit attendance"):
            attendance_df = attendance_df[attendance_df["Date"] != date_str]
            new_records = []
            for roll, name in students.items():
                new_records.append({
                    "Date": date_str,
                    "Roll Number": roll,
                    "Name": name,
                    "Status": st.session_state.get(f"attendance_{roll}", "Unmarked")
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
        today_data["Roll Number"] = today_data["Roll Number"].astype(str)
        df = pd.DataFrame({"Roll Number": list(students.keys()), "Name": list(students.values())})
        df["Roll Number"] = df["Roll Number"].astype(str)
        df = df.merge(today_data[["Roll Number", "Status"]], on="Roll Number", how="left")
        df["Status"] = df["Status"].fillna("Unmarked")
        df.insert(0, "S No.", range(1, len(df) + 1))
        df.set_index("S No.", inplace=True)
        st.table(df)


def attendance_report():
    st.title("Attendance Report")
    attendance_df = load_attendance()

    if attendance_df.empty:
        st.warning("No attendance data available.")
        return

    attendance_df["Date"] = pd.to_datetime(attendance_df["Date"])
    attendance_df["Month"] = attendance_df["Date"].dt.strftime("%Y-%m")
    attendance_df["Day"] = attendance_df["Date"].dt.day

    # Create a dropdown with all months of the current year (by name)
    current_year = datetime.date.today().year
    month_options = {calendar.month_name[i]: f"{current_year}-{i:02d}" for i in range(1, 13)}
    selected_month_name = st.selectbox("Select Month:", list(month_options.keys()), key="report_month_selector")
    selected_month = month_options[selected_month_name]

    # Filter data for the selected month
    monthly_data = attendance_df[attendance_df["Month"] == selected_month]

    # Get the number of days in the selected month
    month_num = int(selected_month.split("-")[1])
    last_day = calendar.monthrange(current_year, month_num)[1]

    # Create a complete day range DataFrame for the month
    days_df = pd.DataFrame({"Day": list(range(1, last_day + 1))})

    # Calculate present count per day from available data
    summary = monthly_data.groupby("Day")["Status"].apply(lambda x: (x == "Present").sum()).reset_index()
    # Merge with complete days to ensure days with no data show 0
    days_df = days_df.merge(summary, on="Day", how="left")
    days_df["Status"].fillna(0, inplace=True)
    days_df["Status"] = days_df["Status"].astype(int)

    # Create an ordinal string for each day (e.g., 1st, 2nd, etc.)
    def ordinal(n):
        return f"{n}{'st' if n % 10 == 1 and n != 11 else 'nd' if n % 10 == 2 and n != 12 else 'rd' if n % 10 == 3 and n != 13 else 'th'}"

    days_df["Day_Ordinal"] = days_df["Day"].apply(ordinal)

    st.subheader(f"Daily Attendance for {selected_month_name} {current_year}")

    total_students = len(students)

    # Build an Altair line chart using the complete day range
    chart = alt.Chart(days_df).mark_line(point=True).encode(
        x=alt.X("Day_Ordinal:N", title="Day of the Month", sort=days_df["Day"].tolist()),
        y=alt.Y("Status:Q", title="Number of Students", scale=alt.Scale(domain=(0, total_students))),
        tooltip=["Day", "Day_Ordinal", "Status"]
    ).properties(
        title=f"Attendance Report for {selected_month_name} {current_year}",
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)


# Session state initialization for login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Main flow
if not st.session_state["logged_in"]:
    faculty_login()
else:
    st.sidebar.markdown(
        "<h1 style='text-align: center; color: royalblue; margin-top: -10px;'>Dashboard</h1>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

    page = st.sidebar.radio("Navigation", ["Take Attendance", "Today's Attendance", "View Report"], key="sidebar_nav")
    if page == "Take Attendance":
        attendance_page()
    elif page == "Today's Attendance":
        todays_attendance_page()
    elif page == "View Report":
        attendance_report()
    if st.sidebar.button("Logout", key="logout_button"):
        st.session_state["logged_in"] = False
        st.rerun()
