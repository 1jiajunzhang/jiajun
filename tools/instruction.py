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
        
 