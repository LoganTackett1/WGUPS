import csv
import datetime

class Package:
    def __init__(self,id,address,deadline,city,zip,weight,note,status="At Hub"):
        self.id = int(id)
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = int(zip)
        self.weight = float(weight)
        self.status = status
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
    def __init__(self):
        self.packages = []
        self.package_count = 0
        self.departure_time = None
        self.return_time = None
        self.miles = None

    #packages are stored by id, and their information will be pulled from the hash table
    def loadPackage(self,package):
        if package.id in self.packages:
            return False
        else:
            if self.package_count == 16:
                return False
            self.packages.append(package)
            self.package_count += 1
            return True

    def loadPackages(self,packages):
        for package in packages:
            self.loadPackage(package)

    #first sorts packages by deadline to ensure that packages with earlier deadlines get delivered first, O(nlogn).
    #then sorts each group of packages with the same deadline using nearest neighbor, 
    # such that the start of each group is the closest location to the end of the previous group.
    def sortPackages(self,hashTable,adjMatrix):
        return