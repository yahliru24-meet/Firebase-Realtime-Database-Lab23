from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyCtTNHBjczxTp8LYMG3LCIN6mhysqomptM",
  "authDomain": "proj1-d4176.firebaseapp.com",
  "projectId": "proj1-d4176",
  "storageBucket": "proj1-d4176.appspot.com",
  "messagingSenderId": "484315964747",
  "appId": "1:484315964747:web:72531f52840ac1bde834ce",
  "measurementId": "G-WZJ5YGS1PT",
  "databaseURL": "https://proj1-d4176-default-rtdb.europe-west1.firebasedatabase.app/",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form["username"]
        full_name = request.form["full_name"]
        bio = request.form["bio"]
        try:
            UID = login_session['user']['localId']
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"name": full_name, "username" : username, "bio": bio,}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)