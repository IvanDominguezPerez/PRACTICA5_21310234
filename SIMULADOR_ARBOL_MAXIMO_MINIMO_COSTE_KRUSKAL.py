#Practica5: SIMULADOR ARBOL MAXIMO Y MINIMO COSTE KRUSKAL
#Alumno: Ivan Dominguez
#Registro: 21310234
#Grupo: 6E1

import networkx as nx  # Importa la biblioteca NetworkX para manejar grafos
import matplotlib.pyplot as plt  # Importa Matplotlib para la visualización gráfica

# Clase para manejar conjuntos disjuntos (Union-Find)
class DisjointSet:
    def __init__(self, vertices):
        # Inicializa cada vértice como un conjunto separado
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, item):
        # Encuentra el representante del conjunto al que pertenece el elemento 'item'
        if self.parent[item] == item:
            return item
        else:
            self.parent[item] = self.find(self.parent[item])  # Compresión de caminos
            return self.parent[item]

    def union(self, set1, set2):
        # Une dos conjuntos: el que contiene a 'set1' y el que contiene a 'set2'
        root1 = self.find(set1)
        root2 = self.find(set2)

        if root1 != root2:
            # Unión por rango para mantener el árbol plano
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root1] = root2
                if self.rank[root1] == self.rank[root2]:
                    self.rank[root2] += 1

# Función para implementar el algoritmo de Kruskal
def kruskal(graph, max_cost=False):
    mst = []  # Lista para almacenar las aristas del Árbol de Mínimo/Máximo Costo
    total_weight = 0  # Variable para almacenar el peso total del árbol
    disjoint_set = DisjointSet(graph.nodes())  # Inicializa los conjuntos disjuntos

    # Obtiene las aristas del grafo y las ordena por peso
    edges = list(graph.edges(data=True))
    edges.sort(key=lambda x: x[2]['weight'], reverse=max_cost)

    for u, v, data in edges:
        # Si los vértices 'u' y 'v' no están en el mismo conjunto, añadir la arista al árbol
        if disjoint_set.find(u) != disjoint_set.find(v):
            disjoint_set.union(u, v)
            mst.append((u, v, data['weight']))
            total_weight += data['weight']

    return mst, total_weight  # Devuelve las aristas del árbol y su peso total

# Función para dibujar el grafo y el árbol generado
def draw_graph(graph, mst_edges, title):
    pos = nx.spring_layout(graph)  # Calcula la posición de los nodos para la visualización
    plt.figure(figsize=(10, 8))  # Configura el tamaño de la figura

    # Dibuja el grafo original
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=15)
    labels = nx.get_edge_attributes(graph, 'weight')  # Obtiene los pesos de las aristas
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)  # Dibuja las etiquetas de los pesos

    # Resalta el Árbol de Mínimo o Máximo Costo
    mst_graph = nx.Graph()
    mst_graph.add_weighted_edges_from(mst_edges)
    nx.draw_networkx_edges(graph, pos, edgelist=mst_graph.edges(), width=2.0, edge_color='r')  # Dibuja las aristas del árbol en rojo
    
    plt.title(title)  # Añade un título a la figura
    plt.show()  # Muestra la figura

# Crear un grafo y añadir aristas con pesos
G = nx.Graph()
edges = [
    ('A', 'B', 1),  # Arista entre A y B con peso 1
    ('A', 'C', 4),  # Arista entre A y C con peso 4
    ('B', 'C', 2),  # Arista entre B y C con peso 2
    ('B', 'D', 5),  # Arista entre B y D con peso 5
    ('C', 'D', 3)   # Arista entre C y D con peso 3
]
G.add_weighted_edges_from(edges)  # Añade las aristas al grafo

# Encontrar el Árbol de Mínimo Costo usando el algoritmo de Kruskal
mst_edges, total_weight_mst = kruskal(G)
print(f"Peso total del Árbol de Mínimo Costo: {total_weight_mst}")  # Imprime el peso total del árbol
print("Aristas del Árbol de Mínimo Costo:")  # Imprime las aristas del árbol
for frm, to, weight in mst_edges:
    print(f"{frm} - {to}: {weight}")

# Dibujar el grafo y el Árbol de Mínimo Costo
draw_graph(G, mst_edges, "Árbol de Mínimo Costo usando el algoritmo de Kruskal")

# Encontrar el Árbol de Máximo Costo usando el algoritmo de Kruskal
max_cost_edges, total_weight_max = kruskal(G, max_cost=True)
print(f"Peso total del Árbol de Máximo Costo: {total_weight_max}")  # Imprime el peso total del árbol
print("Aristas del Árbol de Máximo Costo:")  # Imprime las aristas del árbol
for frm, to, weight in max_cost_edges:
    print(f"{frm} - {to}: {weight}")

# Dibujar el grafo y el Árbol de Máximo Costo
draw_graph(G, max_cost_edges, "Árbol de Máximo Costo usando el algoritmo de Kruskal")
