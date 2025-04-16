
import time  # 用于模拟实时数据流
import numpy as np  # 用于数值计算
import pandas as pd  # 处理 CSV 数据
import plotly.express as px  # 交互式数据可视化
import streamlit as st  # Streamlit Web 应用框架
import uuid  # 用于生成唯一的 key，防止重复 ID 错误

# 设置 Streamlit 页面配置
st.set_page_config(
    page_title="Real-Time Data Science Dashboard",  # 网页标题
    page_icon="✅",  # 页面图标
    layout="wide",  # 采用宽屏布局
)

# 读取远程 CSV 数据的 URL
dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

# 使用 Streamlit 缓存机制缓存数据，避免重复下载
@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)  # 读取 CSV 数据并返回 DataFrame

df = get_data()  # 获取数据

# 在页面上显示主标题
st.title("Real-Time / Live Data Science Dashboard")

# 添加下拉筛选器，用户可以选择职业类别
job_filter = st.selectbox("Select the Job", pd.unique(df["job"]))

# 创建一个占位符容器，用于实时更新数据
placeholder = st.empty()

# 根据筛选条件过滤数据
df = df[df["job"] == job_filter]

# 开始模拟实时数据流（循环 200 次，每次间隔 1 秒）
for seconds in range(200):

    # 生成新的列，模拟数据动态变化
    df["age_new"] = df["age"] * np.random.choice(range(1, 5))  # 年龄数据乘以 1-4 之间的随机数
    df["balance_new"] = df["balance"] * np.random.choice(range(1, 5))  # 账户余额数据变化

    # 计算 KPI（关键指标）
    avg_age = np.mean(df["age_new"])  # 计算平均年龄

    # 计算已婚人数，并随机增加 1~30 之间的浮动值
    count_married = int(df[df["marital"] == "married"]["marital"].count() + np.random.choice(range(1, 30)))

    balance = np.mean(df["balance_new"])  # 计算账户平均余额

    with placeholder.container():  # 使用占位符，刷新整个数据区块

        # 创建三列用于展示 KPI 指标
        kpi1, kpi2, kpi3 = st.columns(3)

        # 填充 KPI 指标数据
        kpi1.metric(label="Age ⏳", value=round(avg_age), delta=round(avg_age) - 10)  # 显示平均年龄
        kpi2.metric(label="Married Count 💍", value=int(count_married), delta=-10 + count_married)  # 已婚人数
        kpi3.metric(label="A/C Balance ＄", value=f"$ {round(balance,2)} ", delta=-round(balance / count_married) * 100)  # 账户余额

        # 创建两个列用于显示图表
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.markdown("### First Chart")  # 图表标题
            fig = px.density_heatmap(data_frame=df, y="age_new", x="marital")  # 生成热力图
            st.plotly_chart(fig, use_container_width=True, key=f"heatmap_{uuid.uuid4()}")  # 生成唯一 key，避免冲突

        with fig_col2:
            st.markdown("### Second Chart")  # 图表标题
            fig2 = px.histogram(data_frame=df, x="age_new")  # 生成直方图
            st.plotly_chart(fig2, use_container_width=True, key=f"histogram_{uuid.uuid4()}")  # 生成唯一 key，避免冲突

        # 显示详细数据表格
        st.markdown("### Detailed Data View")
        st.dataframe(df)  # 在页面上显示 DataFrame 数据表

    time.sleep(0.01)  # 等待 1 秒，模拟实时数据流


