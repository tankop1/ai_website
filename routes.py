from app import app
from app import db
from forms import Login, Register, ContactUs, MakeAI, PurchaseInfo
from models import User
from ai import recordAudio, generateResponse, speak
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

manager = LoginManager()
manager.init_app(app)
manager.login_view = 'login'

order = []

# Defining of flask_login.user_loader
@manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route for main page
@app.route('/', methods=["GET", "POST"])
def home():
    aiError = False
    youSaid = ''
    if request.method == 'POST':
        print('REQUEST = POST')
        if request.form["mic"] == " ":
            text = recordAudio()
            if text == 1 or text == 2:
                aiError = True
            else:
                youSaid = text
                print("RECORD AUDIO EXECUTED")
                response = generateResponse(text)
                print("GENERATE RESPONSE EXECUTED")
                num = speak(response)
                if num != None:
                    if num == 1:
                        return redirect(url_for('home'))
                    elif num == 2:
                        return redirect(url_for('plans'))
                    elif num == 3:
                        return redirect(url_for('shop'))
                    elif num == 4:
                        return redirect(url_for('login'))
                    elif num == 5:
                        return redirect(url_for('logout'))
                print('IT WORKED!!!')
            return redirect(url_for('home'))
    return render_template('home.html', youSaid=youSaid, aiError=aiError)

@app.route('/register', methods=["GET", "POST"])
def register():
    register = Register()
    if register.validate_on_submit():
        new_user = User(first_name=register.first_name.data, last_name=register.last_name.data, username=register.username.data, password=register.password.data, email=register.email.data)
        db.session.add(new_user)
        try:
            db.session.commit()
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            print('ERROR ADDING USER. PLEASE TRY AGAIN.')
    return render_template('register.html', register=register)

# Login route that logs in user
@app.route('/login', methods=["GET", "POST"])
def login():
    login = Login()
    if login.validate_on_submit():
        user = User.query.filter_by(username=login.username.data).first()
        if user:
            if user.password == login.password.data:
                login_user(user)
                return redirect(url_for('home'))
            else:
                print('INVALID')
        else:
            print('INVALID')
    return render_template('login.html', login=login)

# Logout route that logs out user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Routes user to page with commands for samantha
@app.route('/shop', methods=["GET", "POST"])
@login_required
def shop():
    makeai = MakeAI()
    if makeai.validate_on_submit():
        order.append(makeai.wake_word.data)
        order.append(makeai.voice.data)
        order.append(makeai.purchase.data)
        order.append(makeai.tracking.data)
        order.append(makeai.os.data)
        order.append(makeai.user_names.data)
        order.append(makeai.files.data)
        order.append(makeai.files2.data)
        order.append(makeai.sos.data)
        print(order)
        return redirect(url_for('checkout'))
    else:
        pass
    return render_template('shop.html', makeai=makeai)

@app.route('/checkout', methods=["GET", "POST"])
@login_required
def checkout():
    purchase = PurchaseInfo()
    if purchase.validate_on_submit():
        return redirect(url_for('info'))
    else:
        pass
    return render_template('checkout.html', purchase=purchase, order=order)

@app.route('/plans')
def plans():
    return render_template('plans.html')

@app.route('/success')
@login_required
def info():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('info.html', user=user)

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

@app.route('/secret')
def secret():
    return render_template('secret.html')