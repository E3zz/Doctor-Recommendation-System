from pymongo import MongoClient


class DatabaseOperations:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['Drinfo']
        self.collections = ['Pediatrician', 'Orthopedic', 'Gynecologist', 'Eye', 'ENT', 'Diabetologist',
                            'Dermatologist']

    def merge_collections(self):
        records_list = []
        for collection_name in self.collections:
            collection = self.db[collection_name]
            records = collection.find({})
            records_list.extend(list(records))
        return records_list
