import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import altair as alt

# ---------------------
# 页面设置
# ---------------------
st.set_page_config(page_title="ROM Trend Viewer", layout="centered")
st.title("📈 Range of Motion (ROM) Trend Dashboard")

# ---------------------
# 加载数据
# ---------------------
data_dir = "doc"
motion_files = [f for f in os.listdir(data_dir) if f.startswith("Goran") or f.startswith("jiajun") and f.endswith(".csv")]

records = []
for file in motion_files:
    df = pd.read_csv(os.path.join(data_dir, file))
    if "Rotation_Angle" in df.columns and "Timestamp" in df.columns:
        max_angle = df["Rotation_Angle"].max()
        timestamp = pd.to_datetime(df["Timestamp"].iloc[0])
        records.append({"file": file, "timestamp": timestamp, "max_rotation": max_angle})

# 构建数据表
df_all = pd.DataFrame(records)
df_all["date"] = df_all["timestamp"].dt.date

# ---------------------
# 最近7天数据
# ---------------------
today = datetime.now().date()
df_week = df_all[df_all["date"] >= (today - timedelta(days=6))]

# 每天的最大角度
df_daily = df_week.groupby("date")["max_rotation"].max().reset_index()

# ---------------------
# 切换视图
# ---------------------
view_option = st.radio("📊 Choose view mode:", ["Each Record", "Daily Maximum"], horizontal=True)

if view_option == "Each Record":
    st.subheader("🔁 Max Rotation per Motion Record (Past 7 Days)")
    chart = alt.Chart(df_week).mark_line(point=True).encode(
        x="timestamp:T",
        y=alt.Y("max_rotation:Q", scale=alt.Scale(domain=[165, 185])),  # 设置 Y 轴范围
        tooltip=["file", "timestamp", "max_rotation"]
    ).properties(height=400)
    st.altair_chart(chart, use_container_width=True)

elif view_option == "Daily Maximum":
    st.subheader("📅 Max Rotation per Day (Past 7 Days)")
    chart = alt.Chart(df_daily).mark_line(point=True).encode(
        x="date:T",
        y=alt.Y("max_rotation:Q", scale=alt.Scale(domain=[165, 185])),  # 设置 Y 轴范围
        tooltip=["date", "max_rotation"]
    ).properties(height=400)
    st.altair_chart(chart, use_container_width=True)

# ---------------------
# 显示当前最大值
# ---------------------
if not df_all.empty:
    latest_row = df_all.sort_values("timestamp").iloc[-1]
    st.metric("📌 Most Recent Max Rotation", f"{latest_row['max_rotation']:.2f}°")
