import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image

G = nx.Graph()
G.add_edges_from([(1,2),(2,3),(1,4),(3,5),(2,5),(4,5),(3,6),(4,6)])
nx.draw_networkx(G)
print(nx.has_path(G,1,5))
#def path(s,d):
 #   n = nx.neighbors()
paths = nx.all_simple_paths(G,3,4)
for path in paths:
    print(path)
plt.show()  

im = Image.open("Figure_1.png")
im.show()