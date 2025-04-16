import streamlit as st
from datetime import date
import json

# 用户数据存储文件
USER_DATA_FILE = "user_data.json"


# 加载用户数据
def load_users():
    try:
        with open(USER_DATA_FILE, "r") as file:
            users = json.load(file)
            # 将 start_date 从字符串转换为 date 类型
            for user in users:
                if "start_date" in users[user] and users[user]["start_date"]:
                    users[user]["start_date"] = date.fromisoformat(users[user]["start_date"])
            return users
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# 保存用户数据
def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        users_serializable = {
            user: {**data, "start_date": str(data["start_date"]) if "start_date" in data and data["start_date"] else None}
            for user, data in users.items()
        }
        json.dump(users_serializable, file, indent=4)

# 初始化用户数据库
users = load_users()

# 用户登录功能
def login():
    st.title("login")
    username = st.text_input("用户名", key="login_username")
    password = st.text_input("密码", type="password", key="login_password")
    
    if st.button("login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user_data = users[username]
            st.success("登录成功！")
            st.rerun()
        else:
            st.error("用户名或密码错误。")

# 用户注册功能
def register():
    st.title("用户注册")
    
    username = st.text_input("用户名", key="reg_username")
    password = st.text_input("密码", type="password", key="reg_password")
    role = st.selectbox("角色", ["Doctor", "Patient"], key="reg_role")
    
    if role == "Patient":
        doctor_id = st.text_input("医生ID", key="reg_doctor_id")
        injury_type = st.selectbox("伤情类型", ["肩袖撕裂", "冻结肩（粘连性肩关节囊炎）", "肩关节脱位"], key="reg_injury_type")
        age = st.number_input("年龄", min_value=10, max_value=100, key="reg_age")
        gender = st.selectbox("性别", ["男", "女", "其他"], key="reg_gender")
        start_date = st.date_input("康复开始日期", value=date.today(), key="reg_start_date")
    else:
        doctor_id = st.text_input("医生ID", key="reg_doctor_id")
    
    if st.button("注册"):
        if username and password and username not in users:
            if role == "Patient":
                valid_doctor = any(user for user in users if users[user]["role"] == "Doctor" and users[user]["doctor_id"] == doctor_id)
                if not valid_doctor:
                    st.error("未找到该医生ID，请输入有效的医生ID。")
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
            st.success("注册成功！现在可以登录。")
        elif username in users:
            st.error("用户名已存在，请选择其他用户名。")
        else:
            st.error("请填写所有字段。")

# 登出功能
def logout():
    st.title("User Logout")  # Display title for logout page
    
    # Logout button functionality
    if st.button("Log out"):
        st.session_state.logged_in = False  # Reset login state
        st.session_state.user_data = None  # Clear user data
        st.success("Logged out successfully.")  # Display success message
        st.rerun()  # Refresh the page after logout
        #st.switch_page("main.py") 
        
login_page = st.Page(login, title="Log in", icon=":material/login:")  # Login page
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")  # Logout page

# Reports section
#dashboard = st.Page("reports/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)  # Main dashboard page
#bugs = st.Page("reports/bugs.py", title="Bug reports", icon=":material/bug_report:")  # Bug reporting page
#alerts = st.Page("reports/alerts.py", title="System alerts", icon=":material/notification_important:")  # System alerts page

# Tools section
instruction = st.Page("tools/instruction.py", title="Instruction", icon=":material/search:")  # Search tool page

# 初始化登录状态
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_data = None

# 登录后的主界面
if st.session_state.logged_in:
    #st.sidebar.title("导航")
    
    # 医生页面
    if st.session_state.user_data["role"] == "Doctor":
        if "patients" in st.session_state.user_data:
            st.sidebar.title("您的患者-信息")
            selected_patient = st.sidebar.radio("选择患者", st.session_state.user_data["patients"])
            if selected_patient in users:
                patient_data = users[selected_patient]
                st.write(f"### 患者：{selected_patient}")
                st.write(f"**伤情类型：** {patient_data['injury_type']}")
                st.write(f"**年龄：** {patient_data['age']}")
                st.write(f"**性别：** {patient_data['gender']}")
                st.write(f"**康复开始日期：** {patient_data['start_date']}")
                
        st.sidebar.title("您的患者-训练进程")
        page = st.sidebar.radio("前往页面", ["登出"])
        if page == "登出":
            logout()
    
    # 患者页面
    elif st.session_state.user_data["role"] == "Patient":
        page = st.navigation(
            {
                "Account": [logout_page],  # Account section with logout option
                #"Reports": [dashboard, bugs, alerts],  # Reports section
                "Tools": [instruction],  # Tools section
            }
            )
        page.run()


# 未登录状态：显示登录或注册界面
else:
    option = st.radio("请选择操作", ["login", "注册"])
    if option == "login":
        login()
    else:
        register()
        

