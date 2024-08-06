from database import DatabaseOperations
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


class recommended_doctors:
    def __init__(self):
        # connection string
        self.connection_string = Commection_String
        self.db_operations = DatabaseOperations(self.connection_string)

    def get_data(self):
        try:
            data_list = self.db_operations.merge_collections()
            df = pd.DataFrame(data_list)
            df = df.rename(columns={'Doctor Name': 'Doctor_Name',
                                    'Number Of Patients': 'Number_Of_Patients',
                                    'Satisfaction level': 'Satisfaction_level',
                                    'Hospital Name': 'Hospital_Name'})

            return df
        except Exception as e:
            print(f"Error occurred while fetching data: {e}")
            return None

    def preprocess_data(self, df):
        X = df[['Experience', 'Number_Of_Patients', 'Fees']]
        y = df['Satisfaction_level'] > 95  # Binary target variable based on satisfaction level threshold
        return X, y

    def train_model(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.60, random_state=42)
        model = LogisticRegression()
        model.fit(X_train, y_train)
        return model, X_test

    def get_recommended_doctors(self):
        df = self.get_data()
        if df is not None:
            X, y = self.preprocess_data(df)
            model, X_test = self.train_model(X, y)
            y_pred = model.predict(X_test)
            recommended_doctors = df.iloc[X_test.index[y_pred]]
            recommended_doctors = recommended_doctors[recommended_doctors['Number_Of_Patients'] >= 100]
            data = recommended_doctors[
                ['Doctor_Name', 'Specialty', 'Experience', 'Number_Of_Patients', 'Fees', 'Degree',
                 'Satisfaction_level', 'Hospital_Name', 'Waiting']]
            return data.to_dict('records')
        else:
            return None

