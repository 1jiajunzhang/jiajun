import streamlit as st
import json
from datetime import date

USER_DATA_FILE = "user_data.json"

def load_users():
    try:
        with open(USER_DATA_FILE, "r") as file:
            users = json.load(file)
            for user in users:
                if "start_date" in users[user] and users[user]["start_date"]:
                    users[user]["start_date"] = date.fromisoformat(users[user]["start_date"])
            return users
    except:
        return {}

users = load_users()

if "user_data" not in st.session_state or st.session_state.user_data["role"] != "Doctor":
    st.warning("请以医生身份登录访问此页面。")
else:
    st.title("查看患者信息")
    patient_list = st.session_state.user_data.get("patients", [])
    if not patient_list:
        st.info("您尚未关联任何患者。")
    else:
        selected = st.selectbox("选择患者", patient_list)
        if selected in users:
            data = users[selected]
            st.write(f"### 患者：{selected}")
            st.write(f"**伤情类型：** {data['injury_type']}")
            st.write(f"**年龄：** {data['age']}")
            st.write(f"**性别：** {data['gender']}")
            st.write(f"**康复开始日期：** {data['start_date']}")
