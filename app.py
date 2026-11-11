from flask import Flask, render_template, request, redirect, session
import mysql.connector
import joblib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask application
app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

# Load trained ML model
model = joblib.load("energy_model.pkl")


# MySQL database connection
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# Home page
@app.route("/")
def home():
    return render_template("login.html")


# User registration
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


# User login
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


# Dashboard page
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        name=session["user"]
    )


# Energy prediction
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

        prediction_input = [[
            temperature,
            occupants,
            appliances,
            hour,
            weekend
        ]]

        result = model.predict(prediction_input)[0]

    return render_template(
        "prediction.html",
        result=result
    )


# Logout
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# Run application
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )