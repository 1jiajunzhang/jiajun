import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.spatial.transform import Rotation as R

st.set_page_config(page_title="3D Vector Animation", layout="wide")
st.title("🦴 Arm Vector Animation (Forward & Reverse)")

# 读取数据
df = pd.read_csv("doc/motion_data.csv")
max_frame = len(df)
axis_range = [-1.5, 1.5]

def swap_yz(v):
    return np.array([v[0], v[2], v[1]])

# 生成帧序列的函数（支持正序和倒序）
def generate_frames(reverse=False):
    frames = []
    indices = range(max_frame)
    if reverse:
        indices = reversed(indices)

    for i in indices:
        h_q = df.loc[i, ["Humerus_w", "Humerus_x", "Humerus_y", "Humerus_z"]].to_numpy()
        r_q = df.loc[i, ["Radius_w", "Radius_x", "Radius_y", "Radius_z"]].to_numpy()

        h_rot = R.from_quat([h_q[1], h_q[2], h_q[3], h_q[0]])
        r_rot = R.from_quat([r_q[1], r_q[2], r_q[3], r_q[0]])

        radius_dir = swap_yz(r_rot.apply([1, 0, 0]))
        humerus_dir = swap_yz(h_rot.apply([1, 0, 0]))

        O = np.array([0, 0, 0])
        P1 = radius_dir
        P2 = P1 + humerus_dir

        frame_data = [
            go.Scatter3d(x=[O[0]], y=[O[1]], z=[O[2]],
                         mode='markers',
                         marker=dict(size=4, color='black'),
                         name="Origin"),
            go.Scatter3d(x=[O[0], P1[0]], y=[O[1], P1[1]], z=[O[2], P1[2]],
                         mode='lines+markers',
                         marker=dict(size=4, color='red'),
                         line=dict(color='red', width=5),
                         name="Radius (Upper Arm)"),
            go.Scatter3d(x=[P1[0], P2[0]], y=[P1[1], P2[1]], z=[P1[2], P2[2]],
                         mode='lines+markers',
                         marker=dict(size=4, color='blue'),
                         line=dict(color='blue', width=5),
                         name="Humerus (Forearm)")
        ]
        frames.append(go.Frame(data=frame_data, name=str(i)))
    return frames

# 生成两个动画：正序 & 倒序
frames_forward = generate_frames(reverse=False)
frames_reverse = generate_frames(reverse=True)

def build_figure(frames, title):
    return go.Figure(
        data=frames[0].data,
        layout=go.Layout(
            title=title,
            scene=dict(
                xaxis=dict(title='X', range=axis_range),
                yaxis=dict(title='Y (Up)', range=axis_range),
                zaxis=dict(title='Z', range=axis_range),
                aspectmode="cube"
            ),
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(label="▶ Play", method="animate", args=[None, {
                        "frame": {"duration": 100, "redraw": True},
                        "fromcurrent": True}]),
                    dict(label="⏸ Pause", method="animate", args=[[None], {
                        "frame": {"duration": 0, "redraw": False},
                        "mode": "immediate"}])
                ]
            )]
        ),
        frames=frames
    )

# 并列显示两个图
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(build_figure(frames_forward, "Forward Animation"), use_container_width=True)

with col2:
    st.plotly_chart(build_figure(frames_reverse, "Reverse Animation"), use_container_width=True)
