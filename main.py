# Student ID #012308366
# Logan Tackett

from util import populateUpperTriange, FloydWarshallAllPairsShortestPath, merge_sort, floatify
from hashTable import HashTable
from postal import loadTrucks, printAllTrucksStatus, loadWrongAddressPackages, loadPackageData, loadDistanceData
from package import Package
from truck import Truck
import datetime
import os

#import csv data
csv_packages = loadPackageData('WGUPS Package File - Sheet1.csv')
csv_packages_ids = []
for package in csv_packages:
    csv_packages_ids.append(package.id)

#import distance table
destination_array, matrix = loadDistanceData('WGUPS Distance Table - Sheet1.csv')
#populate empty cells of distance table to make it symmetric
populateUpperTriange(matrix)
#convert all entries of distance table to float values
floatify(matrix)
#convert distance table to all-paths shortest distance table
FloydWarshallAllPairsShortestPath(matrix)

#create package hash table
hash_table = HashTable(10)
#insert all packages into hash table
for package in csv_packages:
    hash_table.insertPackage(package)

#mark package 9's address as incorrectly listed by assigning correction time:
package_9 = hash_table.lookup(9)
package_9.setAddressCorrectionTime(datetime.datetime(2024,11,10,10,20))

#create trucks 1, 2, and 3. Truck 1 leaves at 8:00, Truck 2 leaves at 9:05, and truck 3 leaves when one of the two trucks returns. 
truck1 = Truck(0,datetime.datetime(2024,11,10,8,0),destination_array,matrix,hash_table)
truck2 = Truck(1,datetime.datetime(2024,11,10,9,5),destination_array,matrix,hash_table)
truck3 = Truck(2,datetime.datetime(2024,11,10,23,59),destination_array,matrix,hash_table)

Fleet = [truck1,truck2,truck3]

#load packages onto trucks, returns list of packages with incorrect addresses
wrong_addresses = loadTrucks(Fleet,csv_packages_ids,hash_table)

#loads packages with wrong addresses onto trucks
loadWrongAddressPackages(Fleet,wrong_addresses)

#delivers packages for trucks 1 and 2 (delivering packages is done by first sorting into optimal delivery order and then delivering in sequence)
truck1.deliverPackages()
truck2.deliverPackages()
#truck three starts delivery when one of the two trucks returns
if truck1.return_time < truck2.return_time:
    truck3.updateDeparture(truck1.return_time)
else:
    truck3.updateDeparture(truck2.return_time)
truck3.deliverPackages()

def interface(error = ""):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("*** WGUPS Parcel System ***")
    print(error)
    print("   Type '1' and hit enter for status of specific package   ")
    print("   Type '2' and hit enter for status of all trucks and their packages   ")
    action = input()
    if action != '1' and action != '2':
        interface("!!! Wrong Input, Make sure you typed '1' or '2' !!!")
    elif action == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Type the id of the package and press enter:")
        package_id = input()
        package = hash_table.lookup(package_id)
        if package == False:
            interface("!!! Package ID not found in system !!!")
        else:
            print("Type out a time in the following format: '09:50' or '17:02':")
            time_inp = input()
            time_arr = time_inp.split(":")
            time = datetime.datetime(2024,11,10,int(time_arr[0]),int(time_arr[1]))
            os.system('cls' if os.name == 'nt' else 'clear')
            package.printStatus(time)
            print("Hit ENTER to return to home screen.")
            dummy = input()
            interface()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Type out a time in the following format: '09:50' or '17:02':")
        time_inp = input()
        time_arr = time_inp.split(":")
        time = datetime.datetime(2024,11,10,int(time_arr[0]),int(time_arr[1]))
        os.system('cls' if os.name == 'nt' else 'clear')
        printAllTrucksStatus(Fleet,time)
        print("Hit ENTER to return to home screen.")
        dummy = input()
        interface()

interface()