import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
n, l, e = [int(i) for i in raw_input().split()]
links = []
for i in xrange(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in raw_input().split()]
    links.append((n1, n2))

exits = []
for i in xrange(e):
    ei = int(raw_input())  # the index of a gateway node
    exits.append(ei)

def find_shortest_path(start, end, links, acc, min_so_far):
    if start == end:
        min_so_far[0] = min(min_so_far[0], len(acc))
        return acc

    if min_so_far[0] < len(acc):
        return None

    results = []
    for link in links:
        l_from, l_to = link
        if l_from != start and l_to != start:
            continue
        l_to = l_to if l_from == start else l_from

        acc_copy = list(acc)
        acc_copy.append(link)
        links_copy = list(links)
        links_copy.remove(link)

        result = find_shortest_path(l_to, end, links_copy, acc_copy, min_so_far)
        if result == None:
            continue
        results.append(result)

    if len(results) == 0:
        return None

    sorted_results = sorted(results, key=lambda l:len(l))
    res = sorted_results[0]
    min_so_far[0] = min(min_so_far[0], len(res))
    return res

# game loop
while True:
    si = int(raw_input())
    shortest_paths = []
    limit = len(links)-1
    for ei in exits:
        shortest_path = find_shortest_path(si, ei, links, [], [limit])
        limit = min(len(shortest_path), limit) if shortest_path != None else limit
        if shortest_path != None:
            shortest_paths.append(shortest_path)

    shortest_paths = sorted(shortest_paths, key=lambda l:len(l))
    shortest_path = shortest_paths[0]
    link_to_severe = shortest_path[0]
    print(str(link_to_severe[0]) + " " + str(link_to_severe[1]))
    links.remove(link_to_severe)
    blocked_exits = list(exits)
    for ei in exits:
        for f,t in links:
            if f == ei or t == ei:
                blocked_exits.remove(ei)
                break
    for ei in blocked_exits:
        exits.remove(ei)

