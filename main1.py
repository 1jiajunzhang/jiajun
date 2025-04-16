import streamlit as st
from datetime import date

# Function for user login
def login():
    st.title("User Login")  # Display title for login page
    
    # User input fields for login
    username = st.text_input("Username", key="username")  # Input field for username
    password = st.text_input("Password", type="password", key="password")  # Input field for password (masked)
    injury_type = st.selectbox(  # Dropdown for selecting injury type
        "Type of Injury", 
        ["Rotator Cuff Tear", "Frozen Shoulder (Adhesive Capsulitis)", "Shoulder Dislocation"], 
        key="injury_type"
    )
    age = st.number_input("Age", min_value=10, max_value=100, key="age")  # Numeric input for age
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender")  # Dropdown for gender selection
    start_date = st.date_input("Start Date", value=date.today(), key="start_date")  # Date picker for start date
    
    # Login button functionality
    if st.button("Log in"):
        if username and password:  # Check if username and password are entered
            # Store login state and user details in session
            st.session_state.logged_in = True  
            st.session_state.user_data = {
                "username": username,
                "injury_type": injury_type,
                "age": age,
                "gender": gender,
                "start_date": start_date
            }
            st.success("Login successful!")  # Display success message
            st.rerun()  # Refresh the page after login
        else:
            st.error("Please enter a valid username and password.")  # Display error if fields are empty

# Function for user logout
def logout():
    st.title("User Logout")  # Display title for logout page
    
    # Logout button functionality
    if st.button("Log out"):
        st.session_state.logged_in = False  # Reset login state
        st.session_state.user_data = None  # Clear user data
        st.success("Logged out successfully.")  # Display success message
        st.rerun()  # Refresh the page after logout

# Define navigation pages for the application
login_page = st.Page(login, title="Log in", icon=":material/login:")  # Login page
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")  # Logout page

# Reports section
#dashboard = st.Page("reports/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)  # Main dashboard page
#bugs = st.Page("reports/bugs.py", title="Bug reports", icon=":material/bug_report:")  # Bug reporting page
#alerts = st.Page("reports/alerts.py", title="System alerts", icon=":material/notification_important:")  # System alerts page

# Tools section
instruction = st.Page("tools/instruction.py", title="Instruction", icon=":material/search:")  # Search tool page
#history = st.Page("tools/history.py", title="History", icon=":material/history:")  # History tool page

# Initialize session state variables if not set
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False  # Default login state is False
    st.session_state.user_data = None  # No user data by default

# Navigation logic based on login status
if st.session_state.logged_in:
    # Show different sections for logged-in users
    pg = st.navigation(
        {
            "Account": [logout_page],  # Account section with logout option
            #"Reports": [dashboard, bugs, alerts],  # Reports section
            "Tools": [instruction],  # Tools section
        }
    )
else:
    # If not logged in, show only the login page
    pg = st.navigation([login_page])


# Run the selected navigation page
pg.run()
