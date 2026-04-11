from flask import Blueprint, render_template

views_bp = Blueprint('views', __name__)

@views_bp.route('/login')
def login_page():
  return render_template('auth/login.html')

@views_bp.route('/registrar')
def register_page():
  return render_template('auth/register.html')

@views_bp.route('/')
def index():
  return render_template('index.html')

@views_bp.route('/contacto')
def contact_page():
  return render_template('contact.html')

@views_bp.route('/reservar')
def reservation_page():
	return render_template('/players/reservate.html')