import sys
import math
import Queue

def debug(msg):
    print >> sys.stderr, str(msg)

class Node:
    def __init__(self, elevators_left, distance, direction, action, floor, pos, prev_node, match_floor, match_pos):
        self.elevators_left = elevators_left
        self.distance = distance
        self.direction = direction
        self.floor = floor
        self.pos = pos
        self.prev_node = prev_node
        self.action = action
        self.match_floor = match_floor
        self.match_pos = match_pos

def get_next_step(pos, direction, target_pos, current_distance):
    same_direction = pos <= target_pos and direction == "RIGHT"
    same_direction |= pos >= target_pos and direction == "LEFT"

    next_action = "WAIT" if same_direction or pos == target_pos else "BLOCK"
    next_direction = direction if same_direction else ("RIGHT" if direction == "LEFT" else "LEFT")
    next_distance = current_distance + abs(target_pos - pos) + (0 if same_direction else 3)

    return (next_action, next_direction, next_distance)

def backtrack(finish_node):
    if finish_node == None:
        raise Exception("Unable to find optimal path")
    current = finish_node
    result = []
    while current != None:
        result.append((current.match_floor, current.match_pos, current.action, current.distance))
        current = current.prev_node

    return list(reversed(result))[1:]

def filter_exits(pos, exits):
    # return exits
    first_right = sorted([x for x in exits if x > pos])[:1]
    first_left = sorted([x for x in exits if x < pos], reverse=True)[:1]
    same = [x for x in exits if x == pos]
    return first_left + same + first_right

def find_path(start_floor, start_pos, exit_floor, exit_pos, floors_map, total_elevators):
    q = Queue.Queue()

    distances = {}

    finish_node = None
    root = Node(total_elevators, 0, "RIGHT", "WAIT", start_floor, start_pos, None, start_floor, start_pos,)
    q.put(root)
    while not q.empty():
        current = q.get()
        floor = current.floor
        pos = current.pos
        direction = current.direction
        distance = current.distance
        elevators_left = current.elevators_left

        key = floor, pos, direction, elevators_left
        if key in distances:
            existing_distance = distances[key]
            if existing_distance < distance:
                continue
        distances[key] = distance

        # finish node
        if pos == exit_pos and floor == exit_floor:
            if finish_node == None:
                finish_node = current
            else:
                finish_node = current if distance < finish_node.distance else finish_node
            continue

        # probe all exits

        exits = [exit_pos] if floor == exit_floor else (filter_exits(pos, floors_map[floor]) if floor in floors_map else [])
        if pos in exits:
            exits = [pos]
        for ex in exits:
            next_action, next_direction, next_distance = get_next_step(pos, direction, ex, distance)
            q.put(Node(elevators_left, next_distance, next_direction, next_action, floor + 1, ex, current, floor, pos))

        # probe elevator
        if elevators_left > 0:
            next_distance = distance + 3
            q.put(Node(elevators_left - 1, next_distance, direction, "ELEVATOR", floor + 1, pos, current, floor, pos))
        
        # probe additional elevators
        if elevators_left > 0:
            elevator_poss = [exit_pos]
            for ex in filter_exits(pos, exits):
                elevator_poss.append(ex - 1)
                elevator_poss.append(ex + 1)
            elevator_poss = list(set(elevator_poss))
            temp = list(elevator_poss)
            elevator_poss = []
            for t in temp:
                if t == pos:
                    continue
                if t <= 0:
                    continue
                if t >= width:
                    continue
                elevator_poss.append(t)
            elevator_poss = filter_exits(pos, elevator_poss)

            for elevator_pos in elevator_poss:
                next_action, next_direction, next_distance = get_next_step(pos, direction, elevator_pos, distance)
                walk = Node(elevators_left, next_distance, next_direction, next_action, floor + 1, elevator_pos, current, floor, pos)
                q.put(Node(elevators_left - 1, walk.distance + 3, walk.direction, "ELEVATOR", floor + 1, elevator_pos, walk, floor, elevator_pos))

    # backtrack
    return backtrack(finish_node)

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = [int(i) for i in raw_input().split()]
floors_map = { }
for i in xrange(nb_elevators):
    elevator_floor, elevator_pos = [int(j) for j in raw_input().split()]
    if elevator_floor in floors_map:
        floors_map[elevator_floor].append(elevator_pos)
    else:
        floors_map[elevator_floor] = [elevator_pos]

optimal_path = None

# game loop
while True:
    clone_floor, clone_pos, direction = raw_input().split()
    clone_floor = int(clone_floor)
    clone_pos = int(clone_pos)
    
    if optimal_path == None:
        optimal_path = find_path(clone_floor, clone_pos, exit_floor, exit_pos, floors_map, nb_additional_elevators)
        debug("Calculated optimal path to: " + str(optimal_path))
    
    if direction == "NONE" or len(optimal_path) == 0:
        print "WAIT"
        continue

    (floor, pos, action, distance) = optimal_path[0]
    if clone_floor == floor and clone_pos == pos:
        debug("Executing and deleting action {0}".format(action))
        del optimal_path[0]
        print action
    else:
        print "WAIT"

    debug("Left to go: {0}".format(optimal_path))
