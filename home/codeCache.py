import time


class CodeCache:

    def __init__(self):
        self.__data = {}

    def get(self, paper_name, question_index, userid):
        if (paper_name, question_index, userid) in self.__data:
            code_segment, time_stamp = self.__data[(paper_name, question_index, userid)]
            if time.time() - time_stamp < 3600 * 24:  # expire after 1 day
                return code_segment
            del self.__data[(paper_name, question_index, userid)]
        return None

    def add(self, paper_name, question_index, userid, code_segment):
        self.__data[(paper_name, question_index, userid)] = (code_segment, time.time())

    def dump(self):
        print('--------- Code Cache ---------')
        for key in self.__data:
            print("({}, {}, {}) -> ({}, {})".format(key[0], key[1], key[2], self.__data[key][0], self.__data[key][1]))
        print('------------------------------')