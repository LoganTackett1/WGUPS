# Takes in an adjacency matrix as turns it into an all-pairs shortest path matrix for the graph.
def FloydWarshallAllPairsShortestPath(matrix):
    numVertices = len(matrix)
    for k in range(numVertices):
        for toIndex in range(numVertices):
            for fromIndex in range(numVertices):
                currentLength = matrix[fromIndex][toIndex]
                possibleLength = matrix[fromIndex][k] + matrix[k][toIndex]
                if possibleLength < currentLength:
                    matrix[fromIndex][toIndex] = possibleLength
    return matrix

# key_f is a function that maps start and items from list to their vertex number.
# ex: start and list are package ids, key_f can map package id's to their destinations vertex number.
def nearestNeighbor(start,list,key_f,matrix):
    sorted = []
    curr = start
    while len(list) != 0:
        curr_label = key_f(curr)

        min_item = None
        min_dist = float('inf')
        for item in list:
            item_label = key_f(item)
            if matrix[curr_label][item_label] < min_dist:
                min_item = item
                min_dist = matrix[curr_label][item_label]
        sorted.append(min_item)
        curr = min_item
        list.remove(min_item)
    return sorted

#used to take the distance table and turn it into a symmetrical matrix.
#used in preparing distance table for all-pairs shortest path calculation
def populateUpperTriange(matrix):
    for i in range(len(matrix)-1):
        for j in range(1,len(matrix)):
            matrix[i][j] = matrix[j][i]

