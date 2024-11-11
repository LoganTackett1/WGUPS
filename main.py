from util import populateUpperTriange, FloydWarshallAllPairsShortestPath, merge_sort
from hashTable import HashTable
from postal import Package, Truck, loadTrucks, printAllTrucksStatus, loadWrongAddressPackages
import datetime

my_destination_array = ["A","B","C","D","E"]
my_adjacency_matrix = [[0,0,0,0,0],
                       [5,0,0,0,0],
                       [1,2,0,0,0],
                       [12,11,6,0,0],
                       [1,3,4,5,0]]

populateUpperTriange(my_adjacency_matrix)
FloydWarshallAllPairsShortestPath(my_adjacency_matrix)
[[0, 3, 1, 6, 1], 
 [3, 0, 2, 8, 3], 
 [1, 2, 0, 6, 2], 
 [6, 8, 6, 0, 5], 
 [1, 3, 2, 5, 0]]
def ezPackage(id,address,deadline,note=None):
    return Package(id,address,deadline,"1","1","1",note)

my_packages = [ezPackage(1,"B",datetime.datetime(2024,11,10,10,30),"Wrong Address Listed"),ezPackage(2,"A",datetime.datetime(2024,11,10,10,30)),ezPackage(3,"C",datetime.datetime(2024,11,10,11,30),"note"),ezPackage(4,"D",datetime.datetime(2024,11,10,10,30)),ezPackage(5,"E",datetime.datetime(2024,11,10,12,30)),ezPackage(6,"A",datetime.datetime(2024,11,10,10,30),"note"),ezPackage(7,"B",datetime.datetime(2024,11,10,11,30)),ezPackage(8,"C",datetime.datetime(2024,11,10,12,30)),ezPackage(9,"D",datetime.datetime(2024,11,10,12,30)),ezPackage(10,"E",datetime.datetime(2024,11,10,12,30)),ezPackage(11,"A",datetime.datetime(2024,11,10,11,30),"note"),ezPackage(12,"B",datetime.datetime(2024,11,10,10,30),"note"),ezPackage(13,"A",datetime.datetime(2024,11,10,10,30)),ezPackage(14,"C",datetime.datetime(2024,11,10,11,30),"note"),ezPackage(15,"D",datetime.datetime(2024,11,10,11,30)),ezPackage(16,"E",datetime.datetime(2024,11,10,12,30)),ezPackage(17,"A",datetime.datetime(2024,11,10,10,30),"note"),ezPackage(18,"B",datetime.datetime(2024,11,10,11,30)),ezPackage(19,"C",datetime.datetime(2024,11,10,12,30)),ezPackage(20,"D",datetime.datetime(2024,11,10,12,30)),ezPackage(21,"E",datetime.datetime(2024,11,10,12,30)),ezPackage(22,"A",datetime.datetime(2024,11,10,11,30),"note")]

my_hash_table = HashTable(10)
for package in my_packages:
    my_hash_table.insertPackage(package)

truck1 = Truck(0,datetime.datetime(2024,11,10,9,30),my_destination_array,my_adjacency_matrix,my_hash_table)
truck2 = Truck(1,datetime.datetime(2024,11,10,8,30),my_destination_array,my_adjacency_matrix,my_hash_table)
truck3 = Truck(2,datetime.datetime(2024,11,10,8,30),my_destination_array,my_adjacency_matrix,my_hash_table)

Fleet = [truck1,truck2,truck3]

wrong_addresses = loadTrucks(Fleet,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22],my_hash_table)
for truck in Fleet:
    truck.sortPackages()

loadWrongAddressPackages(Fleet,wrong_addresses)

truck1.deliverPackages()
truck2.deliverPackages()
truck3.deliverPackages()

printAllTrucksStatus(Fleet,datetime.datetime(2024,11,10,11,44))
