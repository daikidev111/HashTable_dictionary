import timeit
from hash_table import LinearProbeHashTable
from typing import Tuple


class Statistics:
    """
    Statistics class is a class to output all the counters and other elements
    required for analysis in csv format.
    """

    def load_statistics(self, hash_base: int, table_size: int, filename: str, max_time: int) -> Tuple:
        """
        load statistics is a method that creates an instance of Dictionary and time the loading time to see if it
        exceeds its determined max_time and also it calls a statistics method from LinearProbe class to get all the
        counter value.

        :param hash_base: a base for hash table
        :type hash_base: int
        :param table_size: a size of the hash table
        :type table_size: int
        :param filename: a file to be processed with
        :type filename: str
        :param max_time: a limit for loading time of a file
        :type max_time: int
        :return: words, time, collision_count, probe_total, probe_max, rehash_count
        :complexity: O(1)
        """
        dictionary = Dictionary(hash_base, table_size)

        try:
            start_time = timeit.default_timer()
            words = dictionary.load_dictionary(filename, max_time)
            end_time = timeit.default_timer()
            collision_count, probe_total, probe_max, rehash_count = dictionary.hash_table.statistics()
            time = end_time - start_time

        except TimeoutError:
            words = len(dictionary.hash_table)
            time = max_time
            print(f"Loading time has exceeded the limit of {max_time}")
            collision_count, probe_total, probe_max, rehash_count = dictionary.hash_table.statistics()

        return words, time, collision_count, probe_total, probe_max, rehash_count

    def table_load_statistics(self, max_time: int) -> None:
        """
        This method opens a writeable csv file and writes all the required values in a proper format.
        It uses three for loop to create 27 combinations from three arrays of table_size, filename, base_list.

        :param max_time: a limit for loading time of a file
        :type max_time: int
        :return: None
        :complexity: O(N)
        """

        file = open('output_task2.csv', 'w')

        file.write("FileName" + "," + "Table Size" + "," + "Hash Base" + "," + "Total Words" + "," + "Total Collision"
                   + "," + "Total Probe Length" + "," + "Maximum Probe Length" + ","
                   + "Rehash Count" + "," + "Loading Time" + "\n")

        table_size = [250727, 402221, 1000081]
        filename = ["french.txt", "english_small.txt", "english_large.txt"]
        base_list = [1, 27183, 250726]

        for index_base in base_list:
            for index_table in table_size:
                for index_file in filename:
                    words, time, collision_count, probe_total, probe_max, rehash_count = self.load_statistics(index_base, index_table, index_file, max_time)
                    file.write(index_file + "," + str(index_table) + "," + str(index_base) + "," + str(words)
                               + "," + str(collision_count) + "," + str(probe_total) + "," + str(probe_max)
                               + "," + str(rehash_count) + "," + str(time) + "\n"
                               )
        file.close()


class Dictionary:
    """
    Dictionary class creates an instance of LinearProbeHashTable class to create a hash table.
    Then, it prints out a menu where a user can choose whether to load its file, add a word, find a word, or
    delete a word.
    """

    def __init__(self, hash_base: int, table_size: int) -> None:
        """
        A constructor of Dictionary class
        :param hash_base: a base for hash table
        :type hash_base: int
        :param table_size: a size of hash table
        :type table_size: int
        :return None:
        :complexity: O(1)
        """
        self.hash_base = hash_base
        self.table_size = table_size
        self.hash_table = LinearProbeHashTable(self.hash_base, self.table_size)

    def load_dictionary(self, filename: str, time_limit: int = None) -> int:
        """
        A method that loads a file from the parameter. it calculates a loading time and if it exceeds its time limit it
        throws a TimeoutError.
        :param filename: a file to be loaded
        :type filename: str
        :param time_limit: a loadng time of a file
        :type time_limit: int or None
        :return length of a hash table from a chosen file:
        :complexity: O(N) for best/worst
        :pre: time_limit < elapsed_time
        """
        start_time = timeit.default_timer()
        file = open(filename, encoding='UTF-8')

        if type(time_limit) is int:  # time limit
            for word in file:
                self.hash_table.insert(word.rstrip(), 1)
                elapsed_time = timeit.default_timer() - start_time

                if time_limit < elapsed_time:
                    file.close()
                    raise TimeoutError("TimeoutError has occurred")

            file.close()
            return len(self.hash_table)

        else:  # no time limit
            for word in file:
                self.hash_table.insert(word.rstrip(), 1)

            file.close()
            return len(self.hash_table)

    def add_word(self, word: str) -> None:
        """
        This method uses insert function from the LinearProbeHashTable class to enable
        inserting a word inside a hash table.
        :param word: a word to be added inside the hash_table
        :return None:
        :complexity: O(1)
        """
        self.hash_table.insert(word.lower(), 1)

    def find_word(self, word: str) -> bool:
        """
        This method determines whether or not a word chosen from the parameter exists inside the hash table.
        :param word: a word to be found from the hash_table
        :type word: str
        :return bool:
        :complexity: O(N)
        """
        # return self.hash_table.__contains__(word)
        if word in self.hash_table:
            return True
        else:
            return False

    def delete_word(self, word: str) -> None:
        """
        This method uses del to enable deleting a word inside a hash table.
        :param word: a word to be deleted
        :type word: str
        :return None:
        :complexity: O(1)
        """
        # self.hash_table.__delitem__(word)
        del self.hash_table[word.lower()]

    def menu(self) -> None:
        """
        menu prints out all the available options for a user.
        :return None:
        :complexity: O(1)
        """
        print('\nMenu:')
        print('1.␣read a file')
        print('2.␣add a word')
        print('3.␣find a word')
        print('4.␣delete a word')
        print('5.␣quit')

    def menu_select(self):
        """
        A method that allows a user to constantly choose available options and create a restriction of what
        a user can type in the command. For example, if a user types an unknown file name in option 1, it calls
        FileNotFound error.
        :return None:
        :complexity: O(N) for best/worst
        :raises: FileNotFoundError when file is not found and TypeError when input word is digit.
        :pre: user_filename needs to have a correct existing file name, word_choice must not be a number.
        """
        selected_quit = False
        while not selected_quit:
            self.menu()
            command = int(input("\nEnter command:"))

            if command == 1:
                user_filename = str(input("Enter a name of the file\n"))
                choice = input("Would you like to limit the time of reading the file? -> Yes or No\n")
                try:
                    if choice == "Yes":
                        user_timeLimit = int(input("Please enter a time limit for reading a file in integer\n"))
                        print(self.load_dictionary(user_filename, time_limit=user_timeLimit))
                    if choice == "No":
                        print(self.load_dictionary(user_filename, time_limit=None))
                    if not (choice == "Yes" or choice == "No"):
                        raise Exception("Must choose either Yes or No")
                except FileNotFoundError:
                    raise FileNotFoundError(
                        "File name that you entered could not be found. Please enter the correct file "
                        "name.")

            elif command == 2:
                word_choice = input("Please enter a word you would like to add\n")
                if word_choice.isdigit():
                    raise TypeError("It must be a word, not a number")
                else:
                    self.add_word(word_choice)
                    print("The word you entered is successfully added to the dictionary")

            elif command == 3:
                word_choice = input("Please enter a word you would like to search\n")
                if word_choice.isdigit():
                    raise TypeError("It must be a word, not a number")
                else:
                    if self.find_word(word_choice) is True:
                        print(f"{word_choice} exists in the dictionary")
                    else:
                        print(f"{word_choice} does not exist in the dictionary")

            elif command == 4:
                word_choice = input("Please enter a word you would like to delete\n")
                if word_choice.isdigit():
                    raise TypeError("It must be a word, not a number")
                else:
                    self.delete_word(word_choice)
                    print("The word you entered is successfully deleted from the dictionary")

            elif command == 5:
                selected_quit = True
            else:
                print("Invalid option number. Please try again with valid number")


if __name__ == '__main__':
    stats = Statistics()
    stats.table_load_statistics(10)



