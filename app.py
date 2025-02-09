from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from model import predict_suggestions, fetch_user_data 

app = Flask(__name__)
from dotenv import load_dotenv
import os

load_dotenv()

app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
app.config['MYSQL_PORT'] = 3306  

# app.config['MYSQL_HOST'] = "localhost"
# app.config['MYSQL_USER'] = "root"
# app.config['MYSQL_PASSWORD'] = "Kopal2005@"
# app.config['MYSQL_DB'] = "questionnaire_database"

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        user_input = {
            'age': request.form['age'],
            'gender': request.form['gender'],
            'fitness_level': request.form['fitness'],
            'mood': request.form['mood'],
            'motivation': request.form['motivation'],
            'connectedness': request.form['connectedness'],
            'energy': request.form['energy'],
            'sleep_quality': request.form['sleep'],
            'interest': request.form['interest'],
            'time': request.form['time']
        }
    
        # cur = mysql.connection.cursor()

        # cur.execute(
        #     "INSERT INTO Table1 (age, gender, fitness_level, mood, motivation, connectedness, energy, sleep_quality, interest, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
        #     (user_input['age'], user_input['gender'], user_input['fitness_level'], user_input['mood'], user_input['motivation'], user_input['connectedness'], user_input['energy'], user_input['sleep_quality'], user_input['interest'], user_input['time'])
        # )
        

        # mysql.connection.commit()
        # cur.close()
        
        try:
            cur = mysql.connection.cursor()
            query = """
            INSERT INTO Table1 
            (age, gender, fitness_level, mood, motivation, connectedness, energy, sleep_quality, interest, time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (
                user_input['age'], user_input['gender'], user_input['fitness_level'], 
                user_input['mood'], user_input['motivation'], user_input['connectedness'], 
                user_input['energy'], user_input['sleep_quality'], user_input['interest'], user_input['time']
            ))

            mysql.connection.commit()
            cur.close()

        except Exception as e:
            print("Database Error:", e)

        workout_suggestion, meditation_suggestion, yoga_suggestion = predict_suggestions(user_input)
        # import os
        # print(os.path.abspath('templates/suggestions.html'))

        # Return suggestions to the user
        return render_template('suggestions.html', 
                               workout=workout_suggestion, 
                               meditation=meditation_suggestion, 
                               yoga=yoga_suggestion)

    return render_template('questionarrie.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)