# from flask import Flask, render_template, request
# from flask_mysqldb import MySQL

# app=Flask(__name__)

# app.config['MYSQL_HOST']="localhost"
# app.config['MYSQL_USER']="root"
# app.config['MYSQL_PASSWORD']="Kopal2005@"
# app.config['MYSQL_DB']="questionnaire_database"

# mysql=MySQL(app)

# @app.route('/', methods=['GET','POST'])
# def index():

#     if request.method =="POST":
#         age = request.form['age']
#         gender = request.form['gender']
#         fitness = request.form['fitness']
#         mood = request.form['mood']
#         motivation = request.form['motivation']
#         connectedness = request.form['connectedness']
#         energy = request.form['energy']
#         sleep = request.form['sleep']
#         interest = request.form['interest']
#         time = request.form['time']
    
#         cur=mysql.connection.cursor()

#         cur.execute("INSERT INTO Table1 (age, gender, fitness_level, mood, motivation, connectedness, energy, sleep_quality, interest, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (age, gender, fitness, mood, motivation, connectedness, energy, sleep, interest, time))

#         mysql.connection.commit()

#         cur.close()

#         return "success"

#     return render_template('questionarrie.html')

# if __name__=="__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from model import predict_suggestions, fetch_user_data  # Import your functions

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Kopal2005@"
app.config['MYSQL_DB'] = "questionnaire_database"

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # Get user input from the form
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
    
        cur = mysql.connection.cursor()

        # Insert user data into the database
        cur.execute(
            "INSERT INTO Table1 (age, gender, fitness_level, mood, motivation, connectedness, energy, sleep_quality, interest, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
            (user_input['age'], user_input['gender'], user_input['fitness_level'], user_input['mood'], user_input['motivation'], user_input['connectedness'], user_input['energy'], user_input['sleep_quality'], user_input['interest'], user_input['time'])
        )

        mysql.connection.commit()
        cur.close()

        # Get suggestions from the model
        workout_suggestion, meditation_suggestion, yoga_suggestion = predict_suggestions(user_input)
        import os
        print(os.path.abspath('templates/suggestions.html'))

        # Return suggestions to the user
        return render_template('suggestions.html', 
                               workout=workout_suggestion, 
                               meditation=meditation_suggestion, 
                               yoga=yoga_suggestion)

    return render_template('questionarrie.html')

if __name__=="__main__":
    app.run(debug=True)