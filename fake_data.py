# import json
# import random

# # Các trang giả lập trên website
# pages = ["/home", "/jobs", "/job/it-job", "/job/hr-job", "/job/dev-tech", "/contact", "/about", "/blog", "/login", "/register"]

# # Tạo dữ liệu clickstream giả lập
# fake_clickstream_data = []

# # Số lượng người dùng giả lập
# num_users = 50

# for i in range(1, num_users + 1):
#     user_ip = f"192.168.1.{i}"  # Tạo địa chỉ IP giả lập
#     path_length = random.randint(2, 5)  # Số trang trong hành trình
#     path = random.sample(pages, path_length)  # Hành trình truy cập ngẫu nhiên
#     fake_clickstream_data.append({"user": user_ip, "path": path})

# # Lưu dữ liệu giả lập vào tệp JSON
# with open("clickstream.json", "w") as file:
#     json.dump(fake_clickstream_data, file, indent=2)

# print(f"Generated clickstream data for {num_users} users and saved to 'clickstream.json'")

import random
from datetime import datetime, timedelta

# Các trang và trình duyệt giả lập
pages = ["/home", "/jobs", "/job/it-job", "/job/hr-job", "/job/dev-tech", "/contact", "/about", "/blog", "/login", "/register"]
browsers = ["Chrome", "Firefox", "Safari", "Edge"]

# Tạo dữ liệu nhật ký giả lập
log_data = []

# Số lượng người dùng và lượt truy cập giả lập
num_users = 500
num_entries_per_user = 10

start_time = datetime(2023, 1, 1, 10, 0, 0)

for user_id in range(1, num_users + 1):
    ip_address = f"192.168.1.{user_id}"
    for _ in range(num_entries_per_user):
        timestamp = start_time + timedelta(seconds=random.randint(0, 3600))
        page = random.choice(pages)
        browser = random.choice(browsers)
        time_on_page = random.randint(1, 30)
        log_data.append(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')},{ip_address},{page},{browser},{time_on_page}")

# Lưu dữ liệu vào tệp
with open("web_log.txt", "w") as file:
    file.write("\n".join(log_data))

print(f"Generated log data for {num_users} users and saved to 'web_log.txt'")