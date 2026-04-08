from app import db
from datetime import datetime, timedelta
from app.models.reservations import Reservation
from app.models.reservationPlayers import ReservationPlayer
from app.models.courts import Court
from app.models.users import User
from app.models.clubs import Club
from app.models.followers import Follower
from app.enums import StatusGame, Team, WinnerTeam

def create_reservation():
  user_id = 1
  user = User.query.filter_by(id = user_id).first()
  if user.rol.value != "player":
    print("El usuario no es jugador")
    return
  
  club_id = 2
  existing_club = Club.query.filter_by(id = club_id).first()
  if existing_club is None:
    print("No existe el club")
    return
  
  start_date = datetime(2026, 3, 17, 13, 00)
  hour_start_date = start_date.time()
  end_date = start_date + timedelta(minutes= existing_club.game_duration)
  hour_end_date = end_date.time()
  
  if start_date < datetime.now():
    print("No es posible reservar para una fecha anterior a la de hoy")
    return
  
  if hour_start_date < existing_club.open_hour or hour_end_date > existing_club.close_hour:
    print(f"Horario inválido. El club abre de {existing_club.open_hour} a {existing_club.close_hour}")
    return
  
  new_reservation = Reservation(court_id = 1, creator_id = user.id, start_date = start_date, end_date = end_date)
  existing_court = Court.query.filter_by(id = new_reservation.court_id, club_id = club_id).first()
  if existing_court is None:
    print("No existe la pista")
    return
  
  existing_reservations = Reservation.query.filter_by(court_id = existing_court.id).all()
  existing_reservation = None
  for reserva in existing_reservations:
    if new_reservation.start_date < reserva.end_date and new_reservation.end_date > reserva.start_date and reserva.court_id == new_reservation.court_id:
      existing_reservation = reserva
  
  if existing_reservation is None:
    db.session.add(new_reservation)
    db.session.flush()
    print(f"Reserva creada para el {new_reservation.start_date} en la pista {existing_court.number_court} en el club {existing_club.club_name}")
    
    new_reservation_player = ReservationPlayer(user_id = user_id, reservation_id = new_reservation.id, team = Team.a, is_creator = True)
    db.session.add(new_reservation_player)
    db.session.commit()
  else:
    print("Franja horaria no disponible")

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