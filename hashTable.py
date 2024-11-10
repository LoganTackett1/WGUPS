from package import Package
from package import packageFromCsv

class HashTable:
    def __init__(self,initial_size):
        self.table = [None] * initial_size
        self.size = initial_size
        self.count = 0
    
    def hashkey(self,id):
        return int(id) - 1


    def resize(self):
        extension = [None] * self.size
        self.table.extend(extension)
        self.size *= 2


    #assumes status to be default at hub
    def insertPackage(self,package):
        key = self.hashkey(package.id)

        #If key outside range of table
        if key > self.size - 1:
            self.resize()
            return self.insertPackage(package)
    
        #If key already in table, dont increment count and update info
        #If key not in table, increment count
        if self.table[key] == None:
            self.count += 1
        self.table[key] = package

        return True


    #Inserts package from csv file using only id for lookup
    def insertPackageCsv(self,id,csv):
        package = packageFromCsv(id,csv)
        if package != False:
            return self.insertPackage(package)
        else:
            return False     
        
    #Lookup function
    def lookup(self,id):
        key = self.hashkey(id)
        if key < 0 or key > self.size - 1:
            return False
        else:
            return self.table[key]
