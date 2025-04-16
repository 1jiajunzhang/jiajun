import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --------------- 视频播放 ---------------- #

# 视频文件列表
video_files = ["videos/v1.mp4", "videos/v2.mp4", "videos/v3.mp4"]  # 这里可以修改视频数量

# 初始化 session state
if "video_index" not in st.session_state:
    st.session_state.video_index = 0
if "completed" not in st.session_state:
    st.session_state.completed = False

def next_video():
    if st.session_state.video_index < len(video_files) - 1:
        st.session_state.video_index += 1
    else:
        st.session_state.completed = True
    st.rerun()

# 显示视频
st.video(video_files[st.session_state.video_index], loop=True)  # 启用循环播放

# 显示按钮
if not st.session_state.completed:
    if st.button("Next"):
        next_video()
else:
    if st.button("Done"):
        st.balloons()
        st.write("### You've completed all of today's training, you're awesome!")
        

# --------------- 3D 传感器可视化 ---------------- #

st.header("3D IMU Sensor Visualization")

# 读取 IMU 数据（按照文件顺序，而不是按时间合并）
file1_path = "doc/HumeralMonitor1.txt"  # 请修改为实际文件路径
file2_path = "doc/HumeralMonitor2.txt"
file3_path = "doc/HumeralMonitor3.txt"

df1 = pd.read_csv(file1_path, sep=" ", header=None, names=["Time1", "X1", "Y1", "Z1", "W1"])
df2 = pd.read_csv(file2_path, sep=" ", header=None, names=["Time2", "X2", "Y2", "Z2", "W2"])
df3 = pd.read_csv(file3_path, sep=" ", header=None, names=["Time3", "X3", "Y3", "Z3", "W3"])

# **保证三组数据行数相等**
min_len = min(len(df1), len(df2), len(df3))
df1, df2, df3 = df1.iloc[:min_len], df2.iloc[:min_len], df3.iloc[:min_len]  # 截取最短的长度，确保索引一致

# **唯一** 3D 图表占位符
chart_placeholder = st.empty()

# 设定坐标轴范围，防止缩放跳动
x_range = [-1, 1]
y_range = [-1, 1]
z_range = [-1, 1]

# **模拟实时数据流**
for index in range(min_len):
    latest_x1, latest_y1, latest_z1 = df1.iloc[index][["X1", "Y1", "Z1"]]
    latest_x2, latest_y2, latest_z2 = df2.iloc[index][["X2", "Y2", "Z2"]]
    latest_x3, latest_y3, latest_z3 = df3.iloc[index][["X3", "Y3", "Z3"]]
    time_key = index  # 用索引作为唯一 Key，保证顺序不变

    # **创建 3D 轨迹图**
    fig = go.Figure()

    # **点 1**
    fig.add_trace(go.Scatter3d(
        x=[latest_x1], y=[latest_y1], z=[latest_z1],
        mode="markers",
        marker=dict(size=8, color="red"),
        name="HumeralMonitor1"
    ))

    # **点 2**
    fig.add_trace(go.Scatter3d(
        x=[latest_x2], y=[latest_y2], z=[latest_z2],
        mode="markers",
        marker=dict(size=8, color="blue"),
        name="HumeralMonitor2"
    ))

    # **点 3**
    fig.add_trace(go.Scatter3d(
        x=[latest_x3], y=[latest_y3], z=[latest_z3],
        mode="markers",
        marker=dict(size=8, color="green"),
        name="HumeralMonitor3"
    ))

    # **连接三点的线**
    fig.add_trace(go.Scatter3d(
        x=[latest_x1, latest_x2, latest_x3],
        y=[latest_y1, latest_y2, latest_y3],
        z=[latest_z1, latest_z2, latest_z3],
        mode="lines",
        line=dict(color="black", width=3),
        name="连接线"
    ))

    # **设定坐标轴范围**
    fig.update_layout(
        scene=dict(
            xaxis_title="X 轴",
            yaxis_title="Y 轴",
            zaxis_title="Z 轴",
            xaxis=dict(range=x_range),
            yaxis=dict(range=y_range),
            zaxis=dict(range=z_range)
        ),
        title="IMU 三传感器 3D 位置"
    )

    # ✅ **使用 `index` 作为 key，确保唯一 ID（按顺序）**
    chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"plotly_chart_{time_key}")

    # **控制更新频率**
    time.sleep(0.1)
