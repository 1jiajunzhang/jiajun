import pandas as pd
import random
from datetime import datetime, timedelta

# 设置文件与对应日期
file_date_map = {
    "doc/move4.csv": "2025-05-15",
    "doc/move2.csv": "2025-05-14",
    "doc/move3.csv": "2025-05-13",
    "doc/move8.csv": "2025-05-12",
    "doc/move1.csv": "2025-05-12",
    "doc/move6.csv": "2025-05-11",
    "doc/move7.csv": "2025-05-11",
    "doc/move9.csv": "2025-05-10",
    "doc/move11.csv": "2025-05-10",
    "doc/move10.csv": "2025-05-09",
    "doc/move5.csv": "2025-05-09",

}

# 白天时间段（8:00 到 18:00）
def get_random_daytime_timestamp(date_str):
    base_date = datetime.strptime(date_str, "%Y-%m-%d")
    # 白天从 8:00 到 18:00（共10小时 = 36000秒）
    random_seconds = random.randint(8*3600, 18*3600)
    random_time = base_date + timedelta(seconds=random_seconds)
    return random_time.strftime("%Y-%m-%d %H:%M:%S")

# 批量处理每个文件
for file_path, date_str in file_date_map.items():
    df = pd.read_csv(file_path)
    timestamp = get_random_daytime_timestamp(date_str)
    df["Timestamp"] = timestamp
    df.to_csv(file_path, index=False)
    print(f"✅ 已为 {file_path} 添加标签时间：{timestamp}")
