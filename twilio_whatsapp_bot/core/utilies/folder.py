#!/usr/bin/python

from typing import Any


class Folder(object):
    
    def __init__(self, data_array: Any):
        self.data_array = data_array


    def check_probability_and_return_folder(self, sentence: str, column_array: str = "words") -> Any:
        index = -1
        res_index = -1
        #
        for i in range(0, len(self.data_array)):
            data_ = self.data_array[i]
            list_A = data_[column_array].split("-")
            res = 0
            for key in list_A:
                res += 1 if key in sentence else 0
            if res > 0 and res_index < res:
                res_index = res
                index = int(data_["folder"])
        #    
        return index

    
    def get_folders_as_default(self) -> Any:
        return_ = []
        i = 1
        # select all folder define in 0.json and propose that to user
        for data_ in self.data_array:
            return_.append(str(i) + ". " + data_["title"])
            i += 1
        return return_
    