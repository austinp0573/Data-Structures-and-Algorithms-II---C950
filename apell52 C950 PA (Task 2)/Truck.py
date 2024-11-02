# Create Truck class
class Truck:
    def __init__(self, truckNumber, speed, packages, mileage, address, departureTime):
        self.truckNumber = truckNumber
        self.speed = speed
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.departureTime = departureTime
        self.time = departureTime

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (self.truckNumber, self.speed, self.packages, self.mileage, self.address, self.departureTime)