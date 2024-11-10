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
        self.departure_time = None
        self.return_time = None
        self.miles = None

    def loadPackage(self,package):
        if package.id in self.packages:
            return False
        else:
            self.packages.append(package)

    def loadPackages(self,packages):
        for package in packages:
            self.loadPackage(package)