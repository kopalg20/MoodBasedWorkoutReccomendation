import mysql.connector
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import mysql.connector

# Connect to MySQL and fetch user data
def fetch_user_data():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kopal2005@",
        database="questionnaire_database"
    )
    query = "SELECT age,gender,fitness_level,mood,motivation,connectedness,energy,time FROM Table1"  # Replace 'user_table' with your actual table name
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    
    cursor.close()
    db_connection.close()
    return result
data = pd.read_excel('mood__dataset__.xlsx')
data.to_csv("mood_dataset_.csv",index=False)

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

model_workout = RandomForestClassifier(n_estimators=50, random_state=42)
model_workout.fit(X_train, y_train_workout)

model_meditation = RandomForestClassifier(n_estimators=100, random_state=42)
model_meditation.fit(X_train, y_train_meditation)

model_yoga = RandomForestClassifier(n_estimators=100, random_state=42)
model_yoga.fit(X_train, y_train_yoga)

print("Workout Model Evaluation:")
y_pred_workout = model_workout.predict(X_test)
print(classification_report(y_test_workout, y_pred_workout))

print("Meditation Model Evaluation:")
y_pred_meditation = model_meditation.predict(X_test)
print(classification_report(y_test_meditation, y_pred_meditation))

print("Yoga Model Evaluation:")
y_pred_yoga = model_yoga.predict(X_test)
print(classification_report(y_test_yoga, y_pred_yoga))

def predict_suggestions(user_input):
    input_data = pd.DataFrame([user_input])
    for column in input_data.columns:
        if column in label_encoders:
             if user_input[column] in label_encoders[column].classes_:
                input_data[column] = label_encoders[column].transform(input_data[column])
             else:
                input_data[column] = 0
        else : 
                input_data[column] = 0  

    input_data = input_data[X.columns]  

    workout_prediction = model_workout.predict(input_data)
    meditation_prediction = model_meditation.predict(input_data)
    yoga_prediction = model_yoga.predict(input_data)

    workout_suggestion = label_encoders['Suggested Workout'].inverse_transform(workout_prediction)
    meditation_suggestion = label_encoders['Suggested Meditation'].inverse_transform(meditation_prediction)
    yoga_suggestion = label_encoders['Suggested Yoga'].inverse_transform(yoga_prediction)

    return workout_suggestion[0], meditation_suggestion[0], yoga_suggestion[0]

user_data = fetch_user_data()

for user_input in user_data:
    suggested_workout, suggested_meditation, suggested_yoga = predict_suggestions(user_input)
    print(f'Suggested Workout: {suggested_workout}')
    print(f'Suggested Meditation: {suggested_meditation}')
    print(f'Suggested Yoga: {suggested_yoga}')
    print('---')  