import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways

infinity = sys.maxsize

n, l, e = [int(i) for i in raw_input().split()]
links = []
for i in xrange(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in raw_input().split()]
    links.append((n1, n2))

exits = []
for i in xrange(e):
    ei = int(raw_input())# the index of a gateway node
    exits.append(ei)

def is_linked_by(node, link):
    l_from, l_to = link
    return node == l_from or node == l_to

def get_link_to(node, link):
    if not is_linked_by(node, link):
        raise Exception("{0} is not linked by {1}".format(node, link))
    l_from, l_to = link
    return l_to if l_from == node else l_from

def fill_distances(start, end, links, node_infos, visited):
    q = [start]
    while len(q) > 0:
        current = q[-1]
        del q[-1]

        neighbors = []
        for link in links:
            if not is_linked_by(current, link):
                continue
            neighbor = get_link_to(current, link)
            if neighbor in visited:
                continue
            neighbors.append(neighbor)

        for neighbor in neighbors:
            node_infos[neighbor] = min(node_infos[neighbor], node_infos[current] + 1)

        visited.append(current)
        q += neighbors

def find_shortest_path(start, end, links, nodes):
    # init
    node_infos = { }
    for node in nodes:
        node_infos[node] = infinity
    node_infos[start] = 0

    # traverse
    fill_distances(start, end, links, node_infos, [])

    # backtrack
    path = []
    current = end
    if node_infos[current] == infinity:
        return None
    while node_infos[current] > 0:
        min_neighbor, min_distance = None, infinity
        for link in links:
            if not is_linked_by(current, link):
                continue

            neighbor = get_link_to(current, link)
            distance = node_infos[neighbor]
            if distance < min_distance:
                min_neighbor, min_distance = neighbor, distance

        path.append((current, min_neighbor))
        current = min_neighbor

    # result
    return list(path)

def get_nodes(links):
    nodes = []
    for a,b in links:
        nodes.append(a)
        nodes.append(b)
    return list(set(nodes))

def remove_link(link, links):
    if link in links:
        links.remove(link)
        return
    l1,l2 = link
    link2 = l2,l1
    if link2 in links:
        links.remove(link2)
        return

nodes = get_nodes(links)
# game loop
while True:
    si = int(raw_input())
    shortest_paths = []
    for ei in exits:
        shortest_path = find_shortest_path(si, ei, links, nodes)
        if shortest_path != None:
            shortest_paths.append(shortest_path)

    shortest_paths = sorted(shortest_paths, key=lambda l:len(l))
    link_to_severe = shortest_paths[0][-1]
    print(str(link_to_severe[0]) + " " + str(link_to_severe[1]))
    remove_link(link_to_severe, links)
