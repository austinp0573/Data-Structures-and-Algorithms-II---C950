#C950 Performance Assessment
#Name: Austin Pelley
#Student ID: 011191773

import csv
from datetime import timedelta
from HashTable import HashTable
from Package import Package
from Truck import Truck
from builtins import ValueError

# Load and read the csv files
with open("CSV_files/WGUPS Package File.csv") as CSV_Packages:
    PackageCSV = csv.reader(CSV_Packages)
    PackageCSV = list(PackageCSV)
with open("CSV_files/Separated Distances.csv") as CSV_Distances:
    DistanceCSV = csv.reader(CSV_Distances)
    DistanceCSV = list(DistanceCSV)
with open("CSV_files/Separated Addresses.csv") as CSV_Addresses:
    AddressCSV = csv.reader(CSV_Addresses)
    AddressCSV = list(AddressCSV)


# Function to load packages from package csv file into the hash table
def inputData(filename):
    with open(filename, encoding='utf-8-sig') as packages:  # Use utf-8-sig to handle BOM
        package_data = csv.reader(packages, delimiter=',')
        for package in package_data:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pStatus = "IN HUB"
            # Create package object
            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline, pWeight, pStatus)
            # Insert package object into the hash table
            packageHashTable.insertion(pID, p)


# Create a hash table for packages
packageHashTable = HashTable()

# Load packages from package csv file into the hash table
inputData('CSV_files/WGUPS Package File.csv')


# Function to find distance between two addresses
def spaceApart(address1, address2):
    distance = DistanceCSV[address1][address2]
    if distance == '':
        distance = DistanceCSV[address2][address1]
    return float(distance)


# Function to find index of address from address csv file
def address(a):
    for row in AddressCSV:
        if a in row[2]:
            return int(row[0])


truck1 = Truck(1, 18, [1, 4, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
               timedelta(hours=8))
truck2 = Truck(2, 18, [3, 5, 6, 18, 25, 27, 33, 35, 36, 38], 0.0, "4001 South 700 East",
               timedelta(hours=9, minutes=5))
truck3 = Truck(3, 18, [2, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 26, 28, 32, 39], 0.0, "4001 South 700 East",
               timedelta(hours=11))



# Function to deliver packages on a given truck using nearest neighbor algorithm
def packageDelivery(truck):
    # Create a list for all packages that are not delivered yet
    notDelivered = []

    # Append the list with packages from the hash table and set initial properties
    for packageID in truck.packages:
        package = packageHashTable.lookUP(packageID)
        package.truckNumber = truck.truckNumber  # Set the truck number
        package.departureTime = truck.departureTime  # Set the departure time
        package.status = "En route"  # Update status when loaded
        notDelivered.append(package)
        # Update the package in the hash table
        packageHashTable.insertion(packageID, package)

    # Create a new list for packages to be delivered
    delivery_list = truck.packages.copy()
    truck.packages.clear()

    # Loop through the list until no package left
    while delivery_list:
        nextAddress = float('inf')  # Use infinity as initial distance
        nextPackage = None
        nextPackageID = None

        # Find the next nearest package
        for packageID in delivery_list:
            package = packageHashTable.lookUP(packageID)

            # Ensure packages that must be delivered by 10:30 are properly prioritized
            if package.id in [6, 25]:
                currentDistance = spaceApart(address(truck.address), address(package.address))
                nextAddress = currentDistance
                nextPackage = package
                nextPackageID = packageID
                break

            # Find the nearest package
            currentDistance = spaceApart(address(truck.address), address(package.address))
            if currentDistance < nextAddress:
                nextAddress = currentDistance
                nextPackage = package
                nextPackageID = packageID

        # Update truck's properties
        truck.packages.append(nextPackageID)
        truck.mileage += nextAddress
        truck.address = nextPackage.address
        truck.time += timedelta(hours=nextAddress / 18.0)

        # Update package's properties
        nextPackage.status = "Delivered"
        nextPackage.deliveryTime = truck.time

        # Update the package in the hash table
        packageHashTable.insertion(nextPackage.id, nextPackage)

        # Remove the delivered package from the delivery list
        delivery_list.remove(nextPackageID)


# Call packageDelivery() method, which uses Nearest Neighbor, on each truck
packageDelivery(truck1)
packageDelivery(truck2)
# Ensure truck 3 leaves at an appropriate time
firstTruckBack = min(truck1.time, truck2.time)
truck3.departureTime = max(firstTruckBack, truck3.departureTime)
packageDelivery(truck3)

while True:
    # Provide user interface
    print("\nWestern Governors University Parcel Service (WGUPS)")
    print("<=================================================>")
    # Output the sum mileage of all the trucks
    print("Total mileage traveled by all delivery vehicles:", (truck1.mileage + truck2.mileage + truck3.mileage), "miles")

    try:
        # Prompt for user to input a number to engage with the interface
        userInput = int(input("""\nPlease select a menu option from those provided below:
1) View a summary of all package deliveries for the day:
2) View a summary of package(s) at a user specified time:
3) Exit the program\n"""))

        # Provide menu functionality
        if userInput == 1:
            # Output summary of the day's deliveries
            print("Packages delivered:")
            for pID in range(1, 41):
                package = packageHashTable.lookUP(pID)
                package.updateStatus(truck3.time)
                print(str(package) + " by Truck " + str(package.truckNumber))

        elif userInput == 2:
            # Prompt for user specified time
            timeInput = input("Please enter a time to check the status of package(s), using format (HH:MM):\n")
            (h, m) = timeInput.split(':')
            userTime = timedelta(hours=int(h), minutes=int(m))
            try:
                viewInput = int(input("""Please select an option to view a summary of package(s):
1. View an individual package by package ID:
2. View all packages:\n"""))
                if viewInput == 1:
                    idInput = [int(input("Please enter a package ID:\n"))]
                    print("Summary of package as of " + str(userTime) + ":")
                    for pID in idInput:
                        package = packageHashTable.lookUP(pID)
                        package.updateStatus(userTime)
                        print(str(package))
                elif viewInput == 2:
                    idInput = range(1, 41)
                    print("Summary of packages as of " + str(userTime) + ":")
                    for pID in idInput:
                        package = packageHashTable.lookUP(pID)
                        package.updateStatus(userTime)
                        print(str(package))

                    # Calculate total mileage up to the user-specified time
                    total_mileage = 0
                    for truck in [truck1, truck2, truck3]:
                        if truck.departureTime <= userTime:
                            # If the truck has completed its route by userTime
                            if truck.time <= userTime:
                                total_mileage += truck.mileage
                            # If the truck is still en route
                            else:
                                # Calculate mileage based on time elapsed
                                time_ratio = (userTime - truck.departureTime) / (truck.time - truck.departureTime)
                                total_mileage += truck.mileage * time_ratio

                    print(f"\nTotal mileage traveled by all trucks as of {userTime}: {total_mileage:.1f} miles")

            except ValueError:
                print("Input not recognized, please try again.")

        elif userInput == 3:
            # Exit the program
            break

        else:
            print("That input wasn't one the the provided options, please select again.")

    except ValueError:
        print("Input not recognized, please try again.")