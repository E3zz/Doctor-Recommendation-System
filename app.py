from flask import Flask, render_template, request, g
from flask_caching import Cache
from recommend import recommended_doctors

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)


def recommendations():  # This function is used to get the recommended doctors
    doc_recommender = g.recommeded_doctors()
    g.data = doc_recommender.get_recommended_doctors()
    return g.data


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=5000)
