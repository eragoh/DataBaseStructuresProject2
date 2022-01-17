# project aims to implement an indexed-sequential file with
# some avaiable operations, like: inserting, reading, deleting and updating a record for start

# record::::student index + his 3 scores + key(natural number)
# sorting by key

class IndexedSequentialFile:
    pass  # Level? Arrays of Indexes/Cylinders?


class Record:
    def __init__(self, studentIndex, scores, sort_key, overflowPointer = None):
        self.studentIndex = studentIndex
        self.scores = scores  # list of 3 scores
        self.sort_key = sort_key  # natural number
        self.overflowPointer = overflowPointer
        # probably some getOverflow() method


# dictionary of key : primary_area(like a pointer to it)
index = {}
# dictionary of key : Record(class with Data + Overflow pointer)
primary_area = {}
# dictionary of key : Record(class with Data + Overflow pointer)
overflow_area = {}


