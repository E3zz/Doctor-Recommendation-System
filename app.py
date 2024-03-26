from flask import Flask, render_template, request, g
from flask_caching import Cache
from recommend import recommended_doctors
from database import user_feedback

app = Flask(__name__)
db_operations = user_feedback("mongodb+srv://yahyakhalid1272:Cj%40123456@mydb.kudw48y.mongodb.net/")
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
    return render_template("ent_recommendation.html", data=ent_doctors)


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
        print(request.form)  # Check if form data is being received correctly
        name = request.form['name']
        email = request.form['email']
        feedback_text = request.form['message']
        speciality = request.form['speciality']
        db_operations.save_feedback(name, email, feedback_text, speciality)

        return render_template("feedback.html", success=True)
    # Logic for handling GET request
    return render_template("feedback.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=5000)
