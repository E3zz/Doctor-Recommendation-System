from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/orthopedic")
def ortho():
    return render_template("orthopedic_recommendation.html", title="orthopedic")


@app.route("/Gynecologist")
def gyn():
    return render_template("gynecologist_recommendation.html")


@app.route("/ENT")
def ent():
    return render_template("ENT_recommendation.html")


@app.route("/Diabetes", methods=["POST"])
def diabetes():
    return render_template("diabetologist_recommendation.html")


@app.route("/Dermatologist")
def dermatologist():
    return render_template("dermatologist_recommendation.html")


@app.route("/Pediatrician")
def pediatrician():
    return render_template("pediatrician_recommendation.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
