import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
from itertools import islice

G = nx.Graph()
G.add_edges_from([(1,2),(2,3),(1,4),(3,5),(2,5),(4,5),(3,6),(4,6)])
nx.draw_networkx(G)

for i in range(1,7):
    for j in range(1,7):
        paths = nx.shortest_simple_paths(G,i,j)
        p = list(islice(paths,5))
        sum = 0
        for path in p:
            sum += len(path)
        print(sum)

#plt.show()  
