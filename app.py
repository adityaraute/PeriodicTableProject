from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/elements")
def elements():
    return render_template("elements.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/quiz")
def quiz():
    return render_template("quizpage.html")

if __name__ == "__main__":
  app.debug = True
  app.run()