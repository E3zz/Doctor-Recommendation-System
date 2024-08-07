from flask import Flask, render_template, request, g
from flask_caching import Cache
from recommend import recommended_doctors
from database import user_feedback
import os


app = Flask(__name__)
db_operations = user_feedback("Connection String")
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)


def recommendations():
    if 'doc_recommender' not in g:
        g.doc_recommender = recommended_doctors()  # Assuming recommended_doctors is a class or function
    data = g.doc_recommender.get_recommended_doctors()
    return data


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/orthopedic")
@cache.memoize(100)
def ortho():
    data = recommendations()
    orthopedic_doctors = [doctor for doctor in data if 'orthopedic' in doctor['Specialty'].lower()]
    return render_template("orthopedic_recommendation.html", data=orthopedic_doctors)


@app.route("/Gynecologist")
@cache.memoize(100)
def gyn():
    data = recommendations()
    gynecologist_doctors = [doctor for doctor in data if 'gynecologist' in doctor['Specialty'].lower()]
    return render_template("gynecologist_recommendation.html", data=gynecologist_doctors)


@app.route("/ENT")
@cache.memoize(100)
def ent():
    data = recommendations()
    ent_doctors = [doctor for doctor in data if 'ent' in doctor['Specialty'].lower()]
    return render_template("ENT_recommendation.html", data=ent_doctors)


@app.route("/Diabetes")
@cache.memoize(100)
def diabetes():
    data = recommendations()
    diabetes_doctors = [doctor for doctor in data if 'diabetologist' in doctor['Specialty'].lower()]
    return render_template("diabetologist_recommendation.html", data=diabetes_doctors)


@app.route("/Dermatologist")
@cache.memoize(100)
def dermatologist():
    data = recommendations()
    dermatologist_doctors = [doctor for doctor in data if 'dermatologist' in doctor['Specialty'].lower()]
    return render_template("dermatologist_recommendation.html", data=dermatologist_doctors)


@app.route("/Pediatrician")
@cache.memoize(100)
def pediatrician():
    data = recommendations()
    pediatrician_doctors = [doctor for doctor in data if 'pediatrician' in doctor['Specialty'].lower()]
    return render_template("pediatrician_recommendation.html", data=pediatrician_doctors)


@app.route("/Eye")
@cache.memoize(100)
def eye():
    data = recommendations()
    eye_doctors = [doctor for doctor in data if 'eye specialist' in doctor['Specialty'].lower()]
    return render_template("eye_recommendation.html", data=eye_doctors)


@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    # fetch data from the form and save it into the database
    if request.method == 'POST':
        # Check if form data is being received correctly
        name = request.form['name']
        email = request.form['email']
        feedback_text = request.form['message']
        speciality = request.form['speciality']
        rating = request.form['rating']
        # Check if any of the required fields are empty and return a specific error message for each one
        if not name:
            return render_template("feedback.html", error="Name is required.", success=False)
        if not email:
            return render_template("feedback.html", error="Email is required.", success=False)
        if not feedback_text:
            return render_template("feedback.html", error="Feedback message is required.", success=False)
        # Save the feedback to the database
        db_operations.save_feedback(name, email, feedback_text, speciality, rating)
        return render_template("feedback.html", success=True)
    # Logic for handling GET request
    return render_template("feedback.html")





@app.route("/view_feedback", methods=['GET', 'POST'])
def view_feedback():
    feedback = db_operations.get_feedback()
    print(feedback)
    return render_template("view.html", feedback=feedback)

 

if __name__ == "__main__":
    # Use the PORT environment variable if available, otherwise use port 5000
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', debug=False, port=port)
