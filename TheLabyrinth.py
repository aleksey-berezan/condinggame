import sys
import math
import Queue

def debug(msg):
    print >> sys.stderr, msg

# r: number of rows.
# c: number of columns.
# a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
r, c, a = [int(i) for i in raw_input().split()]

debug("r={0}, c={1}, a = {2}".format(r,c,a))

def set_min_distance(distances, location, value):
    if location in distances:
        current = distances[location]
        if current > value:
            distances[location] = value
            return True
        else:
            return False
        #distances[location] = min(distances[location], value)
    else:
        distances[location] = value
        return True

def get_distance(distances, location):
    if location in distances:
        return distances[location]
    else:
        return None;

def in_bounds(maze, location):
    nr, nc = location
    if nr <= 0 or nc <= 0:
        return False
    rr = len(maze)
    cc = len(maze[0])    
    return nr < rr and nc < cc

def get_navigatable_neighbors(maze, current):
    cr, cc = current
    
    neighbors = []
    for rv, cv in [(0, +1), (0, -1), (+1, 0), (-1, 0)]:
        nr = cr + rv
        nc = cc + cv
        if not in_bounds(maze, (nr, nc)):
            continue
        if maze[nr][nc] == '#':
            continue
        neighbors.append((nr, nc))
    if len(neighbors) == 0:
        debug("Unable to find navigatable neighbors of " + str(current))
    return neighbors

def trace_back(maze, distances, finish, start): 
    current = finish
    cr, cc = current
    result = []
    
    min_distance = sys.maxsize
    while True:
        cr, cc = current
        result.append(current)
        if get_distance(distances, current) == 0:
            break

        min_location = None        
        for rv, cv in [(0, +1), (0, -1), (+1, 0), (-1, 0)]:
            nr = cr + rv
            nc = cc + cv
            next = nr, nc
            if not in_bounds(maze, next):
                continue
            
            if maze[nr][nc] == '#':
                continue
            d = get_distance(distances, next)
            if d == None:
                continue
            if d > min_distance:
                continue
            min_distance = d
            min_location = (nr, nc)

        if min_location == None:
            raise Exception("Unable to find next distance from " + str(current))
        current = min_location
    return list(reversed(result))

def find_nearest(maze, start, predicate):
    cr, cc = current = start
    distances = { current: 0 }
    visited = {}

    q = Queue.Queue()
    q.put(start)

    while not q.empty():
        current = q.get()
        visited[current] = None
        cr, cc = current
        if predicate(maze[cr][cc]):
            shortest_path = trace_back(maze, distances, current, start)
            return shortest_path[1]

        neighbors = get_navigatable_neighbors(maze, current)
        
        current_distance = get_distance(distances, current)
        for neighbor in neighbors:
            # if neighbor in visited:
            #     continue
            updated = set_min_distance(distances, neighbor, current_distance + 1)
            if updated:
                q.put(neighbor)

    return None

# game loop
mode = 'explore' # explore_C_seen,
while True:
    # kr: row where Kirk is located.
    # kc: column where Kirk is located.
    kr, kc = [int(i) for i in raw_input().split()]

    # init maze
    maze = [None] * r    
    for i in xrange(r):
        row = raw_input()  # C of the characters in '#.TC?' (i.e. one line of the ASCII maze).
        maze[i] = list(row)
        row_str = str(row)
        row_str = list(row)
        if mode == 'explore':
            for c in row_str:
                if c == 'C':
                    mode = 'explore_C_seen'
                    break

        if i == kr:            
            row_str[kc] = 'K'
        row_str = "".join(row_str)
            
        debug("{0:>2d}: {1}".format(i, row_str))
        
    if maze[kr][kc] == 'C':
        mode = 'C_triggered'
    
    debug("Mode is " + mode)
    if mode == 'explore':
        nkr, nkc = find_nearest(maze, (kr, kc), lambda cell_content: cell_content == '?')
    elif mode == 'explore_C_seen':
        temp = find_nearest(maze, (kr, kc), lambda cell_content: cell_content == 'C')
        if temp == None:
            temp = find_nearest(maze, (kr, kc), lambda cell_content: cell_content == '?')
            nkr, nkc = temp
        else:
            nkr, nkc = temp
            mode = 'C_found'
    elif mode == 'C_found':
        nkr, nkc = find_nearest(maze, (kr, kc), lambda cell_content: cell_content == 'C')
    elif mode == 'C_triggered':
        nkr, nkc = find_nearest(maze, (kr, kc), lambda cell_content: cell_content == 'T')

    debug("Current={0}, next={1}".format((kr, kc), (nkr, nkc)))

    if nkr > kr:
        print "DOWN"
    elif nkr < kr:
        print "UP"
    elif nkc > kc:
        print "RIGHT"
    elif nkc < kc:
        print "LEFT"
    else: print "UNKNOWN " + str((kr, kc)) + " / " + str((nkr, nkc))