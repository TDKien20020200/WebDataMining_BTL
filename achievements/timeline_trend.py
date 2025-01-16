# Vấn đề 4: Phân tích xu hướng theo thời gian
# Thách thức
# - Dữ liệu công việc thường thay đổi theo thời gian (ví dụ: yêu cầu kỹ năng, số lượng công việc theo ngành).
# - Việc hiểu xu hướng này có thể giúp dự báo và lập kế hoạch.
# Giải pháp
# - Phân tích thời gian: Theo dõi sự thay đổi số lượng công việc theo tháng hoặc theo ngành.
# - Dự báo: Sử dụng các mô hình chuỗi thời gian (time series) để dự đoán xu hướng trong tương lai.
import pandas as pd
import matplotlib.pyplot as plt
import re

# Load data
data = pd.read_json('./files/myamcat.json')

# Function to clean 'created' dates
def clean_created_dates(created_column):
    cleaned = []
    for value in created_column:
        if isinstance(value, str):
            # Nếu chứa "days ago", chuyển đổi thành số ngày
            match = re.search(r'(\d+)\s+days\s+ago', value)
            if match:
                days_ago = int(match.group(1))
                cleaned.append(pd.Timestamp.now() - pd.Timedelta(days=days_ago))
            elif "yesterday" in value.lower():
                cleaned.append(pd.Timestamp.now() - pd.Timedelta(days=1))
            else:
                cleaned.append(None)
        else:
            cleaned.append(None)
    return pd.Series(cleaned)

# Clean and convert 'created' to datetime
data['created_date'] = clean_created_dates(data['created'])

# Drop NaT values
data = data.dropna(subset=['created_date'])

# Group jobs by month
jobs_by_month = data.groupby(data['created_date'].dt.to_period('M')).size()

# Plot if data is available
if jobs_by_month.empty:
    print("No valid dates available for plotting.")
else:
    jobs_by_month.plot(kind='line', title='Job Trend Over Time', xlabel='Month', ylabel='Job Count', marker='o')
    plt.grid()
    plt.show()
