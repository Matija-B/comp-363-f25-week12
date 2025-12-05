import copy

# 12345678901234567890123456789012345678901234567890123456789012345678901234567890
def find_path(graph: list[list[int]], source: int, target: int):
    """Return a path -- any path -- from source to target in the graph"""

    # Initialize return item
    path: list[int] = None

    # Make sure inputs are ok
    if graph is not None:
        n: int = len(graph)
        if n > 0 and (0 <= source < n) and (0 <= target < n):

            # Initialize DFS tools
            no_edge: int = graph[0][0]  # absence of edge
            marked: list[int] = [source]  # vertices already processed
            found: bool = False  # Flags detection of path

            # What vertex to explore next and what is the path
            # to it. The information is stored as a tuple in
            # the form:
            #  (vertex, path_to_this_vertex)
            # with path_to_this_vertex being a list of the
            # vertices alonγ the path.
            stack: list[(int, list[int])] = [(source, [source])]

            while len(stack) > 0 and not found:
                # Explore the next vertex from the stack
                (u, path_from_source_to_u) = stack.pop()
                found = (u == target)
                if found:
                    # u is the end of the path, so we got what we are 
                    # looking for
                    path = path_from_source_to_u
                else:
                    # Explore the neighbors of u, hopefully one of them
                    # will get us a stop closer to the target vertex.
                    v: int = n - 1
                    while v >= 0:
                        if graph[u][v] != no_edge and v not in marked:
                            marked.append(v)
                            stack.append((v, path_from_source_to_u + [v]))
                        v -= 1
    return path


def ford_fulkerson(graph, source, target):
    
    residual = copy.deepcopy(graph)
    max_flow = 0
    #When we first start the loop we can allow it to start right away
    #and that is why we give it that it is true
    while True:
        #Then we want to call our helper method that will help us 
        #find the path from the source to the target that we give 
        #and it will give it to us in a list. 
        isPath = find_path(residual, source, target)
        #We then want to first check if there was a path 
        #If there wasent then we break the cycle. 
        if isPath is None:
            break
        
        #We then want to find the capacity at the first edge. 
        m = residual[isPath[0]][isPath[1]]
        for i in range(len(isPath) - 1):
            u = isPath[i]
            v = isPath[i + 1]
            #We then check if the new capacity is less then the old one
            #and then store the new capacity. 
            if residual[u][v] < m:
                m = residual[u][v]
            #We then want to add that in our max_flow
        max_flow = max_flow + m
        #When we finally finish our first step we want to then 
        #updates our residual capacities 
        for i in range(len(isPath) - 1):
            u = isPath[i]
            v = isPath[i + 1]
            #Then we can see that if it is a foward edge 
            #We want to deacrease our edge
            residual[u][v] -= m
            #If its a bacwards edge we want to increase it.
            residual[v][u] += m

        
    return max_flow, residual

def min_cut(graph, residual, source):
   #This is when we want to find all the verticies 
   #that are reachable 
   S = []
   stack = [source]
    #We then want to continue on looking for our verticies until 
    #there is nothing left in the stack
   while stack:
        #We then a value from our stack
        u = stack.pop()
        for v in range(len(graph)):
            #Then we check if the pair is greater then zero 
            #but also still not in S
            #then we add it do our in S
            if residual[u][v] > 0 and v not in S:
                S.append(v)
                stack.append(v)
                
    
    #Then we want to build our other major component 
    #which is not the verticies that are not reachable
   T = []
   #we iterate through our graph
   for i in range(len(graph)):
    #then for every value that isn;t in S
    if i not in S:
        #we add it to T
        T.append(i)

    #Finally we want to make an empty list
    #to put in our edges
   edges = []

   for u in S:
    for v in T:
        #We then check if the graph from uv is not
        #the same as graph[0][0]
        if graph[u][v] != graph[0][0]:
            #If it isnt then we add the pair in our edge. 
            edges.append((u,v))
    
   return S, T, edges



G = [  #  A   B   C   D   E
    [0, 20, 0, 0, 0],  # A
    [0, 0, 5, 6, 0],  # B
    [0, 0, 0, 3, 7],  # C
    [0, 0, 0, 0, 8],  # D
    [0, 0, 0, 0, 0],  # E
]

max_flow, residual = ford_fulkerson(G, 0, 4)

S, T, min =  min_cut(G, residual, 0)

print("max_flow:", max_flow)
print(S)
print(T)
print(min)
