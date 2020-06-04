import time

class CodeCache:

    def __init__(self):
        self.__data = {}

    def get(self, paper_name, question_index, userid):
        if (paper_name, question_index, userid) in self.__data:
            code_segment, time_stamp = self.__data[(paper_name, question_index, userid)]
            if time.time() - time_stamp < 3600 * 24: #expire after 1 day
                return code_segment
            del self.__data[(paper_name, question_index, userid)]
        return None


    def add(self, paper_name, question_index, userid, code_segment):
        self.__data[(paper_name, question_index, userid)] = (code_segment, time.time())