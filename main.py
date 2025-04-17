import streamlit as st
from datetime import date
import json

# User data file
USER_DATA_FILE = "user_data.json"

# Load user data
def load_users():
    try:
        with open(USER_DATA_FILE, "r") as file:
            users = json.load(file)
            for user in users:
                if "start_date" in users[user] and users[user]["start_date"]:
                    users[user]["start_date"] = date.fromisoformat(users[user]["start_date"])
            return users
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save user data
def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        users_serializable = {
            user: {**data, "start_date": str(data["start_date"]) if "start_date" in data and data["start_date"] else None}
            for user, data in users.items()
        }
        json.dump(users_serializable, file, indent=4)

# Initialize user database
users = load_users()

# Login function
def login():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user_data = users[username]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Incorrect username or password.")

# Registration function
def register():
    st.title("User Registration")
    
    username = st.text_input("Username", key="reg_username")
    password = st.text_input("Password", type="password", key="reg_password")
    role = st.selectbox("Role", ["Doctor", "Patient"], key="reg_role")
    
    if role == "Patient":
        doctor_id = st.text_input("Doctor ID", key="reg_doctor_id")
        injury_type = st.selectbox("Injury Type", ["Rotator Cuff Tear", "Frozen Shoulder", "Dislocation"], key="reg_injury_type")
        age = st.number_input("Age", min_value=10, max_value=100, key="reg_age")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="reg_gender")
        start_date = st.date_input("Rehabilitation Start Date", value=date.today(), key="reg_start_date")
    else:
        doctor_id = st.text_input("Doctor ID", key="reg_doctor_id")
    
    if st.button("Register"):
        if username and password and username not in users:
            if role == "Patient":
                valid_doctor = any(user for user in users if users[user]["role"] == "Doctor" and users[user]["doctor_id"] == doctor_id)
                if not valid_doctor:
                    st.error("Doctor ID not found. Please enter a valid Doctor ID.")
                    return
                users[username] = {
                    "password": password,
                    "role": role,
                    "doctor_id": doctor_id,
                    "injury_type": injury_type,
                    "age": age,
                    "gender": gender,
                    "start_date": str(start_date)
                }
                for user in users:
                    if users[user]["role"] == "Doctor" and users[user]["doctor_id"] == doctor_id:
                        if "patients" not in users[user]:
                            users[user]["patients"] = []
                        users[user]["patients"].append(username)
            else:
                users[username] = {
                    "password": password,
                    "role": role,
                    "doctor_id": doctor_id,
                    "patients": []
                }
            save_users(users)
            st.success("Registration successful! You can now log in.")
        elif username in users:
            st.error("Username already exists. Please choose a different one.")
        else:
            st.error("Please fill in all fields.")

# Logout function
def logout():
    st.title("User Logout")
    
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.user_data = None
        st.success("Logged out successfully.")
        st.rerun()

# Page objects (for navigation compatibility if needed)
login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
instruction = st.Page("tools/instruction.py", title="Instruction", icon=":material/search:")
compare = st.Page("tools/test.py", title="compare", icon=":material/search:")

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_data = None

# Main interface after login
if st.session_state.logged_in:
    if st.session_state.user_data["role"] == "Doctor":
        if "patients" in st.session_state.user_data:
            st.sidebar.title("Your Patients - Info")
            selected_patient = st.sidebar.radio("Select a patient", st.session_state.user_data["patients"])
            if selected_patient in users:
                patient_data = users[selected_patient]
                st.write(f"### Patient: {selected_patient}")
                st.write(f"**Injury Type:** {patient_data['injury_type']}")
                st.write(f"**Age:** {patient_data['age']}")
                st.write(f"**Gender:** {patient_data['gender']}")
                st.write(f"**Rehabilitation Start Date:** {patient_data['start_date']}")
                
        st.sidebar.title("Your Patients - Progress")
        page = st.sidebar.radio("Go to", ["Log out"])
        if page == "Log out":
            logout()
    
    elif st.session_state.user_data["role"] == "Patient":
        page = st.navigation(
            {
                "Account": [logout_page],
                "Tools": [instruction,compare],
            }
        )
        page.run()

# Interface before login
else:
    option = st.radio("Please choose an action", ["Login", "Register"])
    if option == "Login":
        login()
    else:
        register()
