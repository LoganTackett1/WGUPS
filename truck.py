from util import merge_sort, nearestNeighbor, twoDigit
from package import Package
import datetime
import math

class Truck:
    def __init__(self,id,departure_time,destination_array,adjacency_matrix,hashTable):
        self.id = id
        #packages to be delivered
        self.packages = []
        #packages with incorrect address note to be delivered when corrected
        self.packages_no_address = []
        #total count combines the two above
        self.package_count = 0
        #delivered packages
        self.delivered = []
        #addresses array, index of address in the array is the index of that address in the adjacency matrix
        self.destination_array = destination_array
        #all pairs shortest distance matrix
        self.adjacency_matrix = adjacency_matrix
        #hash table package info is stored in
        self.hashTable = hashTable
        #when the truck leaves the HUB
        self.departure_time = departure_time
        #time truck returns to HUB
        self.return_time = None
        self.miles = 0
        #time in which correct addresses are received
        self.address_update_time = datetime.datetime(2024,11,10,23,59)
        #in the event that all packages are delivered before correct addresses are received
        #the truck will take a break and wait for the new information.
        self.break_start = None


    #utility function
    def id_to_adj_label(self,id):
        package = self.hashTable.lookup(id)
        label = self.destination_array.index(package.address)
        return label
    

    #utility function
    def id_to_deadline(self,id):
        package = self.hashTable.lookup(id)
        return package.deadline
    

    #utility function
    def address_to_label(self,address):
        return self.destination_array.index(address)


    #packages are stored by id, and their information will be pulled from the hash table
    def loadPackage(self,package):
        if package.id in self.packages:
            return False
        else:
            if self.package_count == 16:
                return False
            #update the packages departure time to be the trucks departure time
            package.departure_time = self.departure_time
            #add package id to correct list
            if package.note == "Wrong Address Listed":
                self.packages_no_address.append(package.id)
            else:
                self.packages.append(package.id)
            self.package_count += 1
            return True
        

    def loadPackageById(self,id):
        if id in self.packages:
            return False
        else:
            if self.package_count == 16:
                return False
            package = self.hashTable.lookup(id)
            package.departure_time = self.departure_time
            if package.note == "Wrong Address Listed":
                self.packages_no_address.append(package.id)
            else:
                self.packages.append(package.id)
            self.package_count += 1
            return True


    def loadPackages(self,packages):
        for package in packages:
            self.loadPackage(package)

    
    def updateDeparture(self,time):
        self.departure_time = time
        for id in self.packages + self.packages_no_address:
            package = self.hashTable.lookup(id)
            package.departure_time = time


    #first sorts packages by deadline to ensure that packages with earlier deadlines get delivered first, O(nlogn).
    #then sorts each group of packages with the same deadline using nearest neighbor, worst case O(n^2), O(n) best case,
    # such that the start of each group is the closest location to the end of the previous group.
    #the destination array stores a list of all destinations such that the index of the destination is the vertex label 
    # in the adjacency matrix
    def sortPackages(self,initial=0):
        #sorts packages first by deadline, earlier to latest
        merge_sort(self.packages,0,len(self.packages)-1,self.id_to_deadline)

        l = 0
        r = 0
        
        start = initial
        while l < len(self.packages) - 1:
            #adjusting r pointer such that l and r pointer group items with same deadline
            if r < len(self.packages) and self.id_to_deadline(self.packages[l]) == self.id_to_deadline(self.packages[r]):
                r += 1
            else:
                #slice that portion of the packages array
                sliced = self.packages[l:r]
                #sort it by nearest neighbor
                optimal = nearestNeighbor(start,sliced,self.id_to_adj_label,self.adjacency_matrix)
                #copy the sorted items back into the original array
                for i in range(len(optimal)):
                    self.packages[l+i] = optimal[i]
                #adjust pointers
                l = r
                start = self.id_to_adj_label(self.packages[r-1])


    #defaults initial location and time to HUB and self.departure_time
    #O(n) best case O(n^2)
    def deliverPackages(self,init_location="HUB",init_time=None):
        #sort packages for optimal delivery order
        self.sortPackages(self.address_to_label(init_location))
        #preparing to deliver in order using array pop
        self.packages.reverse()

        #set current location to the hub
        curr_location = init_location
        #set curr time
        if init_time == None:
            curr_time = self.departure_time
        else:
            curr_time = init_time
        #boolean that tracks if we have received correct addresses for known problem packages
        correct_info_received = False
        #main loop
        while len(self.packages) > 0:
            #we have received the correct address information for packages that had wrong address
            if curr_time > self.address_update_time and correct_info_received == False:
                #add corrected packages to package array
                self.packages.extend(self.packages_no_address)
                self.packages_no_address.clear()
                #sort them to reoptimize delivery order with new information
                self.sortPackages(self.address_to_label(curr_location))
                #reverse as the sort undoes the correct ordering for array.pop() usage
                self.packages.reverse()
                #set correct_info_received to True so this optimization only happens once.
                correct_info_received = True

            #get package information
            delivering_id = self.packages.pop()
            delivering_package = self.hashTable.lookup(delivering_id)
            to_location = delivering_package.address

            #get address labels in adjacency matrix and get distance
            curr_location_label = self.address_to_label(curr_location)
            to_location_label = self.address_to_label(to_location)
            distance = self.adjacency_matrix[curr_location_label][to_location_label]

            #update truck milage
            self.miles += distance

            #18 mph average
            time_to = datetime.timedelta(hours=(distance/18))

            #calculate delivered time
            delivery_time = curr_time + time_to

            #update package information
            delivering_package.arrival_time = delivery_time

            #update curr pointers for next loop
            curr_time = delivery_time
            curr_location = to_location

            #all package delivery steps done for this package, decrement self.package_count
            #add package id to delivered
            self.package_count -= 1
            self.delivered.append(delivering_id)

        #while loop over, check to make sure there aren't any packages with late address corrections
        #if the below condition returns true, then we have delivered all packages except for those
        #with incorrect addresses, delivery truck will sit still until that time, and continue delivering
        if self.package_count != 0:
            self.packages.extend(self.packages_no_address)
            self.packages_no_address.clear()
            self.break_start = curr_time
            self.deliverPackages(curr_location,self.address_update_time)
        else:
            #all packages are delivered, time to return to HUB
            curr_location_label = self.address_to_label(curr_location)
            dist_to_hub = self.adjacency_matrix[0][curr_location_label]
            self.miles += dist_to_hub
            time_to_hub = datetime.timedelta(hours=(dist_to_hub/18))
            self.return_time = curr_time + time_to_hub

    
    #lots of casework here
    def calculateMilage(self,time):
        #time is after truck return
        if time >= self.return_time:
            miles = self.miles
        #time is before truck departure
        elif time <= self.departure_time:
            miles = 0
        else:
            #truck never took a break or time is before its break
            if self.break_start == None or time <= self.break_start:
                delta = time - self.departure_time
                miles = 18 * (delta / datetime.timedelta(hours=1))
            #truck took a break and time is in between break start and end
            elif time > self.break_start and time <= self.address_update_time:
                delta = self.break_start - self.departure_time
                miles = 18 * (delta / datetime.timedelta(hours=1))
            #truck took break and time is after break end
            else:
                delta1 = time - self.departure_time
                deltabreak = self.address_update_time - self.break_start
                miles = 18 * (delta1 / datetime.timedelta(hours=1) - deltabreak / datetime.timedelta(hours=1))
        return math.floor(100*miles) / 100

    
    def printDeliveryStatus(self,time):
        #print truck status
        if time < self.departure_time:
            status = "At HUB"
        elif time >= self.departure_time and time <= self.return_time:
            status = "Delivering"
        else:
            status = "At HUB"
        print("Truck " + str(int(self.id) + 1) + " status: " + status)

        #print truck milage
        print("   Current Milage: " + str(self.calculateMilage(time)))
        print()
        
        #print package information
        print("   Truck " + str(int(self.id) + 1) +  " Packages:")
        all_packages = self.packages + self.packages_no_address + self.delivered
        for id in all_packages:
            package = self.hashTable.lookup(id)
            print("   ",end="")
            package.printStatus(time)
            #calculate status
            """
            if time < package.departure_time:
                status = "HUB"
            elif time >= package.departure_time and time < package.arrival_time:
                if time > package.deadline:
                    status = "En Route (Late)"
                else:
                    status = "En Route"
            else:
                if package.arrival_time > package.deadline:
                    status = "Delivered at time: " + str(package.arrival_time.hour) + ":" + twoDigit(package.arrival_time.minute) + " (Late)"
                else:
                    status = "Delivered at time: " + str(package.arrival_time.hour) + ":" + twoDigit(package.arrival_time.minute) + " (On Time)"
            print("   ID: " + str(package.id) + "  Status: " + status)
            """