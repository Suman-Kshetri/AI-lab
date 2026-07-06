import tkinter as tk 
from heapq import  heappush,heappop

goal = (
    (1,2,3),
    (4,5,6),
    (7,8,0)
)

start = (
    (0,1,3),
    (4,2,6),
    (7,5,8)
)

def misplaced_tiles(state):
    count = 0 
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                count = count+1
    return count 

def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                goal_row = (state[i][j]-1)//3
                goal_col = (state[i][j]-1)%3
                distance += abs(i-goal_row) + abs(j-goal_col)
    return distance           

def combined_heuristic(state):
    comb_heuristic = misplaced_tiles(state)+manhattan_distance(state)
    return comb_heuristic

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i,j

def get_neighbours(state):
    x,y = find_blank(state)
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    neighbours = []
    for dx,dy in moves: 
        nx = x + dx      # new x //nx 
        ny = y + dy 
        if 0 <=nx < 3 and 0 <= ny < 3:
            board = [list(row) for row in state]
            board[x][y] , board[nx][ny] = board[nx][ny], board[x][y]
            neighbours.append(tuple(map(tuple,board)))
    
    return neighbours

print(get_neighbours(start))   
def reconstruct(parent,current):
    path = []
    while current is not None: 
        path.append(current)
        current = parent[current]
    return path[::-1]

def astar(start,heuristic):
    pq = []
    heappush(pq,(heuristic(start),0,start)) # fn, gn , state
    parent = {start:None}
    g_cost = {start:0}
    expanded = 0 
    while pq:
        f,g, current = heappop(pq)
        expanded = expanded + 1
        if current == goal:
            return reconstruct(parent,current),expanded

        for neighbor in get_neighbours(current):
            new_g  = g + 1
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                f_cost = new_g + heuristic(neighbor) # cost = f(n)+g(n)
                
                heappush(
                    pq,
                    (f_cost,new_g,neighbor)
                )
                parent[neighbor] = current
    return None,expanded

# path,expanded = astar(start,misplaced_tiles)


root = tk.Tk()
root.title("8 puzzle solver")
# up to here no thing will appear , appear and closes instantaneouly 
# you need mainloop to show the window 
buttons = []
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(root,width=10,height=6)
        btn.grid(row=i,column=j)
        row.append(btn)
    buttons.append(row)


def draw_board(state):
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            
            if value == 0:
                buttons[i][j]["text"] = ""
            else:
                buttons[i][j]["text"] =  value
                          
draw_board(start)

index = 0 
path = []
expanded = [] 



def animate():
    global index 
    
    if index < len(path):
        draw_board(path[index])
        index+=1
        root.after(1000,animate) 

def solve():
    global path,expanded,index
    path,expanded = astar(start,misplaced_tiles)
    index = 0 
    animate()

solve_button = tk.Button(root,text="Solve",command=solve)
solve_button.grid(row=3,column=0,columnspan=3)
root.mainloop()