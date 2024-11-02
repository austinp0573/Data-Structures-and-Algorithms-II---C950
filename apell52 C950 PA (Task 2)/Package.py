from datetime import timedelta

# Create Package class
class Package:
    def __init__(self, id, address, city, state, zipcode, deadline, weight, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departureTime = None
        self.deliveryTime = None
        self.truckNumber = None

    def __str__(self):
        status_str = self.status
        if self.status == "Delivered":
            status_str = f"Delivered at {self.deliveryTime}"
        elif self.status == "En route":
            status_str = f"En route - Truck {self.truckNumber}"
        elif self.status == "IN HUB":
            status_str = "IN HUB"

        return ("%s | %s | %s | %s | %s | %s | %s kg | %s" %
                (self.id, self.address, self.city, self.state, self.zipcode, self.deadline, self.weight, status_str))
    # Provide appropriate status in program output
    def updateStatus(self, input_time):
        if self.departureTime is None:
            self.status = "IN HUB"
        elif input_time < self.departureTime:
            self.status = "IN HUB"
        elif input_time < self.deliveryTime:
            self.status = "En route"
        else:
            self.status = "Delivered"

        # Ensure that special package, ID 9, is set properly at 10:20
        if self.id == 9:
            if input_time >= timedelta(hours=10, minutes=20):
                self.address = "410 S State St"
                self.zipcode = "84111"
            else:
                self.address = "300 State St"
                self.zipcode = "84103"