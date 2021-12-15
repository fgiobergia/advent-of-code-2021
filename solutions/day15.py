import networkx as nx
import numpy as np

def min_dist(m):

    G = nx.DiGraph()
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            for a,b in [(-1,0),(+1,0),(0,-1),(0,+1)]:
                if 0 <= i+a < m.shape[0] and 0 <= j+b < m.shape[1]:
                    G.add_edge((i+a,j+b), (i,j), weight=m[i,j])
    
    return nx.shortest_path_length(G, (0,0), (m.shape[0]-1, m.shape[1]-1), "weight")



if __name__ == "__main__":
    with open("day15.input") as f:
        m = np.array([ list(map(int, l.strip())) for l in f.readlines() ])
    
    print(min_dist(m))

    x = np.hstack([ ((m + (i-1)) % 9) + 1 for i in range(5) ]) 
    y = np.vstack([ ((x + (i-1)) % 9) + 1 for i in range(5) ])

    print(min_dist(y))