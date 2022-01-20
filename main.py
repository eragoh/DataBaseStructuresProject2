# project aims to implement an indexed-sequential file with
# some avaiable operations, like: inserting, reading, deleting and updating a record for start

# record::::student index + his 3 scores + key(natural number)
# sorting by key

import bisect
from os.path import getsize
from pickle import dump as serialize
from pickle import load as deserialize
import pickle

RECORDS_PER_PAGE = 4  # Blocking factor for primary area
DISK_READS = 0
DISK_WRITES = 0
ALPHA = 0.5  # How much of each page is utilise after each reorganization
PAGE_BYTES_SIZE_LIMIT = 2048


class FileManager:
    DISK_READS = 0
    DISK_WRITES = 0

    def readFromFile(self, file):
        with open(file, "r") as f:
            return f.read()

    def writeToFile(self, file, text):
        with open(file, "w") as f:
            return f.write(text)

    def writeToPrimaryArea(self, page, offset):
        self.DISK_WRITES += 1
        with open("PrimaryArea.bin", "r+b") as f:
            f.seek(offset)
            serialize(page, f)
            #serialize(';', f)

    def readPageFromPrimaryArea(self, offset):
        self.DISK_READS += 1
        with open("PrimaryArea.bin", "rb") as f:
            f.seek(offset)
            return deserialize(f)

    @property
    def primaryAreaSize(self):
        return getsize("PrimaryArea.bin")

    @property
    def overflowAreaSize(self):
        return getsize("OverflowArea.bin")


class Page:
    def __init__(self):
        self.entries = []
        # SAVE PAGE

    def insertRecord(self, record):
        if len(self.entries) == RECORDS_PER_PAGE:
            # assign it to overflow of a record
            for entry in reversed(self.entries):
                if record.key > entry.key:
                    return entry  # return start of overflow chain
            return "ERROR 404"
        else:
            # bisect check where to insert
            # CHECK IF SEARCH_KEY WORKS
            bisect.insort_left(self.entries, record)
            # self.entries.insert(i, record)
            return 'inserted'


class Index:
    def __init__(self):
        self.key_page_map = []
        iFile = open("index.bin", 'wb')

    def getPageOffset(self, key):
        global DISK_READS
        DISK_READS += 1
        i = bisect.bisect_left(self.key_page_map, (key, )) - 1
        if i != -1:
            return self.key_page_map[i][1]
        return None  # None, if no page corresponding with such key found

    def makeEntry(self, key, page_offset):
        # make an entry with given key and page offset
        self.key_page_map.append((key, page_offset))


class Record:
    # only key is required
    def __init__(self, key, studentIndex=123456, scores=None, overflowPointer=None):
        self.key = key  # natural number
        self.studentIndex = studentIndex
        if scores is None:
            self.scores = [2.0, 3.5, 5.0]  # list of 3 default scores
        self.overflowPointer = overflowPointer
        # probably some getOverflow() method

    def __lt__(self, other):
        return self.key < other.key


class PrimaryArea:
    pages_number = 0

    def __init__(self):
        pass

    def makePage(self):
        new_page = Page()
        self.pages_number += 1
        return new_page


class OverflowArea:
    records = []

    def addRecordToChain(self, record, chain_start):
        global DISK_WRITES
        while chain_start.overflowPointer is not None:
            if chain_start.overflowPointer.key < record.key:
                chain_start = chain_start.overflowPointer
            else:
                break
        if chain_start.overflowPointer is None:
            DISK_WRITES += 1
            chain_start.overflowPointer = record
        else:
            DISK_WRITES += 3
            record.overflowPointer = chain_start.overflowPointer
            chain_start.overflowPointer = record
        self.records.append(record)  # HERE WRITE TO FILE INSTEAD


class IndexedSequentialFile:
    index = Index()
    primary_area = PrimaryArea()
    overflow_area = OverflowArea()
    FM = FileManager()

    def insertRecord(self, record):
        page_offset = self.index.getPageOffset(record.key)
        if page_offset is None:
            # REORGANISE, can't just make new page, index needs to be sorted after that
            self.reorganizeWithRecord(record)
            return
        page = self.FM.readPageFromPrimaryArea(page_offset)
        result = page.insertRecord(record)
        # self.FM.writeRecordToPage
        if result != 'inserted':
            self.overflow_area.addRecordToChain(record, result)
        self.FM.writeToPrimaryArea(page, page_offset)

    def readRecord(self, key):
        page = self.index.getPageOffset(key)

    def reorganizeWithRecord(self, record):
        if self.FM.primaryAreaSize + self.FM.overflowAreaSize == 0:
            # this record is the first one
            new_page = self.primary_area.makePage()
            new_page.insertRecord(record)
            # Page ready -> Write page to PrimaryArea
            self.FM.writeToPrimaryArea(new_page, 0)
            # Create index entry
            self.index.makeEntry(record.key, 0)
        # rest later, now 1st record should work fine


ISFile = IndexedSequentialFile()

# TEST

with open("PrimaryArea.bin", 'w'):
    pass

ISFile.insertRecord(Record(5))
ISFile.insertRecord(Record(8))
ISFile.insertRecord(Record(11))
ISFile.insertRecord(Record(21))
ISFile.insertRecord(Record(7))
ISFile.insertRecord(Record(12))
ISFile.insertRecord(Record(13))
ISFile.insertRecord(Record(14))
ISFile.insertRecord(Record(6))

ISFile.insertRecord(Record(1))
ISFile.insertRecord(Record(4))
ISFile.insertRecord(Record(7))
ISFile.insertRecord(Record(2))
ISFile.insertRecord(Record(9))
ISFile.insertRecord(Record(8))

# +reorganization
# I assume that Index is all in RAM memory, so no disk operations needed here
# I assume overflow doesn't have pages

# Lets make it with indexes, overflow will be paged now, so pages will have index
# OverflowPointer will have (x,y) format, where x is a page number of overflow area
# and y is a record number on this page (y<RECORDS_PER_PAGE)

# Still Index in RAM? Cause i should decide if I page it, and then I have to count disk ops

# makeEntry will need rebuild when implementing reorganization

# what if next record is smaller than smalles at the moment? Reorganise?
# I can always start with 1 so then there will be no problem

# PrimaryArea data format:
# 0:0 KEY:STUDENT_INDEX:SCORE1:SCORE2:SCORE3:X:Y
# 0:1 None
# 0:2 None
# 0:3 None
# 1:0 None etc.
# 1:1
# 1:2

#insert
#seek
#reorginise when want to put lower than can
#classes to and from txt, will this work just like that?? Potential error
#check for reorganizations

#rozmiar przy 4 wpisach to 330B, spróbuję robić offsety co 450B

print('x')
