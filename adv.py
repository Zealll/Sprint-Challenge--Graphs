from room import Room
from player import Player, Queue
from world import World

import random
from ast import literal_eval
import time

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def traverse(player, moves_cue):
    # init queue
    q = Queue()
    # init set for visited rooms
    visited = set()
    # add current room to queue
    q.enqueue([player.current_room.id])
    # if queue is bigger than 0 there are things to explore
    while q.size() > 0:
        # as path is explored removefrom queue
        path = q.dequeue()
        # keep track of last room visited
        last_room = path[-1]
        # if the last room was not in previously visited
        if last_room not in visited:
            # add to list of visited
            visited.add(last_room)
            # Find all the exits for the room
            for exit in graph[last_room]:
                # if we find an exit in the room that is unexplored
                if graph[last_room][exit] == "?":
                    # add path to list to explore
                    return path
                    # otherwise remove path as already explored
                else:
                    # print('PAAAATH', path)
                    lost = list(path)
                    lost.append(graph[last_room][exit])
                    q.enqueue(lost)
    return []


def move(player, moves_q):
    current_exits = graph[player.current_room.id]
    # print(current_exits)
    untried_exits = []
    for direction in current_exits:
        if current_exits[direction] == "?":
            untried_exits.append(direction)
    if len(untried_exits) == 0:
        unexplored = traverse(player, moves_q)
        room_num = player.current_room.id
        temp ={}
        for next in unexplored:
            temp[next] = next
        for direction in graph[room_num]:
            if graph[room_num][direction] in temp:
                moves_q.enqueue(direction)
                room_num = temp[next]
                break
    else:
        moves_q.enqueue(untried_exits[random.randint(0, len(untried_exits) - 1)])


will_not_give_up = True
max_moves = 960
start = time.time()

while will_not_give_up:
    
    player = Player(world.starting_room)
    graph = {}
    # print(player.current_room.name)

    new_room = {}
    for direction in player.current_room.get_exits():
        new_room[direction] = "?"
        # print(new_room)
    graph[world.starting_room.id] = new_room
    # print(graph[world.starting_room.id])

    queue = Queue()
    total_moves = []
    move(player, queue)

    reverse_compass = {"n": "s", "s": "n", "e": "w", "w": "e"}

    while queue.size() > 0:
        init_prev_room = player.current_room.id
        dir = queue.dequeue()
        # print(dir. curr)
        player.travel(dir)
        total_moves.append(dir)
        next_room = player.current_room.id
        # print(next_room, init_prev_room)
        graph[init_prev_room][dir] = next_room
        # print(graph[init_prev_room], dir)
        if next_room not in graph:
            graph[next_room] = {}
            for exit in player.current_room.get_exits():
                graph[next_room][exit] = "?"
        # print(init_prev_room)
        graph[next_room][reverse_compass[dir]] = init_prev_room
        # print(graph[next_room])
        if queue.size() == 0:
            move(player, queue)
    if len(total_moves) < max_moves:
        traversal_path = total_moves
        max_moves = len(total_moves)
        will_not_give_up = False
        
end = time.time()
print(end - start)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
