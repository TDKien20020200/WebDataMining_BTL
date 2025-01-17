import json
import networkx as nx
import matplotlib.pyplot as plt

# Load dữ liệu clickstream
with open('clickstream.json', 'r') as file:
    clickstream_data = json.load(file)  # Sửa lỗi ở đây

# Xây dựng đồ thị clickstream
clickstream_graph = nx.DiGraph()

for session in clickstream_data:
    path = session['path']
    for i in range(len(path) - 1):
        clickstream_graph.add_edge(path[i], path[i + 1])

# Phân tích đồ thị
print("Số lượng trang:", clickstream_graph.number_of_nodes())
print("Số lượng đường dẫn:", clickstream_graph.number_of_edges())

# Vẽ đồ thị clickstream
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(clickstream_graph)
nx.draw(clickstream_graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10)
plt.title("Clickstream Graph")
plt.show()
