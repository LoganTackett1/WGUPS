from util import populateUpperTriange
from hashTable import HashTable
from postal import Package, Truck
import datetime

my_destination_array = ["A","B","C","D","E"]
my_adjacency_matrix = [[0,0,0,0,0],
                       [5,0,0,0,0],
                       [1,2,0,0,0],
                       [12,11,6,0,0],
                       [1,3,4,5,0]]

my_populated_matrix = populateUpperTriange(my_adjacency_matrix)
