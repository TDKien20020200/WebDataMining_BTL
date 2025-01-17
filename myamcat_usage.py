import pandas as pd
import matplotlib.pyplot as plt

# Load dữ liệu nhật ký truy cập
log_columns = ['timestamp', 'ip', 'url', 'browser', 'time_on_page']
log_data = pd.read_csv('web_log.txt', names=log_columns)

# Chuyển đổi timestamp thành định dạng datetime
log_data['timestamp'] = pd.to_datetime(log_data['timestamp'])

# 1. Thống kê số lượng truy cập theo URL
url_access_count = log_data['url'].value_counts()
print("Số lượt truy cập theo URL:")
print(url_access_count)

# 2. Thống kê thời gian trung bình người dùng ở mỗi URL
average_time_on_page = log_data.groupby('url')['time_on_page'].mean()
print("\nThời gian trung bình trên mỗi URL:")
print(average_time_on_page)

# 3. Thống kê số lượng truy cập theo trình duyệt
browser_access_count = log_data['browser'].value_counts()
print("\nSố lượt truy cập theo trình duyệt:")
print(browser_access_count)

# 4. Vẽ biểu đồ số lượng truy cập theo URL
url_access_count.plot(kind='bar', title='Số lượt truy cập theo URL', xlabel='URL', ylabel='Số lượt truy cập')
plt.show()

# 5. Vẽ biểu đồ thời gian trung bình trên mỗi URL
average_time_on_page.plot(kind='bar', title='Thời gian trung bình trên mỗi URL', xlabel='URL', ylabel='Thời gian (giây)')
plt.show()
