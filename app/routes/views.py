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

@views_bp.route('/confirmar_reserva')
def confirm_reservation():
  return render_template('/players/confirm_reservation.html')

@views_bp.route('/mis_reservas')
def show_reservations():
  return render_template('/players/my_reservations.html')

@views_bp.route('/reserva/<int:id>')
def reservation_detail_page(id):
  return render_template('players/reservation_detail.html')

@views_bp.route('/reserva/cancelar/<int:id>')
def cancel_page(id):
  return render_template('players/cancel_reservation.html')

@views_bp.route('/buscar_partidos')
def search_matches_page():
  return render_template('players/search_matches.html')

@views_bp.route('/unirse_reserva')
def join_reservation_page():
  return render_template('players/join_reservation.html')

@views_bp.route('/perfil')
def profile_page():
  return render_template('users/profile.html')

@views_bp.route('/editar_perfil')
def edit_profile_page():
  return render_template('auth/register.html', edit_mode=True)