
from flask import Flask, render_template, request, redirect, session
import mysql.connector
import joblib

app = Flask(__name__)
app.secret_key = "smart_energy_key"

model = joblib.load("energy_model.pkl")


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pravallika@2580",
        database="smart_energy"
    )


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )

        db.commit()
        cursor.close()
        db.close()

        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (email, password)
    )

    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user:
        session["user"] = user[1]
        return redirect("/dashboard")
    else:
        return "Invalid Email or Password"


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return render_template("dashboard.html", name=session["user"])


@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    if "user" not in session:
        return redirect("/")

    result = None

    if request.method == "POST":
        temperature = float(request.form["temperature"])
        occupants = int(request.form["occupants"])
        appliances = int(request.form["appliances"])
        hour = int(request.form["hour"])
        weekend = int(request.form["weekend"])

        result = model.predict([[
            temperature, occupants, appliances, hour, weekend
        ]])[0]

    return render_template("prediction.html", result=result)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
