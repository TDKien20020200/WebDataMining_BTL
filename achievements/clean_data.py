# Vấn đề 1: Chuẩn hóa và làm sạch dữ liệu không đồng nhất
# Thách thức
# - Dữ liệu từ các nguồn web thường không đồng nhất, chứa nhiều định dạng và thông tin bị thiếu.
# - Ví dụ: Trong dữ liệu công việc của bạn, các trường như salary, experience, hoặc location có thể có định dạng khác nhau hoặc bị thiếu.
# Giải pháp
# - Làm sạch dữ liệu: Chuẩn hóa các trường như salary thành số thực, tách các mức lương tối thiểu/tối đa.
# - Điền giá trị thiếu: Sử dụng phương pháp suy diễn hoặc trung bình để xử lý dữ liệu bị thiếu.
import pandas as pd
import json

# Load data from JSON file
data = pd.read_json('./files/myamcat.json')

# Clean and normalize salary
data['salary_numeric'] = data['salary'].str.extract(r'(\d+\.?\d*)').astype(float)

# Clean and normalize experience
data['experience_numeric'] = data['experience'].str.extract(r'(\d+)').astype(float)

# Fill missing values
data['salary_numeric'].fillna(data['salary_numeric'].mean(), inplace=True)
data['experience_numeric'].fillna(0, inplace=True)

# Save cleaned data
data.to_json('./files/myamcat_cleaned.json', orient='records', indent=2)

print("Data cleaned and saved to './files/myamcat_cleaned.json'")
