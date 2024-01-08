

import sys
from math import sin, cos, sqrt, atan2, radians

# stores road and their neighbors information
nodes = {}


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


# main program
def main():
    filename = input("Enter file name: ")
    # filename = "memphis-medium.txt"

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
    

    while True:
        print()
        nxtCmd = input("Enter a location ID or 0 to quit: ")
        if (nxtCmd == "0"):
            return
        
        if (nxtCmd in nodes):
            roadData = nodes[nxtCmd]
        
            rloc = roadData[0]

            print(f"Location {nxtCmd} has roads leading to:")

            for neighbor in roadData[1]:
                nloc = nodes[neighbor][0]
                dist = distance(rloc, nloc)
                cspd = roadData[1][neighbor][1]
                nspd = int(cspd)*1.60934/3600
                time = dist/nspd
                rname = roadData[1][neighbor][0].strip("\n")

                print(f"Location {neighbor}, {cspd} mph, {rname}, {time} seconds")
        else:
            print("Node not found!")
            

            
    
if __name__ == "__main__":
    main()
    






            
