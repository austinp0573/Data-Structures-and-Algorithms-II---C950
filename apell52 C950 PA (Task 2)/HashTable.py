# HashTable class using chaining
class HashTable:
    def __init__(self, initial_capacity=40):
        # Initialize hash table with empty lists
        self.table = [[] for _ in range(initial_capacity)]

    # Insert a Package object into the hash table using the package ID as the key
    def insertion(self, key, package):
        # Hash function to find bucket index
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Update the entry if it already exists in the bucket
        for entry in bucket_list:
            if entry[0] == key:  # key is the package ID
                entry[1] = package  # Update the package object
                return True

        # If not found, add a new entry to the bucket
        entry = [key, package]  # Add the key and package object
        bucket_list.append(entry)
        return True

    # Look-up a package in hash table by package ID
    def lookUP(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for entry in bucket_list:
            if entry[0] == key:
                return entry[1]  # Return the package object
        return None

    # Remove a package from hash table by package ID
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for entry in bucket_list:
            if entry[0] == key:
                bucket_list.remove(entry)
                return True
        return False