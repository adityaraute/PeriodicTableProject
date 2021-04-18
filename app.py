from flask import Flask, render_template,request, session, redirect, url_for
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
firedb = firebase.database()

@app.route("/")
def home():
    try:
        return render_template("index.html", user = session['username'])
    except:
        return render_template("index.html")


@app.route("/elements")
def elements():
    try:
        return render_template("elements.html", user = session['username'])
    except:
        return render_template("elements.html")


@app.route("/login",methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        loginEmail = request.form['loginEmail']
        loginPassword = request.form['loginPassword']
        try:
            auth.sign_in_with_email_and_password(loginEmail, loginPassword)
            session['username'] = loginEmail
            return render_template('quizpage.html', user = session['username'])
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
            return render_template('quizpage.html', user = session['username'])
        except Exception as e:
            print(e)
            print("Got error while sign up")
            return render_template('login.html',invalidLogin=True)
    else:
        return render_template("login.html",invalidLogin=False)

@app.route("/quiz",methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        my_var = request.form['quizscore']
        print(my_var)
        username = session['username'].split('.')[0]
        try:
            firedb.child("users").child(username).push(data={'score': my_var})
        except:
            firedb.child("users").set({username: {'score': my_var}})

        try:
            return render_template("quizpage.html", user = session['username'])
        except:
            return render_template('quizpage.html')
    else:
        try:
            return render_template("quizpage.html", user = session['username'])
        except:
            return render_template('quizpage.html')


@app.route('/logout')
def logout():
    try:
       # remove the username from the session if it is there
        session.pop('username', None)
    except:
        pass
    return redirect(url_for('home'))

@app.route('/score')
def score():
        username = session['username'].split('.')[0]

        data = firedb.child("users").child(username).get()
        arr = []
        for i in data.each():
            arr.append(i.val()['score'])
        return render_template('score.html', user = session['username'], data = sorted(arr)[::-1])
    # except Exception as e:
        # print(e)
        return render_template('score.html')

if __name__ == "__main__":
  app.debug = True
  app.secret_key = 'random'
  app.run()