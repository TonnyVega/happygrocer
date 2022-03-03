from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods= ['GET', 'POST'])
def home():
    return render_template('home.html', user=current_user)







@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

