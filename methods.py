import pandas as pd

# Phân tích thống kê cơ bản
# Ý tưởng
# - Thống kê số lượng công việc theo ngành nghề (classification).
# - Số lượng công việc theo vị trí (location).
# - Phân phối mức lương (salary) hoặc yêu cầu kinh nghiệm (experience).
# Đọc dữ liệu JSON
data = pd.read_json('./files/myamcat.json')

# Thống kê số lượng công việc theo ngành nghề
job_count_by_classification = data['classification'].value_counts()

# Thống kê số lượng công việc theo vị trí
job_count_by_location = data['location'].value_counts()

# Phân phối mức lương (nếu dữ liệu lương hợp lệ)
data['salary_numeric'] = data['salary'].str.extract(r'(\d+\.?\d*)').astype(float)
salary_distribution = data['salary_numeric'].describe()

# print(job_count_by_classification)
# print(job_count_by_location)
# print(salary_distribution)

# Vẽ biểu đồ
# Ý tưởng
# - Vẽ biểu đồ thanh hiển thị số lượng công việc theo ngành nghề.
# - Biểu đồ hình tròn thể hiện tỷ lệ công việc theo vị trí.
# - Biểu đồ hộp (boxplot) hiển thị phân phối mức lương.
import matplotlib.pyplot as plt

# # Biểu đồ thanh số lượng công việc theo ngành nghề
# job_count_by_classification.plot(kind='bar', title='Jobs by Classification', xlabel='Classification', ylabel='Count')
# plt.show()

# # Biểu đồ hình tròn tỷ lệ công việc theo vị trí
# job_count_by_location.head(10).plot(kind='pie', title='Top 10 Locations by Job Count', autopct='%1.1f%%')
# plt.ylabel('')
# plt.show()

# # Biểu đồ hộp phân phối mức lương
# data.boxplot(column='salary_numeric', vert=False)
# plt.title('Salary Distribution')
# plt.xlabel('Salary (in LPA)')
# plt.show()

# Phân tích từ khóa từ mô tả công việc
# Ý tưởng
# - Trích xuất các từ khóa phổ biến trong jd (mô tả công việc) để hiểu yêu cầu kỹ năng chung.
# - Xây dựng biểu đồ "word cloud" để trực quan hóa các từ khóa.
from wordcloud import WordCloud

# Gộp tất cả mô tả công việc
text = ' '.join(data['jd'].dropna())

# Tạo biểu đồ Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# # Hiển thị Word Cloud
# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# plt.title('Word Cloud of Job Descriptions')
# plt.show()

# Khai phá nâng cao
# Ý tưởng
# - Dự đoán ngành nghề: Sử dụng mô hình đã huấn luyện (job_classifier.pkl) để dự đoán ngành nghề của các công việc mới.
# - Clustering: Phân cụm các công việc dựa trên mô tả (jd) để tìm nhóm ngành tương đồng.
# - Phân tích xu hướng: Theo dõi sự thay đổi trong yêu cầu kỹ năng, mức lương hoặc số lượng công việc qua thời gian (created).
from sklearn.cluster import KMeans

# Vector hóa mô tả công việc
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['jd'].dropna())

# Phân cụm
kmeans = KMeans(n_clusters=5, random_state=42)
data['cluster'] = kmeans.fit_predict(X)

print(data[['title', 'cluster']])

# Chuyển cột 'created' thành định dạng datetime
data['created'] = pd.to_datetime(data['created'], errors='coerce')

# Đếm số lượng công việc theo ngày/tháng
jobs_by_date = data.groupby(data['created'].dt.to_period('M')).size()

# Vẽ biểu đồ xu hướng
jobs_by_date.plot(title='Job Trend Over Time', xlabel='Month', ylabel='Job Count', kind='line')
plt.show()
