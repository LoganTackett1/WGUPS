from hashTable import HashTable
from package import Package
import datetime

myTable = HashTable(10)
myPackage = Package(1,"111 Goose St",datetime.time(10,30),"Las Vegas",89031,31,"Late Arrival")
myTable.insertPackage(myPackage)