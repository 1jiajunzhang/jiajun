import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from scipy.spatial.transform import Rotation as R
import os

st.set_page_config(page_title="Motion Review Calendar", layout="wide")
st.title("🗓️ Motion Review: Calendar + 3D Animation Comparison")

# Load all motion CSVs and extract their dates
motion_files = ["jiajun_move1.csv", "jiajun_move2.csv", "jiajun_move3.csv", "jiajun_move4.csv","jiajun_move5.csv", "Goran_move6.csv", "Goran_move7.csv", "Goran_move8.csv", "Goran_move9.csv", "Goran_move10.csv", "Goran_move11.csv"]
motion_data = []

for file in motion_files:
    df = pd.read_csv(f"doc/{file}")
    if "Timestamp" in df.columns:
        date_str = df["Timestamp"].iloc[0].split(" ")[0]
        motion_data.append({"file": file, "date": date_str, "label": file.replace(".csv", "").capitalize()})

# ---------------------
# Step 1: Show calendar with activity
# ---------------------
available_dates = sorted(list(set([item["date"] for item in motion_data])))

with st.expander("📅 Dates with motion records"):
    st.markdown("These dates have recorded motions:")
    for date in available_dates:
        st.markdown(f"- ✅ **{date}**")

selected_date = st.selectbox("📆 Choose a date to view motions:", options=available_dates)

# ---------------------
# Step 2: List motions on selected date
# ---------------------
motions_today = [item for item in motion_data if item["date"] == selected_date]

st.subheader(f"📌 Motions recorded on {selected_date}")
motion_labels = [m["label"] for m in motions_today]
chosen_label = st.selectbox("🎯 Select a motion to compare:", motion_labels)

# ---------------------
# Step 3: Load data for comparison
# ---------------------
chosen_file = next(m["file"] for m in motions_today if m["label"] == chosen_label)
df_standard = pd.read_csv("doc/standard.csv")
df_user = pd.read_csv(f"doc/{chosen_file}")

axis_range = [-1.5, 1.5]

def swap_yz(v):
    return np.array([v[0], v[2], v[1]])

def generate_frames(df):
    frames = []
    for i in range(len(df)):
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
                         mode='markers', marker=dict(size=4, color='black'), name="Origin"),
            go.Scatter3d(x=[O[0], P1[0]], y=[O[1], P1[1]], z=[O[2], P1[2]],
                         mode='lines+markers', marker=dict(size=4, color='red'),
                         line=dict(color='red', width=5), name="Radius (Upper Arm)"),
            go.Scatter3d(x=[P1[0], P2[0]], y=[P1[1], P2[1]], z=[P1[2], P2[2]],
                         mode='lines+markers', marker=dict(size=4, color='blue'),
                         line=dict(color='blue', width=5), name="Humerus (Forearm)")
        ]
        frames.append(go.Frame(data=frame_data, name=str(i)))
    return frames

def build_figure(frames, title):
    camera = dict(eye=dict(x=2.5, y=0.01, z=2.5), up=dict(x=0, y=1, z=0))
    return go.Figure(
        data=frames[0].data,
        layout=go.Layout(
            title=title,
            scene=dict(
                xaxis=dict(title='Z (Left-Right)', range=axis_range),
                yaxis=dict(title='Y (Up-Down)', range=axis_range),
                zaxis=dict(title='X (Depth)', range=axis_range),
                aspectmode="manual",
                aspectratio=dict(x=1.2, y=1.2, z=1.2)
            ),
            scene_camera=camera,
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

# ---------------------
# Step 4: Show animation comparison
# ---------------------
st.subheader(f"🎥 Comparing Standard Motion vs. {chosen_label}")
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(build_figure(generate_frames(df_standard), "Standard Motion"), use_container_width=True)

with col2:
    st.plotly_chart(build_figure(generate_frames(df_user), f"{chosen_label} Motion"), use_container_width=True)
