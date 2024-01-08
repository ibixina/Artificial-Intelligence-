

import sys, heapq
from math import sin, cos, sqrt, atan2, radians

from dataclasses import dataclass, field
from typing import Any
from queue import PriorityQueue

debugging = False

# visitedNodes = []


totalNodesVisited = 0

@dataclass(order=True)
class PrioritizedItem:
	priority: int
	item: Any=field(compare=False)

class PQueue:
	def __init__(self):
		self.the_queue = PriorityQueue()
		
	def empty(self):
		return self.the_queue.empty()
		
	def enqueue(self, item, priority):
		self.the_queue.put(PrioritizedItem(priority, item))
		
	def dequeue(self):
		return self.the_queue.get().item
		
	def size(self):
		return self.the_queue.qsize()
		
	def debug_print(self):
		print(self.the_queue)

# stores road and their neighbors information
nodes = {}
reached = {}



frontier = PQueue()

heuristic = {}





class Node:
    def __init__(self,state, parentNode, cost, heuristic, move, name = ""):
        self.state = state
        self.parentNode = parentNode
        self.cost = cost
        self.heuristic = heuristic
        self.move = move
        self.name = name

        if (self.name != ""):
             self.name += ", "

        if self.move == "speeding":
            self.state[1] -= 1
            # self.heuristic = self.heuristic * 2
        if self.state[1] == 0:
            self.heuristic = self.heuristic*2
        # self.boosts = boosts

    def __str__(self) -> str:
        return f"{self.state} {self.move}"
    
        


# calculates distance given two points with lat and long
def distance(loc1, loc2):
    # Approximate radius of earth in km
    R = 6373.0

    lat1 = radians(float(loc1[0]))
    lon1 = radians(float(loc1[1]))
    lat2 = radians(float(loc2[0]))
    lon2 = radians(float(loc2[1]))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def straightDistance(loc1, loc2):
    diffa = float(loc1[0]) - float(loc2[0])
    diffb = float(loc1[1]) - float(loc2[1])
    return sqrt(diffa**2 + diffb**2)
     

def astar(start, goal, boosts):
    istate = [start, boosts]
    node = Node(istate, None, 0, heuristic[start], "Starting Location")
    # print(node.cost)
    
    frontier.enqueue(node, node.cost + node.heuristic)

    
    reached = {str(istate): node}
    global totalNodesVisited

    while not frontier.empty():
        # frontier.debug_print()
        node = frontier.dequeue()
        # visitedNodes.append(node.state[0])
        totalNodesVisited += 1
        if debugging:
             print()
             print(f"Visiting [State: {node.state}, Parent: {node.parentNode} , Cost: {node.cost}, Heuristic: {node.heuristic}]]")
        if node.state[0] == goal:
            # node.move = "Ending Location"
            return node
        nstate = node.state[1]
        
        # if node.move == "speeding":
        #     nstate = node.state[1] - 1
        
        neighbors = getNeighbors(node.state[0])

        if nstate > 0:
           
            tlist = []
            for neighbor in neighbors:
                addNeighbor = neighbor.copy()
                addNeighbor[3] = addNeighbor[3]/2
                addNeighbor[4] = "speeding"
                tlist += [addNeighbor]
            neighbors += tlist
                 
        for neighbor in neighbors:
            neighborNode = Node([neighbor[0], nstate], node, node.cost + neighbor[3], heuristic[neighbor[0]], neighbor[4], neighbor[2])
            if str(neighborNode.state) not in reached:
                reached[str(neighborNode.state)] = neighborNode
                frontier.enqueue(neighborNode, neighborNode.cost + neighborNode.heuristic)
                if debugging:
                    print(f"Adding [State: {neighborNode.state}, Parent: {neighborNode.parentNode} , Cost: {neighborNode.cost}, Heuristic: {neighborNode.heuristic}]]")

            else:
                if neighborNode.cost < reached[str(neighborNode.state)].cost:
                    reached[str(neighborNode.state)] = neighborNode
                    frontier.enqueue(neighborNode, neighborNode.cost + neighborNode.heuristic)
                    if debugging:
                        print(f"Adding [State: {neighborNode.state}, Parent: {neighborNode.parentNode} , Cost: {neighborNode.cost}, Heuristic: {neighborNode.heuristic}]]")
                elif neighborNode.cost > reached[str(neighborNode.state)].cost:
                    if debugging:
                        print(f"Skipping [State: {neighborNode.state}, Parent: {neighborNode.parentNode} , Cost: {neighborNode.cost}, Heuristic: {neighborNode.heuristic}]]")
    return None
                  
             
        
         



# main program
def main():
    # filename = input("Enter file name: ")
    filename = "memphis-medium.txt"

    # read the file and store the information
    with open(filename, "r") as file:
        data = file.readlines()

        for line in data:
            linedata = line.split('|')
            if (linedata[0] == "location"):
                nodeId = linedata[1]
                nodeLoc = linedata[2:]
            
                nodes[nodeId] = [nodeLoc, {}]
            if (linedata[0] == "road"):
                road1 = linedata[1]
                road2 = linedata[2]
                spd = linedata[3]
                name = linedata[4]

                nodes[road1][1][road2] = [name, spd]
                nodes[road2][1][road1] = [name, spd]
    

    startLocation = input("Enter a starting location ID: ")
    endLocation = input("Enter an ending location ID: ")
    boostno = int(input("How many times are you allowed to speed? "))
    debugData = input("Do you want debugging information? (y/n): ")
    if (debugData.lower() == "y"):
        debugging = True

    generateHeuristic(endLocation)
    # print(heuristic)

    result = astar(startLocation, endLocation, boostno)
    currentNode = result
    totalCost = currentNode.cost
    print("Total travel time in seconds: "+str(totalCost))
    res = []
    while currentNode != None:
        # print(f"{currentNode.state[0]} {currentNode.name} ({str(currentNode.move)})")
        res = [f"{currentNode.state[0]} ({currentNode.name}{str(currentNode.move)})"] + res
        currentNode = currentNode.parentNode
    print("Total Nodes Visited: "+str(totalNodesVisited))
    print()
    if (res):
        print("Route found is: ")
        print("\n".join(res))
    else:
         print("No route found")
        



def getNeighbors(node):
    roadData = nodes[node]
        
    rloc = roadData[0]
    response = []

    # print(f"Location {node} has roads leading to:")

    for neighbor in roadData[1]:
        nloc = nodes[neighbor][0]
        dist = distance(rloc, nloc)
        cspd = roadData[1][neighbor][1]
        nspd = float(cspd)*1.60934/3600
        time = dist/nspd
        rname = roadData[1][neighbor][0].strip("\n")

        # print(f"Location {neighbor}, {cspd} mph, {rname}, {time} seconds")
        response += [[neighbor, cspd, rname, time, "not speeding"]]
    return response



def generateHeuristic(end):
    endLoc = nodes[end][0]
    maxspd = 65 * 2
    for node in nodes:
        nodeLoc = nodes[node][0]
        dist = distance(nodeLoc, endLoc)
        heuristic[node] = dist/(maxspd*1.60934/3600)
    # print(heuristic)



    
if __name__ == "__main__":
    main()
    






            
