from sqlalchemy import and_
from app import db
from datetime import datetime, timedelta
from app.models.reservations import Reservation
from app.models.reservationPlayers import ReservationPlayer
from app.models.courts import Court
from app.models.users import User
from app.models.clubs import Club
from app.models.followers import Follower
from app.enums import CourtType, StatusGame, SurfaceType, Team, WallType, WinnerTeam
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt

player_bp = Blueprint('player', __name__)

@player_bp.route('/reservar', methods=['GET'])
def reservate():
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()

  # Comprobar el rol del usuario
  claims = get_jwt()
  if claims.get("rol") != "player":
    return jsonify({"error": "No autorizado"}), 403

  # filtros de búsqueda
  dia = request.args.get('dia')
  hora = request.args.get('hora')
  municipality = request.args.get('municipio')
  duration = request.args.get('duracion')
  court_type = request.args.get('tipo')
  covered = request.args.get('cubierta')
  wall = request.args.get('pared')
  surface = request.args.get('superficie')

  if dia and hora:
    start = datetime.strptime(f"{dia} {hora}", "%Y-%m-%d %H:%M")
    
    if start < datetime.now():
        return jsonify({"error": "No se puede reservar para una fecha anterior a hoy."}), 400
  else:
    return jsonify({"error": "No has indicado día y hora de reserva."}), 400

  if not duration:
    duration = 60
  else:
    duration = int(duration)
  
  end = start + timedelta(minutes=duration)

  if end.date() != start.date():
    return jsonify({"error": "La reserva no puede superar la medianoche."}), 400
  
  start_time = start.time()
  end_time = end.time()
  
  # query principal
  query = Court.query.join(Club).filter(Court.active == True, Club.active == True)  # noqa: E712

  query = query.filter(Club.open_hour <= start_time, Club.close_hour >= end_time)
  
  # filtros dinámicos
  if municipality:
    query = query.filter(Club.municipality == municipality)

  if court_type:
    query = query.filter(Court.court_type == CourtType(court_type))

  if covered:
    query = query.filter(Court.covered == (covered == "true"))

  if wall:
    query = query.filter(Court.wall == WallType(wall))

  if surface:
    query = query.filter(Court.surface == SurfaceType(surface))

  # quitar pistas ocupadas
  subquery = db.session.query(Reservation.court_id).filter(and_(Reservation.start_date < end, Reservation.end_date > start))

  query = query.filter(~Court.id.in_(subquery))
  query = query.order_by(Club.club_name)
  # ejecutar query
  courts_available = query.all()

  # clubes únicos
  clubs = {}
  for court in courts_available:
    club = court.club
    clubs[club.id] = club

  result = []
  for club in clubs.values():
    result.append({
      "id": club.id,
      "club_name": club.club_name,
      "address": club.address,
      "open_hour": club.open_hour.strftime("%H:%M"),
      "close_hour": club.close_hour.strftime("%H:%M"),
      "game_duration": club.game_duration,
      "photo": club.photo
    })

  return jsonify(result), 200

@player_bp.route('/reservar', methods=['POST'])
def create_reservation():
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()

  # Comprobar el rol del usuario
  claims = get_jwt()
  if claims.get("rol") != "player":
    return jsonify({"error": "No autorizado"}), 403
  
  # datos enviados en el formulario
  data = request.get_json()
  club_id = data.get("club_id")
  day = data.get("dia")
  hour = data.get("hora")
  duration = data.get("duracion")

  court_type = data.get("tipo")
  covered = data.get("cubierta")
  wall = data.get("pared")
  surface = data.get("superficie")
  
  if not club_id or not day or not hour:
    return jsonify({"error": "Faltan datos obligatorios"}), 400
  
  # se mira si el club existe y está activo
  club = Club.query.get(club_id)
  if not club or not club.active:
    return jsonify({"error": "Club no válido"}), 400
  
  # calculo de fecha de inicio y final
  start = datetime.strptime(f"{day} {hour}", "%Y-%m-%d %H:%M")
  if start < datetime.now():
    return jsonify({"error": "No se puede reservar para una fecha anterior a hoy"}), 400
  
  if not duration:
    duration = 60
  else:
    duration = int(duration)
    
  end = start + timedelta(minutes=int(duration))
  
  if end.date() != start.date():
    return jsonify({"error": "La reserva no puede superar la medianoche"}), 400
  
  start_time = start.time()
  end_time = end.time()

  if not (club.open_hour <= start_time and club.close_hour >= end_time):
    return jsonify({"error": "El horario está fuera del horario del club"}), 400
  
  # buscar las pistas activas del club que cumplan con los filtros
  query = Court.query.filter(Court.club_id == club_id, Court.active == True)
  
  if court_type:
    query = query.filter(Court.court_type == CourtType(court_type))

  if covered:
    query = query.filter(Court.covered == (covered == "true"))

  if wall:
    query = query.filter(Court.wall == WallType(wall))

  if surface:
    query = query.filter(Court.surface == SurfaceType(surface))
  
  # escoger solo las disponibles
  subquery = db.session.query(Reservation.court_id).filter(and_(Reservation.start_date < end, Reservation.end_date > start))

  query = query.filter(~Court.id.in_(subquery))
  query = query.order_by(Court.number_court)
  court = query.first()

  if not court:
    return jsonify({"error": "No hay pistas disponibles"}), 400
  
  # se crea la reserva
  reservation = Reservation(court_id=court.id, creator_id=get_jwt_identity(), start_date=start, end_date=end, status_game=StatusGame.open)
  db.session.add(reservation)
  db.session.commit()
  
  # se crea registro de la reserva
  creator = ReservationPlayer(user_id=get_jwt_identity(), reservation_id=reservation.id, team=Team.a, is_creator=True)
  db.session.add(creator)
  db.session.commit()
  
  return jsonify({"message": "Reserva creada correctamente"}), 201

@player_bp.route('/reservar/preview', methods=['GET'])
def preview_reservation():
  verify_jwt_in_request()

  club_id = request.args.get("club_id")
  day = request.args.get("dia")
  hour = request.args.get("hora")
  duration = request.args.get("duracion")

  court_type = request.args.get("tipo")
  covered = request.args.get("cubierta")
  wall = request.args.get("pared")
  surface = request.args.get("superficie")

  if not club_id or not day or not hour:
    return jsonify({"error": "Faltan datos"}), 400

  if not duration:
    duration = 60
  else:
    duration = int(duration)

  start = datetime.strptime(f"{day} {hour}", "%Y-%m-%d %H:%M")
  end = start + timedelta(minutes=duration)

  club = Club.query.get(club_id)

  query = Court.query.filter(Court.club_id == club_id, Court.active == True)

    # filtros
  if court_type:
    query = query.filter(Court.court_type == CourtType(court_type))

  if covered:
    query = query.filter(Court.covered == (covered == "true"))

  if wall:
    query = query.filter(Court.wall == WallType(wall))

  if surface:
      query = query.filter(Court.surface == SurfaceType(surface))

  # disponibilidad
  subquery = db.session.query(Reservation.court_id).filter(and_(Reservation.start_date < end, Reservation.end_date > start))

  query = query.filter(~Court.id.in_(subquery)).order_by(Court.number_court)
  court = query.first()

  if not court:
    return jsonify({"error": "No hay pistas disponibles"}), 400

  return jsonify({
    "club": club.club_name,
    "address": club.address,
    "court_number": court.number_court,
    "start": start.strftime("%Y-%m-%d %H:%M"),
    "end": end.strftime("%Y-%m-%d %H:%M"),
    "duration": duration
  }), 200
    
def join_reservation(user_id = 7, reservation_id = 3, selected_team = Team.b):
  user = User.query.filter_by(id = user_id).first()
  
  if user is None:
    print("No existe el usuario")
    return
  
  if user.rol.value != "player":
    print("El usuario no es jugador")
    return
  
  reservation = Reservation.query.filter_by(id = reservation_id).first()
  if reservation is None:
    print("La reserva no existe")
    return
  
  already_in = ReservationPlayer.query.filter_by(reservation_id=reservation_id, user_id=user_id).first()
  if already_in is not None:
    print("Ya estás apuntado a este partido")
    return
  
  number_players_reservation = len(reservation.players)
  if number_players_reservation >= 4:
    print("No es posible unirse al partido, no hay huecos libres")
    return
  
  team_count = ReservationPlayer.query.filter_by(reservation_id=reservation_id, team=selected_team).count()
  if team_count >= 2:
    print(f"El equipo {selected_team.name} ya está completo")
    return
  
  new__player = ReservationPlayer(user_id = user_id, reservation_id = reservation_id, team = selected_team)
  db.session.add(new__player)
  db.session.commit()
  print(f"Te has unido al equipo {selected_team.name}")

def cancel_reservation(user_id = 1, reservation_id = 1):
  user = User.query.filter_by(id = user_id).first()
  
  if user is None:
    print("No existe el usuario")
    return
  
  if user.rol.value != "player":
    print("El usuario no es jugador")
    return
  
  reservation = Reservation.query.filter_by(id = reservation_id).first()
  if reservation is None:
    print("La reserva no existe")
    return
  
  if user_id != reservation.creator_id:
    print("No puedes cancelar la reserva. no eres el creador")
    return
  
  reservation_status = reservation.status_game.value
  if reservation_status in ["pending_result", "finalized"]:
    print("No se puede cancelar un partido finalizado o en curso")
    return
    
  if reservation_status == "canceled":
    print("La reserva ya está cancelada")
    return

  if datetime.now() + timedelta(hours=3) > reservation.start_date:
    print("Solo se puede cancelar con al menos 3 horas de antelación")
    return

  reservation.status_game = StatusGame.canceled
  reservation.closed_at = datetime.now()
  db.session.commit()
  print(f"Reserva para el {reservation.start_date} cancelada correctamente")

def leave_reservation(user_id = 7, reservation_id = 3):
  user = User.query.filter_by(id = user_id).first()
  
  if user is None :
    print("No existe el usuario")
    return

  if user.rol.value != "player":
    print("El usuario no es jugador")
    return
  
  player_in_reservation = ReservationPlayer.query.filter_by(user_id = user_id, reservation_id = reservation_id).first()
  if player_in_reservation is None:
    print("No estás apuntado a este partido")
    return

  if player_in_reservation.is_creator:
    print("Eres el creador. Para salirte debes cancelar la reserva")
    return

  reservation = Reservation.query.filter_by(id = reservation_id).first()
  if reservation is None:
    print("La reserva no existe")
    return
  
  if reservation.status_game.value in ["pending_result", "finalized"]:
    print("No te puedes salir de un partido finalizado o en curso")
    return
  
  if reservation.status_game.value == "canceled":
    print("No te puedes salir de una reserva cancelada")
    return
  
  if datetime.now() + timedelta(hours = 3) > reservation.start_date:
    print("No puedes salirte a falta de menos de 3 horas")
    return

  db.session.delete(player_in_reservation)
  db.session.commit()
  print(f"Te has salido del partido. Ahora hay un sitio libre en el equipo {player_in_reservation.team.name}")

def set_result(reservation_id = 3, user_id = 1, sets_a=[6, 4, 6], sets_b=[2, 6, 3]):
  reservation = Reservation.query.get(reservation_id)
  if reservation is None:
    print("La reserva no existe")
    return

  if reservation.creator_id != user_id:
    print("No tienes permisos para subir el resultado de este partido")
    return

  if reservation.status_game.value in ["canceled", "finalized"]:
    print("No se puede subir resultado de un partido cancelado o finalizado")
    return
  
  for i in range(3):
    if sets_a[i] == sets_b[i] and (sets_a[i] != 0 or sets_b[i] != 0):
      print(f"Error: El Set {i+1} no puede ser un empate ({sets_a[i]}-{sets_b[i]}). Debe haber un ganador.")
      return
  
  result = f"{sets_a[0]}-{sets_b[0]}/{sets_a[1]}-{sets_b[1]}/{sets_a[2]}-{sets_b[2]}"
    
  wins_a = 0
  for i in range(3):
    if sets_a[i] > sets_b[i]:
      wins_a += 1
    
  if wins_a >= 2:
    winner = WinnerTeam.a
  else:
    winner = WinnerTeam.b

  reservation.result = result
  reservation.winner_team = winner
  reservation.status_game = StatusGame.pending_result
  db.session.commit()
  print(f"Resultado {result} guardado. Ganador: Equipo {winner.name}")

def follow(user_id = 1, user_to_follow_id = 1):
  user = User.query.filter_by(id = user_id).first()
  
  if user is None:
    print("No existe el usuario")
    return
  
  if user.id == user_to_follow_id:
    print("No te puedes seguir a ti mismo")
    return
  
  user_to_follow = User.query.filter_by(id = user_to_follow_id).first()
  if user_to_follow is None:
    print("El usuario al que quieres seguir no existe")
    return
  
  existing_following = Follower.query.filter_by(follower_id = user.id, following_id = user_to_follow.id).first()
  if existing_following is not None:
    print("Ya sigues a este usuario")
    return
  
  new_follower = Follower(follower_id = user.id, following_id = user_to_follow.id)
  db.session.add(new_follower)
  db.session.commit()
  print(f"Has empezado a seguir a {user_to_follow.firstname}")

def unfollow(user_id = 1, user_to_unfollow_id = 1):
  user = User.query.filter_by(id = user_id).first()
  
  if user is None:
    print("No existe el usuario")
    return
  
  if user.id == user_to_unfollow_id:
    print("No te puedes dejar de seguir a ti mismo")
    return
  
  user_to_unfollow = User.query.filter_by(id = user_to_unfollow_id).first()
  if user_to_unfollow is None:
    print("El usuario al que quieres seguir no existe")
    return
  
  existing_following = Follower.query.filter_by(follower_id = user.id, following_id = user_to_unfollow.id).first()
  if existing_following is None:
    print("No sigues a este usuario")
    return
  
  db.session.delete(existing_following)
  db.session.commit()
  print(f"Has dejado de seguir a {user_to_unfollow.firstname}")

# carga los municipios            
@player_bp.route('/municipios', methods=['GET'])
def get_municipality():
  municipalities = db.session.query(Club.municipality).distinct().order_by(Club.municipality).all()
  
  result = []
  for municipality in municipalities:
    result.append(municipality[0])

  return jsonify(result), 200

# carga los tipos de pista 
@player_bp.route('/tipo', methods=['GET'])
def get_types():
  types = []
  for court_type in CourtType:
    types.append(court_type.value )
  
  return jsonify(types), 200

@player_bp.route('/cubierta', methods=['GET'])
def get_cover():
    return jsonify(["true", "false"]), 200

# carga los tipos de pared
@player_bp.route('/pared', methods=['GET'])
def get_walls():
  walls = []
  for wall_type in WallType:
    walls.append(wall_type.value)
  
  return jsonify(walls), 200

# carga los tipos de superficie
@player_bp.route('/superficie', methods=['GET'])
def get_surfaces():
  surfaces = []
  for surface in SurfaceType:
    surfaces.append(surface.value)
  
  return jsonify(surfaces), 200