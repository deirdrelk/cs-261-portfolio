# Name: Deirdre Lyons-Keefe
# OSU Email: lyonsked@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/11/22
# Description: Hash Map ADT using Open Addressing with quadratic probing.


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        This method receives no parameters. It clears the contents of the hash map, and doesn't change the underlying
        table capacity.
        """
        self.buckets = DynamicArray()
        for _ in range(self.capacity):
            self.buckets.append(None)
        self.size = 0

    def get(self, key: str) -> object:
        """
        This method receives a key, and traverses the hash map until the key is found. If found, the key's value
        is returned.
        """
        if self.size == 0:
            return
        bucket_index = self.hash_function(key) % self.capacity
        for j in range(self.capacity):
            next_bucket_index = (bucket_index + j * j) % self.capacity
            match = self.buckets[next_bucket_index]
            if match:
                if match.key == key and match.is_tombstone is False:
                    return match.value

    def put(self, key: str, value: object) -> None:
        """
        This method receives a key and value, and updates the key/value pair in the hash map.
        If the key already exists, the value is replaced.
        If the key doesn't already exist, check load factor. If >= 0.5, resize the table, then add the key/value pair.
        """
        # check for resize
        if self.table_load() >= 0.5:
            self.resize_table(self.capacity * 2)
        # then add the key/value pair
        new_entry = HashEntry(key, value)
        bucket_index = self.hash_function(key) % self.capacity
        for j in range(self.capacity):
            next_bucket_index = (bucket_index + j * j) % self.capacity
            if self.buckets[next_bucket_index] is None:
                self.buckets[next_bucket_index] = new_entry
                self.size += 1
                return
            else:
                match = self.buckets[next_bucket_index]
                if match.is_tombstone is True:
                    self.buckets[next_bucket_index] = new_entry
                    self.size += 1
                    return
                if match.key == key:
                    match.value = value
                    return

    def remove(self, key: str) -> None:
        """
        This method receives a key, and if found in the hash map, removes the key and value,
        and sets is_tombstone to True.
        """
        if self.contains_key(key) is False:
            return
        bucket_index = self.hash_function(key) % self.capacity
        for j in range(self.capacity):
            next_bucket_index = (bucket_index + j * j) % self.capacity
            match = self.buckets[next_bucket_index]
            if match is None:
                return
            if match.key == key and match.is_tombstone is False:
                match.is_tombstone = True
                self.size -= 1
                return

    def contains_key(self, key: str) -> bool:
        """
        This method receives a key, and returns True or False if the key is in the hash map.
        """
        # quadratic probing required
        if self.size == 0:
            return False
        bucket_index = self.hash_function(key) % self.capacity
        for j in range(self.capacity):
            next_bucket_index = (bucket_index + j * j) % self.capacity
            match = self.buckets[next_bucket_index]
            if match is None:
                return False
            if match.key == key and match.is_tombstone is False:
                return True

    def empty_buckets(self) -> int:
        """
        This method returns the number of buckets in the hash map where the value is None.
        """
        empty_bucket_count = 0
        for index in range(self.capacity):
            check_list = self.buckets[index]
            if check_list is None:
                empty_bucket_count += 1
        return empty_bucket_count

    def table_load(self) -> float:
        """
        Returns the load factor (size / number of buckets)
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Recompute the hash function for each element with the new capacity.
        All hash table links must be rehashed.
        If new capacity is less than 1 or less than the current size, just return.
        """
        if new_capacity < 1 or new_capacity < self.size:
            return
        length = self.capacity
        function = self.hash_function
        new_map = HashMap(new_capacity, function)
        self.capacity = new_map.buckets.length()
        # recompute the hash function for each element using the new capacity
        for bucket in range(length):
            check_entry = self.buckets[bucket]
            if check_entry is not None and check_entry.is_tombstone is False:
                new_map.put(check_entry.key, check_entry.value)
        self.buckets = new_map.buckets
        self.capacity = new_map.buckets.length()

    def get_keys(self) -> DynamicArray:
        """
        Returns all keys in the hashmap in an array.
        """
        keys_array = DynamicArray()
        for index in range(self.capacity):
            check_entry = self.buckets[index]
            if check_entry is not None and check_entry.is_tombstone is False:
                keys_array.append(check_entry.key)
        return keys_array


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
