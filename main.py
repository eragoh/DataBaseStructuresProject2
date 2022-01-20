# project aims to implement an indexed-sequential file with
# some avaiable operations, like: inserting, reading, deleting and updating a record for start

# record::::student index + his 3 scores + key(natural number)
# sorting by key

import bisect

RECORDS_PER_PAGE = 4  # Blocking factor for primary area
DISK_READS = 0
DISK_WRITES = 0


def sortingKey(o):
    return o.key


class FileManager:
    def readFromFile(self, file):
        with open(file, "r") as f:
            return f.read()

    def writeToFile(self, file, text):
        with open(file, "w") as f:
            return f.write(text)


class Page:
    def __init__(self):
        self.page_entries = []
        # SAVE PAGE

    def insertRecord(self, record):
        if len(self.page_entries) == RECORDS_PER_PAGE:
            # assign it to overflow of a record
            for entry in reversed(self.page_entries):
                if record.key > entry.key:
                    return entry  # return start of overflow chain
            return "ERROR 404"
        else:
            global DISK_WRITES
            DISK_WRITES += 1
            self.page_entries.append(record)
            self.page_entries.sort(key=sortingKey)
            return 'inserted'


class Index:
    def __init__(self):
        self.key_page_map = []
        iFile = open("index.bin", 'wb')

    def getPage(self, key):
        global DISK_READS
        DISK_READS += 1
        i = bisect.bisect_left(self.key_page_map, (key,)) - 1
        if i != -1:
            return self.key_page_map[i][1]
        return None  # None, if no page corresponding with such key found

    def makeEntry(self, key, page):
        # make an entry with given key and page
        self.key_page_map.append((key, page))


class Record:
    # only key is required
    def __init__(self, key, studentIndex=123456, scores=None, overflowPointer=None):
        self.key = key  # natural number
        self.studentIndex = studentIndex
        if scores is None:
            self.scores = [2.0, 3.5, 5.0]  # list of 3 default scores
        self.overflowPointer = overflowPointer
        # probably some getOverflow() method


class PrimaryArea:
    pages = []

    def __init__(self):
        pass

    def makePage(self):
        new_page = Page()
        self.pages.append(new_page)  # HERE WRITE TO FILE INSTEAD
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

    def insertRecord(self, record):
        page = self.index.getPage(record.key)
        if page is None:
            page = self.primary_area.makePage()
            self.index.makeEntry(record.key, page)
        result = page.insertRecord(record)
        if result != 'inserted':
            self.overflow_area.addRecordToChain(record, result)

    def readRecord(self, key):
        page = self.index.getPage(key)


ISFile = IndexedSequentialFile()

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
print('x')
