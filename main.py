# project aims to implement an indexed-sequential file with
# some avaiable operations, like: inserting, reading, deleting and updating a record for start

# record::::student index + his 3 scores + key(natural number)
# sorting by key

RECORDS_PER_PAGE = 4  # Blocking factor for primary area


def sortingKey(o):
    return o.key


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
            self.page_entries.append(record)
            self.page_entries.sort(key=sortingKey)
            return 'inserted'


class Index:
    def __init__(self):
        self.key_page_dictionary = {}
        iFile = open("index.bin", 'wb')

    def getPage(self, key):
        for i in range(key, -1, -1):
            if i in self.key_page_dictionary:
                return self.key_page_dictionary[i]
        return None  # None, if no page corresponding with such key found

    def makeEntry(self, key, page):
        # make an entry with given key and page
        self.key_page_dictionary[key] = page


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
        self.getLastRecordInChain(chain_start).overflowPointer = record  # insert record at the end of chain
        self.records.append(record)  # HERE WRITE TO FILE INSTEAD

    def getLastRecordInChain(self, record):
        if record.overflowPointer is None:
            return record
        else:
            return self.getLastRecordInChain(record.overflowPointer)


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


ISFile = IndexedSequentialFile()
ISFile.insertRecord(Record(1))
ISFile.insertRecord(Record(4))
ISFile.insertRecord(Record(7))
ISFile.insertRecord(Record(2))
ISFile.insertRecord(Record(9))
ISFile.insertRecord(Record(8))
print('x')
