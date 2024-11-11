from util import populateUpperTriange, FloydWarshallAllPairsShortestPath, merge_sort, floatify
from hashTable import HashTable
from postal import Package, Truck, loadTrucks, printAllTrucksStatus, loadWrongAddressPackages, loadPackageData, loadDistanceData
import datetime

csv_packages = loadPackageData('WGUPS Package File - Sheet1.csv')
csv_packages_ids = []
for package in csv_packages:
    csv_packages_ids.append(package.id)

destination_array, matrix = loadDistanceData('WGUPS Distance Table - Sheet1.csv')
populateUpperTriange(matrix)
floatify(matrix)
FloydWarshallAllPairsShortestPath(matrix)

hash_table = HashTable(10)
for package in csv_packages:
    hash_table.insertPackage(package)

truck1 = Truck(0,datetime.datetime(2024,11,10,8,0),destination_array,matrix,hash_table)
truck2 = Truck(1,datetime.datetime(2024,11,10,9,5),destination_array,matrix,hash_table)
truck3 = Truck(2,datetime.datetime(2024,11,10,8,30),destination_array,matrix,hash_table)

Fleet = [truck1,truck2,truck3]

wrong_addresses = loadTrucks(Fleet,csv_packages_ids,hash_table)

loadWrongAddressPackages(Fleet,wrong_addresses)

truck1.deliverPackages()
truck2.deliverPackages()
if truck1.return_time < truck2.return_time:
    truck3.departure_time = truck1.return_time
else:
    truck3.departure_time = truck2.return_time
truck3.deliverPackages()

printAllTrucksStatus(Fleet,datetime.datetime(2024,11,10,11,44))
