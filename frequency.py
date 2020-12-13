from hash_table import LinearProbeHashTable
from dictionary import Dictionary
from list_adt import ArrayList
from enum import Enum
from typing import Tuple, List
import random
from string import punctuation
import sys


class Rarity(Enum):
    """
    A Subclass of Enum is Rarity class that contains Enum member values.
    This makes them easy to read and hence this class is used for readability purpose.
    """
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    MISSPELT = 3


class Frequency:
    """
    Frequency class is a class that keeps tack of words and their occurrences from an updated
    file and create a ranking system.

    attributes:
        hash_table: An instance of LinearProbeHashTable.
        dictionary: An instance of Dictionary.
        max_word_arr: A list of a tuple that contains word and its occurrence data.
        max_word: A tuple of a word with the highest occurrence.
    """

    def __init__(self) -> None:
        """
        We create an instance of dictionary and load a dictionary that is used to
        evaluate an occurrence of a word. Also, hash table is created with an instance of
        LinearProbeHashTable.

        :complexity: O(1)
        :pre: it must call the correct name of the file for self.dictionary.load_dictionary()
        """
        self.hash_table = LinearProbeHashTable(250726, 1000081)
        self.dictionary = Dictionary(250726, 1000081)
        self.dictionary.load_dictionary("english_large.txt")
        self.max_word_arr = list()
        self.max_word = tuple()
        self.sorted_arr = list()

    def add_file(self, filename: str) -> None:
        """
        It reads every word in a file and insert only a word that appears in english_large.txt
        file. It also keeps a track of how many times the word appears in the file to count its
        occurrence. These data are also added in max_word_arr array.

        :param filename: A name of a file to be added
        :type filename: String
        :return: None
        :complexity: O(N^2) for the worst case and O(N) for the best case
        :raises: FileNotFoundError when a file name does not exist
        :pre: filename should be the name of a file that exists.

        """

        try:
            file = open(filename, encoding='UTF-8')
        except FileNotFoundError:
            raise FileNotFoundError("The file name does not exist.")

        for line in file:

            for word in line.split():
                word = word.strip(punctuation)
                word = word.lower()

                if self.dictionary.find_word(word) is True:
                    if word in self.hash_table:
                        counter = self.hash_table[word]
                        self.hash_table[word] = counter + 1

                        for i in range(len(self.max_word_arr)):
                            if self.max_word_arr[i][0] == word:
                                list_ver = list(self.max_word_arr[i])
                                list_ver[1] = counter + 1
                                self.max_word_arr[i] = tuple(list_ver)

                        continue

                    self.hash_table.insert(word, 1)
                    tuple_data = (word, 1)
                    self.max_word_arr.append(tuple_data)

        file.close()

        # Reference: https://www.geeksforgeeks.org/python-min-and-max-value-in-list-of-tuples/
        self.max_word = (max(self.max_word_arr, key=lambda item: item[1]))  # finding a word with the highest occurrence

    def rarity(self, word: str) -> Rarity:
        """
        This method is used to calculate a rarity score of a given word and return the value
        as an enumerated value.

        :param word: A word that is read for calculating its rarity score.
        :type word: String
        :return: Rarity
        :complexity: O(N^2) for the worst case and O(N) for the best case
        """

        word = word.lower()
        if word in self.hash_table:
            if self.hash_table[word] >= (self.max_word[1] / 100):
                return Rarity.COMMON

            if self.hash_table[word] < (self.max_word[1] / 1000):
                return Rarity.RARE

            if (self.max_word[1] / 100) > self.hash_table[word] >= (self.max_word[1] / 1000):
                return Rarity.UNCOMMON
        else:
            return Rarity.MISSPELT

    def ranking(self) -> ArrayList[tuple]:
        """
        Creates a list of tuples that contain words associated with its occurrence data
        that is sorted by QuickSort function in descending order.

        :return: ArrayList[tuple]
        :complexity: O(N) for best/worst case
        """
        self.sorted_arr = ArrayList(len(self.max_word_arr))
        for i in range(len(self.max_word_arr)):
            self.sorted_arr.insert(i, self.max_word_arr[i])

        qsort(self.sorted_arr)
        return self.sorted_arr


def qsort(array: List[int]) -> None:
    """
     A public interface for quick sort.
     :param array: An array to be processed
     :type array: List[int]
     :return: None
     :complexity: O(1) for best/worst case
     Reference: Week 11 WorkShop QuickSort Algorithm https://edstem.org/courses/4462/lessons/6356/slides/45584

    """

    random.seed()
    _qsort_aux(array, 0, len(array) - 1)


def _partition(array: List[int], low: int, high: int) -> int:
    """
    it creates a pivot at random index in the array range and it allocates
    smaller elements to the left and bigger ones to the right.
    Then, it returns the pivot.

    :param array: an array to be processed
    :type array: List[int]
    :param low: a start index of the array
    :type low: int
    :param high: an end index of the array
    :type high: int
    :return: pivot
    :complexity: O(log n) for the best case, O(n) for the worst case
    Reference: Week 11 WorkShop QuickSort Algorithm https://edstem.org/courses/4462/lessons/6356/slides/45584

    """

    # selecting a pivot randomly
    pivot = random.choice(range(low, high + 1))

    swap(array, pivot, low)
    pivot = low
    for k in range(low + 1, high + 1):
        if array[k][1] > array[low][1]:  # where the pivot sits
            pivot += 1
            swap(array, pivot, k)
    swap(array, pivot, low)
    return pivot


def swap(array, i, j):
    """
    It swaps an element of i and an element of j from an array.
    :param array: An array to be processed 
    :type array: list
    :param i: an index of array to be swapped
    :type i: int
    :param j: an index of array to be swapped
    :type j: int
    :return: None
    :complexity: O(1) for best/worst case
    Reference: Week 11 WorkShop QuickSort Algorithm https://edstem.org/courses/4462/lessons/6356/slides/45584

    """
    array[i], array[j] = array[j], array[i]


def _qsort_aux(array: List[int], low: int, high: int) -> None:
    """
    It uses tail recursive to create two partitions separated by a boundary and
    sort in descending order.

    :param array: an array to be processed
    :type array: List[int]
    :param low: a start index of the array
    :type low: int
    :param high: an end index of the array
    :type high: int
    :return: None
    :complexity: O(1) for best/worst case
    Reference: Week 11 WorkShop QuickSort Algorithm https://edstem.org/courses/4462/lessons/6356/slides/45584

    """

    # non base case
    if low < high:
        boundary = _partition(array, low, high)
        _qsort_aux(array, low, boundary - 1)
        _qsort_aux(array, boundary + 1, high)


def frequency_analysis() -> None:
    """
    It asks a user for the number of rankings to display.
    It creates an instance of Frequency and it adds 215-0.txt and generates a ranking
    :raises KeyError: When the input is not a number.
    :return: None
    :complexity: O(N) for best/worst case
    :raises: ValueError when num_ranking is not a number
    :pre:num_ranking must be in an integer form
    """
    try:
        num_ranking = int(input("Enter the number of rankings to display\n"))
    except ValueError:
        # https://stackoverflow.com/questions/52725278/during-handling-of-the-above-exception-another-exception
        # -occurred
        raise ValueError("Invalid! PLease make sure the input value is a number") from None

    frequency_ranking = Frequency()
    frequency_ranking.add_file("215-0.txt")
    ranks = frequency_ranking.ranking()[0:num_ranking]

    for i, word in enumerate(ranks):
        print(f"{i + 1}: '{word[0]}', the occurrence of the word is {word[1]}, and its rarity is "
              f"{frequency_ranking.rarity(word[0])} \n")


if __name__ == '__main__':
    frequency = Frequency()
    frequency.add_file("215-0.txt")
    print(frequency.rarity("The"))

