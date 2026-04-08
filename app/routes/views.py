from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

@views_bp.route('/login')
def login_page():
    return render_template('auth/login.html')

@views_bp.route('/register')
def register_page():
    return render_template('auth/register.html')

@views_bp.route('/')
def index():
    return render_template('index.html')
