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