from flask import Blueprint,render_template, request, flash,redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method== 'POST':
        email= request.form.get('email')
        password= request.form.get('password')

        user= User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('login successful!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.dashboard'))
            else:
                flash('incorrect password',category='error')
        else:
            flash('user does not exist!', category='error')

    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if request.method== 'POST':
        email= request.form.get('email')
        first_name= request.form.get('firstName')
        password1= request.form.get('password1')
        password2=request.form.get('password2')
    
        user= User.query.filter_by(email=email).first()
        if user:
            flash('user already exists', category='error')

        if len(email) <4:
            flash('email must be greater than four characters', category='error')
        elif len(first_name) <2:
            flash('first name must be greater than 2 characters', category='error')
        elif len (password1)<7:
            flash ('password must be greater than 7 characters', category='error')
        elif password1 != password2:
            flash('first password must match second password', category='error')
        else:
            new_user= User(email=email, first_name=first_name,password= generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('account creation Success!', category='success')
            return render_template('dashboard.html')

    return render_template("signup.html", user=current_user)



@auth.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("dashboard.html", user=current_user)
    