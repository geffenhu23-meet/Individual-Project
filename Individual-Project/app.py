from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import json

config = {
  "apiKey": "AIzaSyDqenMEPs1LOCP3mCM1SWy7bJk_LVCVza4",
  "authDomain": "indy2summer.firebaseapp.com",
  "projectId": "indy2summer",
  "storageBucket": "indy2summer.appspot.com",
  "messagingSenderId": "1039378622302",
  "appId": "1:1039378622302:web:82008f73107ad0f806d1cf",
  "measurementId": "G-3S2E3PL15K",
  "databaseURL":"https://indy2summer-default-rtdb.europe-west1.firebasedatabase.app"}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

@app.route('/', methods=['GET', 'POST'])
def signin():
        error = ""
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            try:
                login_session['user'] = auth.sign_in_with_email_and_password(email, password)
                return redirect(url_for('home'))
            except Exception as e:
                # error = "Authentication failed"
                return render_template("signin.html",er = json.loads(e.args[1])['error']['message'])
        else:
            return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']
        try:
           login_session['user'] = auth.create_user_with_email_and_password(email, password)
           user = {"name": full_name, "email": email, "password":password, "username":username, "bio":bio}
           db.child("Users").child(login_session['user']['localId']).set(user)
           return render_template('home.html')
        except Exception as e:
                # error = "Authentication failed"
                return render_template("signup.html",ersu = json.loads(e.args[1])['error']['message'])

    else:
        return render_template("signup.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    user = db.child("user").get().val()
    if request.method == 'POST':
        product = request.form['product']
        picture_link = request.form['picture_link']
        try:
            Product = {"product": product, "picture_link": picture_link}
            db.child("product").push(Product)
            return redirect(url_for("all_products"))
        except:
            error = "Authentication failed"
            return render_template("home.html")
            
    else:
        return render_template('home.html')


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_products')
def all_products():
    Product = db.child("product").get().val()
    return render_template("all_products.html", Product=Product)

@app.route('/cart')
def cart():
    Product = db.child("product").get().val()
    return render_template("cart.html", Product=Product)


#Code goes above here

if __name__ == '__main__':
    app.run(debug=True, port=9478)