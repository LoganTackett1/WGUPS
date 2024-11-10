from util import populateUpperTriange, FloydWarshallAllPairsShortestPath, merge_sort
from hashTable import HashTable
from postal import Package, Truck
import datetime

my_destination_array = ["A","B","C","D","E"]
my_adjacency_matrix = [[0,0,0,0,0],
                       [5,0,0,0,0],
                       [1,2,0,0,0],
                       [12,11,6,0,0],
                       [1,3,4,5,0]]

populateUpperTriange(my_adjacency_matrix)
FloydWarshallAllPairsShortestPath(my_adjacency_matrix)
print(my_adjacency_matrix)
[[0, 3, 1, 6, 1], 
 [3, 0, 2, 8, 3], 
 [1, 2, 0, 6, 2], 
 [6, 8, 6, 0, 5], 
 [1, 3, 2, 5, 0]]
def ezPackage(id,address,deadline):
    return Package(id,address,deadline,"1","1","1","1","1")

my_truck = Truck()
my_packages = [ezPackage(2,"B",datetime.time(10,30)),ezPackage(1,"A",datetime.time(10,30)),ezPackage(3,"C",datetime.time(11,30)),ezPackage(4,"D",datetime.time(10,30)),ezPackage(5,"E",datetime.time(12,30)),ezPackage(6,"A",datetime.time(10,30)),ezPackage(7,"B",datetime.time(11,30)),ezPackage(8,"C",datetime.time(12,30)),ezPackage(9,"D",datetime.time(12,30)),ezPackage(10,"E",datetime.time(12,30)),ezPackage(11,"A",datetime.time(11,30))]
my_hash_table = HashTable(10)
for package in my_packages:
    my_hash_table.insertPackage(package)
my_truck.loadPackages(my_packages)
for i in range(len(my_truck.packages)):
    package = my_hash_table.lookup(my_truck.packages[i])
    print(package.id,package.address,package.deadline)
my_truck.sortPackages(my_hash_table,my_adjacency_matrix,my_destination_array)
print("NEXT")
for i in range(len(my_truck.packages)):
    package = my_hash_table.lookup(my_truck.packages[i])
    print(package.id,package.address,package.deadline)
