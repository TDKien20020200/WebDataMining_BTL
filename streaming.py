# Ứng dụng thực tiễn
# Ý tưởng
# - Dashboard trực quan: Sử dụng công cụ như Streamlit hoặc Dash để hiển thị bảng điều khiển tương tác.
# - Hệ thống gợi ý: Phát triển hệ thống gợi ý công việc dựa trên ngành nghề hoặc kỹ năng.
import streamlit as st
import pandas as pd

# Load dữ liệu
data = pd.read_json('./files/myamcat.json')

# Hiển thị dữ liệu cơ bản
st.title('Job Analysis Dashboard')
st.write(data)

# Bộ lọc
selected_classification = st.selectbox('Select Classification', data['classification'].unique())
filtered_data = data[data['classification'] == selected_classification]
st.write(filtered_data)
