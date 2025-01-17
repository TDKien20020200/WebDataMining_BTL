import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt

# Thu thập liên kết từ trang web
def collect_links(url):
    print(f"Fetching links from: {url}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: Status code {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        links = set()

        # Lấy tất cả các thẻ <a href="">
        for a_tag in soup.find_all("a", href=True):
            href = a_tag['href']
            # Chỉ thu thập các liên kết nội bộ hoặc liên kết bắt đầu bằng 'http'
            if href.startswith("http") or href.startswith("/"):
                full_url = href if href.startswith("http") else url + href
                links.add(full_url)

        return list(links)

    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return []

# Xây dựng đồ thị cấu trúc web
def build_web_graph(start_url, depth=1):
    graph = nx.DiGraph()  # Sử dụng đồ thị có hướng
    to_visit = [start_url]
    visited = set()

    for _ in range(depth):
        new_to_visit = []
        for url in to_visit:
            if url not in visited:
                visited.add(url)
                links = collect_links(url)
                for link in links:
                    graph.add_edge(url, link)  # Thêm cạnh từ URL hiện tại tới liên kết
                    if link not in visited:
                        new_to_visit.append(link)
        to_visit = new_to_visit

    return graph

# Phân tích đồ thị
def analyze_graph(graph):
    print("Number of nodes (pages):", graph.number_of_nodes())
    print("Number of edges (links):", graph.number_of_edges())
    print("Top 5 nodes by degree:")
    degree_centrality = nx.degree_centrality(graph)
    for node, centrality in sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:50]:
        print(f"{node}: {centrality:.4f}")

# Vẽ đồ thị
def draw_graph(graph):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=False, node_size=20, edge_color="gray", alpha=0.7)
    plt.title("Web Structure Graph")
    plt.show()

# URL bắt đầu (có thể thay đổi)
start_url = "https://www.myamcat.com/"
web_graph = build_web_graph(start_url, depth=1)

# Phân tích và hiển thị đồ thị
analyze_graph(web_graph)
draw_graph(web_graph)
