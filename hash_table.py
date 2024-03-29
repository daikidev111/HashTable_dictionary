""" Hash Table ADT

Defines a Hash Table using Linear Probing for conflict resolution.
It currently rehashes the primary cluster to handle deletion.
"""
__author__ = 'Daiki Kubo'

from referential_array import ArrayR
from typing import TypeVar, Generic, Tuple
import unittest

T = TypeVar('T')


class LinearProbeHashTable(Generic[T]):
    """
    Linear Probe Hash Table

    constants:
        MIN_CAPACITY: smallest valid table size
        DEFAULT_TABLE_SIZE: default table size used in the __init__
        DEFAULT_HASH_TABLE: default hash base used for the hash function
        PRIMES: list of prime numbers to use for resizing

    attributes:
        count: number of elements in the hash table
        table: used to represent our internal array
        hash_base: base prime used in hash function
        table_size: current size of the hash table
        next_prime: next prime number to use when resizing
    """
    MIN_CAPACITY = 1

    DEFAULT_TABLE_SIZE = 17
    DEFAULT_HASH_BASE = 31
    PRIMES = [3, 7, 11, 17, 23, 29, 37, 47, 59, 71, 89, 107, 131, 163, 197, 239, 293, 353, 431, 521, 631, 761, 919,
              1103, 1327, 1597, 1931, 2333, 2801, 3371, 4049, 4861, 5839, 7013, 8419, 10103, 12143, 14591, 17519, 21023,
              25229, 30313, 36353, 43627, 52361, 62851, 75521, 90523, 108631, 130363, 156437, 187751, 225307, 270371,
              324449, 389357, 467237, 560689, 672827, 807403, 968897, 1162687, 1395263, 1674319, 2009191, 2411033,
              2893249, 3471899, 4166287, 4999559, 5999471, 7199369]

    def __init__(self, hash_base: int = DEFAULT_HASH_BASE, table_size: int = DEFAULT_TABLE_SIZE) -> None:
        """
        :complexity: O(N) where N is the table_size
        """
        self.count = 0
        self.table = ArrayR(max(self.MIN_CAPACITY, table_size))
        self.hash_base = hash_base
        self.table_size = table_size
        self.next_prime = 0
        self.collision_counter = 0
        self.rehash_counter = 0
        self.probe_chain_counter = 0
        self.probe_max_counter = 0
        self.probe_max = []

        while LinearProbeHashTable.PRIMES[self.next_prime] <= table_size:
            self.next_prime += 1

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        :complexity: O(1)
        """
        return self.count

    def __delitem__(self, key: str) -> None:
        """
        Deletes an item from our hash table by rehashing the
        remaining items in the current primary cluster
        :raises KeyError: when the key doesn't exist
        :complexity best: O(K) finds the position straight away and doesn't have to rehash
                          where K is the size of the key
        :complexity worst: O(K + N) when it has to rehash all items in the hash table
                          where N is the table size
        """
        position = self.__linear_probe(key, False)
        self.table[position] = None
        self.count -= 1

        position = (position + 1) % len(self.table)
        while self.table[position] is not None:
            item = self.table[position]
            self.table[position] = None
            self.count -= 1
            self[str(item[0])] = item[1]
            position = (position + 1) % len(self.table)

    def __rehash(self) -> None:
        """
        Need to resize table and reinsert all values
        :complexity:
        """
        self.rehashCounterIncrement()
        new_hash = LinearProbeHashTable(self.hash_base, LinearProbeHashTable.PRIMES[self.next_prime])
        self.next_prime += 1

        for i in range(len(self.table)):
            if self.table[i] is not None:
                new_hash[str(self.table[i][0])] = self.table[i][1]

        self.count = new_hash.count
        self.table = new_hash.table

    def __linear_probe(self, key: str, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using linear probing
        If there is something but not the key, we increment probeChain and probeMaxChain counters. Once, it
        successfully, inserts in an empty position, a probeMaxCounter getter that has a length of probe chain per key,
        will be appended inside the array probe_max. Then, we check if the probe_max_counter is more than 0, and if it
        is we increment the collision counter by one. Afterwards, we initialize the probe_max_counter to zero and
        start again.

        :complexity best: O(K) first position is empty
                          where K is the size of the key
        :complexity worst: O(K + N) when we've searched the entire table
                           where N is the table_size
        :raises KeyError: When a position can't be found
        """
        position = self.hash(key)  # get the position using hash

        if is_insert and self.is_full():
            raise KeyError(key)

        for _ in range(len(self.table)):  # start traversing
            if self.table[position] is None:  # found empty slot

                if is_insert:
                    # append all the keys probe length inside the tuple. To find the max number of probe chain
                    self.probe_max.append(self.getProbeMaxCounter())

                    # if a key has more than one probe chain then it means a collision must be incremented by one
                    if self.probe_max_counter > 0:
                        self.collisionCounterIncrement()

                    # This is the probe chain counter for each word used to store inside the tuple. Hence,
                    # it must be initialized back to 0.
                    self.probe_max_counter = 0

                    return position

                else:
                    raise KeyError(key)  # so the key is not in
            elif self.table[position][0] == key:  # found key
                return position

            else:  # there is something but not the key, try next
                position = (position + 1) % len(self.table)
                self.probeChainIncrement()
                self.probeMaxCounterIncrement()

        raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        """
        Checks to see if the given key is in the Hash Table
        :see: #self.__getitem__(self, key: str)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> T:
        """
        Get the item at a certain key
        :see: #self.__linear_probe(key: str, is_insert: bool)
        :raises KeyError: when the item doesn't exist
        """
        position = self.__linear_probe(key, False)
        return self.table[position][1]

    def __setitem__(self, key: str, data: T) -> None:
        """
        Set an (key, data) pair in our hash table
        :see: #self.__linear_probe(key: str, is_insert: bool)
        :see: #self.__rehash()
        """

        if (self.count/len(self.table)) > 0.5:
            self.__rehash()

        # if self.is_full():
        #     self.__rehash()
        position = self.__linear_probe(key, True)

        if self.table[position] is None:
            self.count += 1
        self.table[position] = (key, data)

    def is_empty(self):
        """
        Returns whether the hash table is empty
        :complexity: O(1)
        """
        return self.count == 0

    def is_full(self):
        """
        Returns whether the hash table is full
        :complexity: O(1)
        """
        return self.count == len(self.table)

    def hash(self, key: str) -> int:
        """
        Universal Hash function
        :post: returns a valid position (0 <= value < table_size)
        :complexity: O(K) where K is the size of the key
        """
        value = 0
        for c in key:
            value = (value * self.hash_base + ord(c)) % len(self.table)
        return value

    def insert(self, key: str, data: T) -> None:
        """
        Utility method to call our setitem method
        :see: #__setitem__(self, key: str, data: T)
        """
        self[key] = data

    def statistics(self) -> Tuple:
        """
        It is a method that returns a tuple, containing collision_count, probe_total, probe_max, and rehash_count
        :return Tuple:
        """
        tuple_stats = (self.getCollisionCounter(), self.getProbeChainCounter(), self.getProbeMax(),
                       self.getRehashCounter())

        return tuple_stats

    def collisionCounterIncrement(self):
        """
        A method to increment a collision counter by one
        :return None:
        :complexity: O(1)
        """
        self.collision_counter += 1

    def getCollisionCounter(self):
        """
        A getter for collision_counter
        :return collision_counter:
        :complexity: O(1)
        """
        return self.collision_counter

    def probeChainIncrement(self):
        """
        A method to increment a probe_chain_counter by one
        :return None:
        :complexity: O(1)
        """
        self.probe_chain_counter += 1

    def getProbeChainCounter(self):
        """
        A getter for probe_chain_counter
        :return probe_chain_counter:
        :complexity: O(1)
        """
        return self.probe_chain_counter

    def rehashCounterIncrement(self):
        """
        A method to increment a rehash_counter by one
        :return None:
        :complexity: O(1)
        """
        self.rehash_counter += 1

    def getRehashCounter(self):
        """
        A getter for rehash_counter
        :return rehash_counter:
        :complexity: O(1)
        """
        return self.rehash_counter

    def getProbeMax(self):
        """
        A getter for ProbeMax
        :return max value of probe_max_counter stored inside probe_max or 0:
        :complexity: O(1)
        """
        try:
            return max(self.probe_max)
        except ValueError:
            return 0

    def getProbeMaxCounter(self):
        """
        A getter for probe_max_counter
        :return probe_max_counter:
        :complexity: O(1)
        """
        return self.probe_max_counter

    def probeMaxCounterIncrement(self):
        """
        A method to increment a probe_max_counter by one
        :return None:
        :complexity: O(1)
        """
        self.probe_max_counter += 1

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular order)
        :complexity: O(N) where N is the table size
        """
        result = ""
        for item in self.table:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result


class TestLinearProbeHashTable(unittest.TestCase):
    def test_init(self):
        """ Basic test to ensure the table is initialised """
        dictionary = LinearProbeHashTable()
        self.assertEqual(len(dictionary), 0, "Dictionary should be empty")

    def test_is_empty(self):
        """ Testing when the table is empty and non-empty """
        dictionary = LinearProbeHashTable()
        self.assertTrue(dictionary.is_empty())

        dictionary["test"] = "test"
        self.assertFalse(dictionary.is_empty())

    def test_is_full(self):
        """ Testing when the hash table is full and empty """
        dictionary = LinearProbeHashTable(31, 10)
        self.assertFalse(dictionary.is_full())

        for i in range(10):
            dictionary[str(i)] = i
        self.assertTrue(len(dictionary) == 10)

    def test_hash(self):
        """ Testing the get item and contains """
        dictionary = LinearProbeHashTable(31, 5)
        for i in range(10):
            dictionary[str(i)] = i

        for i in range(10):
            self.assertEqual(dictionary[str(i)], i, "Could not find item: " + str(i))
            self.assertTrue(str(i) in dictionary, "Could not find item: " + str(i))

    def test_len(self):
        """ Testing an empty Hash Table and non-empty Hash Table """
        dictionary = LinearProbeHashTable(5)
        self.assertEqual(len(dictionary), 0, "Dictionary should be empty")

        for i in range(3):
            dictionary[str(i)] = i

        self.assertEqual(len(dictionary), 3, "Dictionary should contain 3 items")

    def test_del(self):
        """ Adding 10 items, removing the first 5 and ensuring the state of the Hash Table is correct afterwards """
        dictionary = LinearProbeHashTable(5)
        for i in range(10):
            dictionary[str(i)] = i

        for i in range(5):
            del dictionary[str(i)]

        for i in range(10):
            if i < 5:
                with self.assertRaises(KeyError):
                    _ = dictionary[str(i)]
            else:
                self.assertEqual(dictionary[str(i)], i, "Could not find item: " + str(i))

    def test_statistics(self):
        # TODO create more complicated test cases!!!

        # TEST CASE 1
        dictionary = LinearProbeHashTable(31, 5)
        tuple_test = (0, 0, 0, 0)
        self.assertTrue(dictionary.statistics(), tuple_test)

        # TEST CASE 2
        dictionary = LinearProbeHashTable(0, 0)
        tuple_test = (0, 0, 0, 0)
        self.assertTrue(dictionary.statistics(), tuple_test)

    def test_str(self):
        """ Testing an empty table and one with 5 elements """
        dictionary = LinearProbeHashTable(31, 5)
        self.assertEqual(str(dictionary), "", "Dictionary should be empty")

        for i in range(5):
            dictionary[str(i)] = i
        for i in range(5):
            self.assertIn("(" + str(i) + "," + str(i) + ")", str(dictionary))


if __name__ == '__main__':
    unittest.main()