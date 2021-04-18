from flask import Flask, render_template,request
import pyrebase
app = Flask(__name__)

firebaseConfig = {
    "apiKey": "AIzaSyBb6jM5x75-MDw3149Y0ZnRRCWotFyhEwI",
    "authDomain": "periodictable-f0687.firebaseapp.com",
    "projectId": "periodictable-f0687",
    "databaseURL": "https://periodictable-f0687-default-rtdb.firebaseio.com/",
    "storageBucket": "periodictable-f0687.appspot.com",
    "messagingSenderId": "285365556906",
    "appId": "1:285365556906:web:c030eea0feef18f4cee2d3"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/elements")
def elements():
    return render_template("elements.html")

@app.route("/login",methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        loginEmail = request.form['loginEmail']
        loginPassword = request.form['loginPassword']

        print(loginEmail,loginEmail)
        try:
            auth.sign_in_with_email_and_password(loginEmail, loginPassword)
            return render_template('elements.html')
        except:
            return render_template('login.html', invalidLogin=True)
    else:
        return render_template("login.html",invalidLogin=False)

@app.route("/signup",methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        signUpEmail = request.form['signUpEmail']
        signUpPassword = request.form['signUpPassword']
        signUpPasswordConfirmed = request.form['signUpPasswordConfirmed']
        if signUpPassword!=signUpPasswordConfirmed:
            return render_template('login.html',invalidLogin=True)
        try:
            auth.create_user_with_email_and_password(signUpEmail, signUpPassword)
            return render_template('elements.html')
        except Exception as e:
            print(e)
            print("Got error while sign up")
            return render_template('login.html',invalidLogin=True)
    else:
        return render_template("login.html",invalidLogin=False)

@app.route("/quiz")
def quiz():
    return render_template("quizpage.html")

if __name__ == "__main__":
  app.debug = True
  app.run()