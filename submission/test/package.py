from util import twoDigit

class Package:
    def __init__(self,id,address,deadline,city,zip,weight,note=None):
        #standard package props from table
        self.id = int(id)
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = int(zip)
        self.weight = float(weight)
        self.note = note

        #extra package props
        self.arrival_time = None
        self.departure_time = None

    def printStatus(self,time):
        #calculate status
            if time < self.departure_time:
                status = "HUB"
            elif time >= self.departure_time and time < self.arrival_time:
                if time > self.deadline:
                    status = "En Route (Late)"
                else:
                    status = "En Route"
            else:
                if self.arrival_time > self.deadline:
                    status = "Delivered at time: " + str(self.arrival_time.hour) + ":" + twoDigit(self.arrival_time.minute) + " (Late)"
                else:
                    status = "Delivered at time: " + str(self.arrival_time.hour) + ":" + twoDigit(self.arrival_time.minute) + " (On Time)"
            print("ID: " + str(self.id) + "  Status: " + status)
