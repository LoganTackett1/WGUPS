from util import merge_sort, nearestNeighbor
import csv
import datetime


class Package:
    def __init__(self,id,address,deadline,city,zip,weight,note=None):
        self.id = int(id)
        self.address = address
        self.deadline = deadline
        self.arrival_time = None
        self.departure_time = None
        self.city = city
        self.zip = int(zip)
        self.weight = float(weight)
        self.note = note


def packageFromCsv(id,csv):
    with open(csv,newline='') as csvfile:
        package_table = csv.reader(csvfile)
        for row in package_table:
            arr = row.split(",")
            if arr[0] == str(id):
                timearr = arr[2].split(':')
                return Package(arr[0],arr[1],datetime.time(timearr[0],timearr[1]),arr[3],arr[4],arr[5],arr[6])
        return False
    

class Truck:
    def __init__(self,id,departure_time,destination_array,adjacency_matrix,hashTable):
        self.id = id
        self.packages = []
        self.packages_no_address = []
        self.delivered = []
        self.destination_array = destination_array
        self.adjacency_matrix = adjacency_matrix
        self.hashTable = hashTable
        self.package_count = 0
        self.departure_time = departure_time
        self.current_time = departure_time
        self.return_time = None
        self.miles = 0
        self.address_update_time = datetime.datetime(2024,11,10,23,59)


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
            self.packages.append(id)
            self.package_count += 1
            return True


    def loadPackages(self,packages):
        for package in packages:
            self.loadPackage(package)


    #first sorts packages by deadline to ensure that packages with earlier deadlines get delivered first, O(nlogn).
    #then sorts each group of packages with the same deadline using nearest neighbor, 
    # such that the start of each group is the closest location to the end of the previous group.
    #the destination array stores a list of all destinations such that the index of the destination is the vertex label 
    # in the adjacency matrix
    def sortPackages(self):
        #key_f function
        def id_to_deadline(id):
            package = self.hashTable.lookup(id)
            return package.deadline
        
        #key_f function
        def id_to_adj_label(id):
            package = self.hashTable.lookup(id)
            label = self.destination_array.index(package.address)
            return label
        
        #sorts packages first by deadline, earlier to latest
        merge_sort(self.packages,0,self.package_count-1,id_to_deadline)

        l = 0
        r = 0
        #will always be the hub.
        start = 0
        while l < self.package_count - 1:
            #adjusting r pointer such that l and r pointer group items with same deadline
            if r < self.package_count and id_to_deadline(self.packages[l]) == id_to_deadline(self.packages[r]):
                r += 1
            else:
                #slice that portion of the packages array
                sliced = self.packages[l:r]
                #sort it by nearest neighbor
                optimal = nearestNeighbor(start,sliced,id_to_adj_label,self.adjacency_matrix)
                #copy the sorted items back into the original array
                for i in range(len(optimal)):
                    self.packages[l+i] = optimal[i]
                #adjust pointers
                l = r
                start = id_to_adj_label(self.packages[r-1])


    def deliverPackages(self):
        #preparing to deliver in order using array pop
        self.packages.reverse()

        curr_location = "A"
        curr_time = self.departure_time
        correct_info_received = False
        while self.package_count > 0:
            #we have received the correct address information for packages that were loaded last
            if curr_time > self.address_update_time and correct_info_received == False:
                #sort them to reoptimize delivery order with new information
                self.sortPackages(self.hashTable,self.adjacency_matrix,self.destination_array)
                #reverse as the sort undoes the correct ordering for array.pop() usage
                self.packages.reverse()
                #set correct_info_received to True so this optimization only happens once.
                correct_info_received = True

            #get package information
            delivering_id = self.packages.pop()
            delivering_package = self.hashTable.lookup(delivering_id)
            to_location = delivering_package.address

            #get address labels in adjacency matrix and get distance
            curr_location_label = self.destination_array.index(curr_location)
            to_location_label = self.destination_array.index(to_location)
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

        #while loop over means that all packages are delivered, time to return to HUB
        curr_location_label = self.destination_array.index(curr_location)
        dist_to_hub = self.adjacency_matrix[0][curr_location_label]
        self.miles += dist_to_hub
        time_to_hub = datetime.timedelta(hours=(dist_to_hub/18))
        self.return_time = curr_time + time_to_hub

    
    def calculateMilage(self,time):
        if time >= self.return_time:
            miles = self.miles
        else:
            delta = time - self.departure_time
            miles = 18 * (delta / datetime.timedelta(hours=1))
        return miles

    
    def printDeliveryStatus(self,time):
        #print truck status
        if time < self.departure_time:
            status = "At HUB"
        elif time >= self.departure_time and time <= self.return_time:
            status = "Delivering"
        else:
            status = "At HUB"
        print("Truck " + str(self.id) + " status: " + status)

        #print truck milage
        print("   Current Milage: " + str(self.calculateMilage(time)))
        print()
        
        #print package information
        print("   Truck " + str(self.id) +  " Packages:")
        all_packages = self.packages + self.packages_no_address + self.delivered
        for id in all_packages:
            package = self.hashTable.lookup(id)
            #calculate status
            if time < package.departure_time:
                status = "HUB"
            elif time >= package.departure_time and time < package.arrival_time:
                if time > package.deadline:
                    status = "En Route (Late)"
                else:
                    status = "En Route"
            else:
                if package.arrival_time > package.deadline:
                    status = "Delivered at time: " + str(package.arrival_time.hour) + ":" + str(package.arrival_time.minute) + "(Late)"
                else:
                    status = "Delivered at time: " + str(package.arrival_time.hour) + ":" + str(package.arrival_time.minute) + "(On Time)"
            print("   ID: " + str(package.id) + "  Status: " + status)

        
            

#functions taking packages as input are assumed to be package id's requiring lookup.
def loadTrucks(trucks,packages,hashtable):
    #key_f function to be used
    def id_to_deadline(id):
            package = hashtable.lookup(id)
            return package.deadline
    
    packages_no_notes = []
    packages_notes = []
    #group package ids by whether they have notes or not
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

    #truck 1 will have all packages with no notes up to 16 packages
    truck1 = trucks[0]
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

#used to load packages who's addresses need correction to the back of the list.
def loadWrongAddressPackages(trucks,extras):
    truck1 = trucks[0]
    truck2 = trucks[1]
    truck3 = trucks[2]
    while truck1.package_count < 16 and len(extras) > 0:
        id = extras.pop()
        truck1.loadPackageById(id)
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
    print("*** All Deliveries Status ***")
    print()
    total_milage = 0
    for truck in trucks:
        total_milage += truck.calculateMilage(time)
    print("All Trucks Current Milage: " + str(total_milage))
    print()
    for truck in trucks:
        truck.printDeliveryStatus(time)
        print()
    