# Vấn đề 2: Xử lý văn bản không có cấu trúc
# Thách thức
# - Mô tả công việc (jd) là dữ liệu không có cấu trúc, khiến việc phân tích và trích xuất thông tin gặp khó khăn.
# - Ví dụ: Tìm ra các kỹ năng phổ biến hoặc yêu cầu chính trong mô tả công việc.
# Giải pháp
# - Trích xuất từ khóa: Sử dụng công cụ như RAKE hoặc TF-IDF để trích xuất các từ khóa quan trọng từ mô tả công việc.
# - Phân cụm nội dung: Sử dụng thuật toán phân cụm như KMeans để nhóm các công việc dựa trên nội dung mô tả.
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from rake_nltk import Rake

# Load data
data = pd.read_json('./files/myamcat.json')

# Extract keywords using RAKE
rake = Rake()
all_keywords = []
for jd in data['jd'].dropna():
    rake.extract_keywords_from_text(jd)
    all_keywords.extend(rake.get_ranked_phrases())

# Count most common keywords
common_keywords = Counter(all_keywords).most_common(10)
print("Most common keywords:", common_keywords)

# Create a Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(all_keywords))

# Display Word Cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Job Descriptions')
plt.show()
