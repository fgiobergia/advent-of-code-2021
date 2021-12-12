import networkx as nx

def visit(G, visited_list, current_pos, currently_visited, twice):
    if current_pos == "end":
        # print(currently_visited)
        if currently_visited not in visited_list:
            visited_list.append(currently_visited)
        return
    
    for neighbor in G.adj[current_pos]:
        if (neighbor.islower() and neighbor not in currently_visited) or neighbor.isupper():
            # can visit, go there!
            visit(G, visited_list, neighbor, currently_visited + [ neighbor ], twice)
        elif not twice and neighbor.islower() and neighbor in currently_visited and neighbor != "start":
            # use "visit twice" token
            visit(G, visited_list, neighbor, currently_visited + [ neighbor ], True)


if __name__ == "__main__":
    with open("day12.input") as f:
        lines = [ l.strip().split("-") for l in f.readlines() ]
    
    G = nx.Graph()
    for a,b in lines:
        G.add_edge(a,b)
    
    visited_list = []
    visit(G, visited_list, "start", ["start"], True)
    print(len(visited_list))
    
    visited_list = []
    visit(G, visited_list, "start", ["start"], False)
    print(len(visited_list)) # sit back, relax, and enjoy the wait