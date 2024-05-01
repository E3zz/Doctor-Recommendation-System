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


class user_feedback:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['feedback_db']
        self.feedback_collection = self.db['Feedback']

    def save_feedback(self, name, email, feedback_text, speciality, rating):
        feedback = {
            'name': name,
            'email': email,
            'feedback': feedback_text,
            'speciality': speciality,
            'rating': rating
        }
        self.feedback_collection.insert_one(feedback)

    def get_feedback(self):
        feedback_db = self.client['feedback_db']
        feedback_collection = feedback_db['Feedback']
        return list(feedback_collection.find())