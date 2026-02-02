import streamlit as st
from datetime import date
from database import *
from datetime import date, timedelta

import streamlit as st
st.write("App Loaded Successfully. WELCOME TO YOUR TO-DO APP!")


# ---------------- INITIAL SETUP ----------------
st.set_page_config(page_title="📝DoItNow To-Do App", layout="centered")

create_users_table()
create_table()

if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- HELPER FUNCTION ----------------
def get_due_status(due_date):
    today = date.today()
    due = date.fromisoformat(due_date)

    if due < today:
        return "❌ Overdue"
    elif due == today:
        return "⚠️ Due Today"
    else:
        return "✅ On Track"

# ---------------- TIME FORMATTER ----------------
def format_time(seconds):
    if seconds is None:
        return "0m 0s"

    minutes = seconds // 60
    seconds = seconds % 60
    return f"{int(minutes)}m {int(seconds)}s"


# ---------------- LOGIN / SIGNUP ----------------
st.title("📝 DoItNow To-Do List App")

menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

if st.session_state.user is None:

    if menu == "Login":
        st.subheader("🔐 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.user = user
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    elif menu == "Signup":
        st.subheader("🆕 Create Account")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Register"):
            if new_user.strip() == "" or new_pass.strip() == "":
                st.warning("All fields are required")
            elif register_user(new_user, new_pass):
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists")


# ---------------- MAIN TODO APP ----------------
else:
    user_id = st.session_state.user[0]
    username = st.session_state.user[1]

    st.sidebar.success(f"Logged in as {username}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    st.subheader("➕ Add New Task")

    task_title = st.text_input("Task Title")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    due_date = st.date_input("Due Date", min_value=date.today())

    if st.button("Add Task"):
        if task_title.strip() == "":
            st.warning("Task title cannot be empty")
        else:
            add_task(user_id, task_title, priority, str(due_date))
            st.success("Task added successfully!")
            st.rerun()

    st.divider()
    st.subheader("📋 Your Tasks")

    tasks = get_tasks(user_id)

    if not tasks:
        st.info("No tasks found. Start adding some!")
    else:
        for task in tasks:
            task_id, _, title, priority, status, due_date, time_spent, timer_start = task
            reminder = get_due_status(due_date)

            col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 2, 2])

            col1.write(f"**{title}**")
            col2.write(priority)
            col3.write(status)
            col4.write(reminder)
            col5.write(format_time(time_spent))

            # ---- TIMER BUTTONS ----
            if timer_start is None:
                if col6.button("▶ Start", key=f"start_{task_id}"):
                    start_timer(task_id)
                    st.rerun()
            else:
                if col6.button("⏹ Stop", key=f"stop_{task_id}"):
                    stop_timer(task_id)
                    st.rerun()

            # ---- STATUS BUTTON ----
            if status == "Pending":
                if st.button("✅ Mark Done", key=f"done_{task_id}"):
                    update_status(task_id, "Completed")
                    st.rerun()
            else:
                if st.button("🗑 Delete", key=f"delete_{task_id}"):
                    delete_task(task_id)
                    st.rerun()

            # ---- ALERTS ----
            if reminder == "❌ Overdue":
                st.error("This task is overdue!")
            elif reminder == "⚠️ Due Today":
                st.warning("Task is due today!")

            st.divider()

# FOOTER
st.markdown("---")
st.markdown("Developed by GARVIT RASTOGI | [GitHub](https://github.com/GarvitRastogi978) | [LinkedIn](https://www.linkedin.com/in/garvit-rastogi/)")
st.write("Thank You ❤️ for using DoItNow To-Do App!")

