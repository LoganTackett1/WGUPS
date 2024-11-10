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
# start is assumed to be the index of the location in the adjacency matrix and not an item id.
def nearestNeighbor(start,list,key_f,matrix):
    sorted = []
    curr_label = start
    while len(list) != 0:
        min_item = None
        min_dist = float('inf')
        for item in list:
            item_label = key_f(item)
            if matrix[curr_label][item_label] < min_dist:
                min_item = item
                min_dist = matrix[curr_label][item_label]
        sorted.append(min_item)
        curr_label = key_f(min_item)
        list.remove(min_item)
    return sorted

#used to take the distance table and turn it into a symmetrical matrix.
#used in preparing distance table for all-pairs shortest path calculation
def populateUpperTriange(matrix):
    for i in range(len(matrix)-1):
        for j in range(1,len(matrix)):
            matrix[i][j] = matrix[j][i]
    return matrix

#merge sort will use key_f to map package id's to their deadline
def merge(items,i,j,k,key_f):
    merged_size = k - i + 1
    merged_items = []
    for l in range(merged_size):
        merged_items.append(0)
    
    merge_pos = 0
    left_pos = i
    right_pos = j + 1

    while left_pos <= j and right_pos <= k:
        if key_f(items[left_pos]) < key_f(items[right_pos]):
            merged_items[merge_pos] = items[left_pos]
            left_pos += 1
        else:
            merged_items[merge_pos] = items[right_pos]
            right_pos += 1
        merge_pos += 1

    while left_pos <= j:
        merged_items[merge_pos] = items[left_pos]
        left_pos += 1
        merge_pos += 1

    while right_pos <= k:
        merged_items[merge_pos] = items[right_pos]
        right_pos += 1
        merge_pos += 1

    merge_pos = 0
    while merge_pos < merged_size:
        items[i + merge_pos] = merged_items[merge_pos]
        merge_pos += 1

#merge sort, O(nlogn) will be used to sort packages in trucks by deadline.
def merge_sort(items,i,k,key_f):
    j = 0
    if i < k:
        j = (i + k) // 2

        merge_sort(items,i,j,key_f)
        merge_sort(items,j + 1,k,key_f)

        merge(items,i,j,k,key_f)
