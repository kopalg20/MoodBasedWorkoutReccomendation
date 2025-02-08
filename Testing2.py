import unittest
from unittest.mock import patch
import mysql.connector
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Assuming the model and functions are defined as follows:

# Mock data to simulate database output
mock_user_data = [
    {'age': 25, 'gender': 'female', 'fitness_level': 'beginner', 'mood': 'happy', 'motivation': 'high', 'connectedness': 'moderate', 'energy': 'medium', 'time': 'morning'},
    {'age': 30, 'gender': 'male', 'fitness_level': 'intermediate', 'mood': 'sad', 'motivation': 'low', 'connectedness': 'high', 'energy': 'low', 'time': 'evening'}
]

# Mock fetch_user_data function to return mock_user_data instead of querying the database
def mock_fetch_user_data():
    return mock_user_data

class TestModel(unittest.TestCase):

    @patch('mysql.connector.connect')
    def test_predict_suggestions(self, mock_db_connect):
        # Create mock database connection and mock cursor
        mock_cursor = mock_db_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = mock_user_data
        
        # Load and preprocess mock dataset (same as original code)
        data = pd.read_excel('mood__dataset__.xlsx')
        data.to_csv("mood_dataset_.csv", index=False)

        label_encoders = {}
        for column in data.columns:
            if data[column].dtype == 'object':
                le = LabelEncoder()
                data[column] = le.fit_transform(data[column])
                label_encoders[column] = le

        X = data.drop(['Suggested Workout', 'Suggested Meditation', 'Suggested Yoga'], axis=1)  # Drop target variables
        y_workout = data['Suggested Workout']
        y_meditation = data['Suggested Meditation']
        y_yoga = data['Suggested Yoga']

        # Split the dataset into training and testing sets
        X_train, X_test, y_train_workout, y_test_workout = train_test_split(X, y_workout, test_size=0.2, random_state=42)
        X_train, X_test, y_train_meditation, y_test_meditation = train_test_split(X, y_meditation, test_size=0.2, random_state=42)
        X_train, X_test, y_train_yoga, y_test_yoga = train_test_split(X, y_yoga, test_size=0.2, random_state=42)

        # Train the models
        model_workout = RandomForestClassifier(n_estimators=50, random_state=42)
        model_workout.fit(X_train, y_train_workout)

        model_meditation = RandomForestClassifier(n_estimators=100, random_state=42)
        model_meditation.fit(X_train, y_train_meditation)

        model_yoga = RandomForestClassifier(n_estimators=100, random_state=42)
        model_yoga.fit(X_train, y_train_yoga)

        # Function to predict suggestions
        def predict_suggestions(user_input):
            input_data = pd.DataFrame([user_input])
            for column in input_data.columns:
                if column in label_encoders:
                    if user_input[column] in label_encoders[column].classes_:
                        input_data[column] = label_encoders[column].transform(input_data[column])
                    else:
                        input_data[column] = 0
                else:
                    input_data[column] = 0  

            input_data = input_data[X.columns]

            workout_prediction = model_workout.predict(input_data)
            meditation_prediction = model_meditation.predict(input_data)
            yoga_prediction = model_yoga.predict(input_data)

            workout_suggestion = label_encoders['Suggested Workout'].inverse_transform(workout_prediction)
            meditation_suggestion = label_encoders['Suggested Meditation'].inverse_transform(meditation_prediction)
            yoga_suggestion = label_encoders['Suggested Yoga'].inverse_transform(yoga_prediction)

            return workout_suggestion[0], meditation_suggestion[0], yoga_suggestion[0]

        # Test prediction for the mock user data
        for user_input in mock_user_data:
            suggested_workout, suggested_meditation, suggested_yoga = predict_suggestions(user_input)

            # Check that predictions are returned
            self.assertIsNotNone(suggested_workout)
            self.assertIsNotNone(suggested_meditation)
            self.assertIsNotNone(suggested_yoga)

            print(f'Suggested Workout: {suggested_workout}')
            print(f'Suggested Meditation: {suggested_meditation}')
            print(f'Suggested Yoga: {suggested_yoga}')
            print('---')

if __name__ == '__main__':
    unittest.main()
