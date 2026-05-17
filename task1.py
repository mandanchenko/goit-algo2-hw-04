import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms.flow import edmonds_karp

# 1. Побудова графа
def create_logistics_graph():
    G = nx.DiGraph()
    
    # Основні маршрути
    edges = [
        ('Terminal 1', 'Warehouse 1', 25), ('Terminal 1', 'Warehouse 2', 20), ('Terminal 1', 'Warehouse 3', 15),
        ('Terminal 2', 'Warehouse 3', 15), ('Terminal 2', 'Warehouse 4', 30), ('Terminal 2', 'Warehouse 2', 10),
        ('Warehouse 1', 'Shop 1', 15), ('Warehouse 1', 'Shop 2', 10), ('Warehouse 1', 'Shop 3', 20),
        ('Warehouse 2', 'Shop 4', 15), ('Warehouse 2', 'Shop 5', 10), ('Warehouse 2', 'Shop 6', 25),
        ('Warehouse 3', 'Shop 7', 20), ('Warehouse 3', 'Shop 8', 15), ('Warehouse 3', 'Shop 9', 10),
        ('Warehouse 4', 'Shop 10', 20), ('Warehouse 4', 'Shop 11', 10), ('Warehouse 4', 'Shop 12', 15),
        ('Warehouse 4', 'Shop 13', 5), ('Warehouse 4', 'Shop 14', 10)
    ]
    
    for u, v, cap in edges:
        G.add_edge(u, v, capacity=cap)

    # Технічні вузли для Edmonds-Karp
    G.add_edge('S', 'Terminal 1', capacity=60)
    G.add_edge('S', 'Terminal 2', capacity=55)
    
    for i in range(1, 15):
        G.add_edge(f'Shop {i}', 'T', capacity=float('inf'))
    
    return G

# 2. Обчислення потоку
def calculate_max_flow(G):
    # Повертає значення та словник розподілу потоків
    return nx.maximum_flow(G, 'S', 'T', flow_func=edmonds_karp)

# 3. Генерація таблиці розподілу
def get_distribution_table(flow_dict):
    distribution = []
    terminals = ['Terminal 1', 'Terminal 2']
    warehouses = ['Warehouse 1', 'Warehouse 2', 'Warehouse 3', 'Warehouse 4']
    shops = [f'Shop {i}' for i in range(1, 15)]

    for w in warehouses:
        total_in_w = sum(flow_dict[t][w] for t in terminals if w in flow_dict[t])
        if total_in_w == 0: continue

        for t in terminals:
            if w not in flow_dict[t] or flow_dict[t][w] == 0: continue
            share = flow_dict[t][w] / total_in_w
            
            for s in shops:
                if s in flow_dict[w] and flow_dict[w][s] > 0:
                    distribution.append({
                        "Термінал": t, "Склад": w, "Магазин": s, "Потік": round(flow_dict[w][s] * share, 2)
                    })
    return pd.DataFrame(distribution)

# 4. Генерація таблиці вузьких місць
def get_bottlenecks_table(G, flow_dict):
    bottlenecks = []
    for u, v, data in G.edges(data=True):
        if u == 'S' or v == 'T': continue
        actual, limit = flow_dict[u][v], data['capacity']
        if actual == limit and limit > 0:
            bottlenecks.append({"Від": u, "До": v, "Завантаження": f"{actual}/{limit} (100%)"})
    return pd.DataFrame(bottlenecks)

# 5. Візуалізація
def visualize_network(G, flow_dict):
    plt.figure(figsize=(16, 10))
    
    # 1. Чіткі координати для логістичних об'єктів
    pos = {
        'Terminal 1': (0, 5), 'Terminal 2': (0, 2),
        'Warehouse 1': (2, 7), 'Warehouse 2': (2, 5), 
        'Warehouse 3': (2, 3), 'Warehouse 4': (2, 1),
        'Shop 1': (4, 8.5), 'Shop 2': (4, 8), 'Shop 3': (4, 7.5),
        'Shop 4': (4, 6.5), 'Shop 5': (4, 6), 'Shop 6': (4, 5.5),
        'Shop 7': (4, 4.5), 'Shop 8': (4, 4), 'Shop 9': (4, 3.5),
        'Shop 10': (4, 2.5), 'Shop 11': (4, 2), 'Shop 12': (4, 1.5), 
        'Shop 13': (4, 1), 'Shop 14': (4, 0.5)
    }
    
    # Створюємо словник міток тільки для тих вузлів, що є в pos
    # Це запобігає спробам підписати 'S' та 'T'
    node_labels = {node: node for node in G.nodes() if node in pos}
    
    # 2. Малюємо вузли
    nx.draw_networkx_nodes(G, pos, nodelist=node_labels.keys(), 
                           node_color='skyblue', node_size=2500)
    
    # КЛЮЧОВЕ ВИПРАВЛЕННЯ: передаємо конкретний список міток
    nx.draw_networkx_labels(G, pos, labels=node_labels, 
                            font_size=9, font_weight='bold')
    
    # 3. Малюємо ребра та потік
    edge_labels = {}
    for u, v in G.edges():
        if u in pos and v in pos:
            flow = flow_dict[u][v]
            cap = G[u][v]['capacity']
            
            # Колір: червоний для вузьких місць
            color = 'red' if (flow == cap and cap > 0) else 'green'
            width = 1.0 + (flow / 10)
            
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], 
                                   edge_color=color, width=width, 
                                   arrows=True, arrowsize=20)
            
            edge_labels[(u, v)] = f"{int(flow)}/{cap}"

    # Малюємо цифри потоків на ребрах
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Фінальний розподіл товарів у логістичній мережі\n(Цифри: Фактичний потік / Пропускна здатність)", pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Виконання програми
if __name__ == "__main__":
    # Крок 1: Побудова
    logistic_graph = create_logistics_graph()
    
    # Крок 2: Розрахунок
    max_val, flows = calculate_max_flow(logistic_graph)
    
    # Крок 3: Аналітика
    df_dist = get_distribution_table(flows)
    df_bottles = get_bottlenecks_table(logistic_graph, flows)
    
    # Вивід результатів
    print(f"Максимальний потік: {max_val}")
    print("\nТаблиця розподілу:\n", df_dist)
    print("\nВузькі місця:\n", df_bottles)
    
    # Крок 4: Візуалізація
    visualize_network(logistic_graph, flows)