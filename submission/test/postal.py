from util import merge_sort, nearestNeighbor, twoDigit
from package import Package
from truck import Truck
import datetime
import csv
import math


#functions taking packages as input are assumed to be package id's requiring lookup.
#mostly manual loading as packages 13,14,15,16,19,20 must go together in earliest leaving truck.
#O(nlogn) because of merge sorts
def loadTrucks(trucks,packages,hashtable):
    #key_f function to be used
    def id_to_deadline(id):
            package = hashtable.lookup(id)
            return package.deadline
    
    #addressing packages that must be delivered together
    packages_grouped = [13,14,15,16,19,20]
    for id in packages_grouped:
        packages.remove(id)

    #group package ids by whether they have notes or not
    packages_no_notes = []
    packages_notes = []
    for id in packages:
        package = hashtable.lookup(id)
        if package.note == None:
            packages_no_notes.append(id)
        else:
            packages_notes.append(id)

    #sort them by time that way packages with earlier deadlines are loaded first
    merge_sort(packages_no_notes,0,len(packages_no_notes)-1,id_to_deadline)
    merge_sort(packages_notes,0,len(packages_notes)-1,id_to_deadline)
    #to prepare them to load by array.pop()
    packages_no_notes.reverse()
    packages_notes.reverse()
    #to store packages that have a note of wrong address
    packages_wrong_address = []

    #truck 1 will first get grouped packages
    truck1 = trucks[0]
    while truck1.package_count < 16 and len(packages_grouped) > 0:
        id = packages_grouped.pop()
        truck1.loadPackageById(id)

    #truck 1 will then get all packages with no notes up to 16 packages
    while truck1.package_count < 16 and len(packages_no_notes) > 0:
        id = packages_no_notes.pop()
        truck1.loadPackageById(id)

    #truck 2 will have all packages with notes and more up to 16
    #truck 2 will be waiting for late arrivals to arrive before leaving.
    truck2 = trucks[1]
    while truck2.package_count < 16 and len(packages_notes) > 0:
        id = packages_notes.pop()
        package = hashtable.lookup(id)
        if package.note == "Wrong Address Listed":
            packages_wrong_address.append(id)
        else:
            truck2.loadPackageById(id)

    #load any remaining packages onto the trucks now
    truck3 = trucks[2]
    while truck1.package_count < 16 and len(packages_no_notes) > 0:
        id = packages_no_notes.pop()
        truck1.loadPackageById(id)
    while truck1.package_count < 16 and len(packages_notes) > 0:
        id = packages_notes.pop()
        truck1.loadPackageById(id)
    while truck2.package_count < 16 and len(packages_no_notes) > 0:
        id = packages_no_notes.pop()
        truck2.loadPackageById(id)
    while truck2.package_count < 16 and len(packages_notes) > 0:
        id = packages_notes.pop()
        truck2.loadPackageById(id)
    while truck3.package_count < 16 and len(packages_no_notes) > 0:
        id = packages_no_notes.pop()
        truck3.loadPackageById(id)
    while truck3.package_count < 16 and len(packages_notes) > 0:
        id = packages_notes.pop()
        truck3.loadPackageById(id)
    
    #we will return these to be loaded onto a truck after sorting, that way it is at the end of the
    #list of packages (to be delivered last). They will be resorted once the new address information
    #is gotten
    return packages_wrong_address


#used to load packages who's addresses need correction to the packages_no_address list
def loadWrongAddressPackages(trucks,extras):
    truck1 = trucks[0]
    truck2 = trucks[1]
    truck3 = trucks[2]
    #try truck 1 first
    while truck1.package_count < 16 and len(extras) > 0:
        id = extras.pop()
        truck1.loadPackageById(id)
        #truck stores when it will be receiving the address for use in delivery function
        truck1.address_update_time = datetime.datetime(2024,11,10,10,20)
    while truck2.package_count < 16 and len(extras) > 0:
        id = extras.pop()
        truck2.loadPackageById(id)
        truck2.address_update_time = datetime.datetime(2024,11,10,10,20)
    while truck3.package_count < 16 and len(extras) > 0:
        id = extras.pop()
        truck3.loadPackageById(id)
        truck3.address_update_time = datetime.datetime(2024,11,10,10,20)


def printAllTrucksStatus(trucks,time):
    print("*** Delivery Status At Time: " + str(time.hour) + ":" + twoDigit(time.minute) + " ***")
    print()
    total_milage = 0
    for truck in trucks:
        total_milage += truck.calculateMilage(time)
    print("All Trucks Current Milage: " + str(math.floor(total_milage*100)/100))
    print()
    for truck in trucks:
        truck.printDeliveryStatus(time)
        print()


#converts time from csv to datetime
def csvToDateTime(time):
    if time == "EOD":
        return datetime.datetime(2024,11,10,23,59)
    else:
        time_arr = time[:-3].split(":")
        return datetime.datetime(2024,11,10,int(time_arr[0]),int(time_arr[1]))


#reads package csv
def loadPackageData(csv_path):
    packages = []
    with open(csv_path,mode='r') as file:
        csvFile = csv.reader(file)
        line_arr = []
        for line in csvFile:
            line_arr.append(line)
        for i in range(1,len(line_arr)):
            line = line_arr[i]
            if line[7] == "":
                note = None
            else:
                note = line[7]
            package = Package(line[0],line[1],csvToDateTime(line[5]),line[2],line[4],line[6],note)
            packages.append(package)
    return packages

    
#reads distance_table csv
def loadDistanceData(csv_path):
    with open(csv_path,mode='r') as file:
        csvFile = csv.reader(file)
        line_arr = []
        for line in csvFile:
            line_arr.append(line)
        destination_array = line_arr[0][1:]
        matrix = []
        for i in range(1,len(line_arr)):
            line = line_arr[i]
            matrix.append(line[1:])
        return (destination_array,matrix)