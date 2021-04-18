from flask import Flask, render_template
import pyrebase

config = {
    'apiKey': "AIzaSyBb6jM5x75-MDw3149Y0ZnRRCWotFyhEwI",
    'authDomain': "periodictable-f0687.firebaseapp.com",
    'databaseURL': "periodictable-f0687.firebaseapp.com",
    'projectId': "periodictable-f0687",
    'storageBucket': "periodictable-f0687.appspot.com",
    'messagingSenderId': "285365556906",
    'appId': "1:285365556906:web:c030eea0feef18f4cee2d3"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
email = 'hello@byebye.in'
password = 'password'
user = auth.create_user_with_email_and_password(email, password)

auth.get_account_info(user['idToken'])
print(user)

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