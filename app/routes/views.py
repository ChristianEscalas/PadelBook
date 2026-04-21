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

@views_bp.route('/ranking')
def ranking_page():
  return render_template('users/ranking.html')

@views_bp.route('/usuario/<int:id>')
def user_profile_page(id):
  return render_template('users/user_profile.html')

@views_bp.route('/seguidores')
def get_followers():
  return render_template('/users/followers.html')

@views_bp.route('/seguidos')
def get_following_page():
  return render_template('/users/followings.html')

@views_bp.route('/reserva/confirmar_resultado/<int:id>')
def confirm_result_view(id):
    return render_template("players/confirm_result.html", reservation_id=id)

@views_bp.route('/mis_clubes')
def my_clubes_page():
    return render_template("owners/my_clubs.html")

@views_bp.route('/pistas/club/<int:id>')
def courts_by_club_page(id):
    return render_template("owners/courts_by_club.html")

@views_bp.route('/crear_club')
def create_club_page():
  return render_template('owners/create_club.html')

@views_bp.route('/editar_club/<int:id>')
def edit_club_page(id):
  return render_template('owners/create_club.html', edit_mode = True)

@views_bp.route('/club/<int:id>/crear_pista')
def create_court_page(id):
  return render_template('owners/create_court.html')

@views_bp.route('/club/<int:club_id>/editar_pista/<int:court_id>')
def edit_court_page(club_id, court_id):
  return render_template('owners/create_court.html', edit_mode = True)

@views_bp.route('/reservas/club/<int:club_id>')
def reservations_club_page(club_id):
  return render_template('owners/reservations_club.html')