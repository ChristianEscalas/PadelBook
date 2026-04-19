from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from app import db
from app.models.clubs import Club
from app.models.users import User
from app.models.courts import Court
from app.models.reservations import Reservation
from app.enums import CourtType, WallType, SurfaceType, StatusGame
from datetime import time, datetime, timedelta

owner_bp = Blueprint('owner', __name__)
@owner_bp.route('/mis_clubes', methods=['GET'])
def get_clubs():
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()

  # Comprobar el rol del usuario
  claims = get_jwt()
  if claims.get("rol") != "owner":
    return jsonify({"error": "No autorizado"}), 403
  
  # id del usuario
  user_id = get_jwt_identity()
  
  # clubes del usuario
  clubs = Club.query.filter(Club.owner_id == user_id, Club.active != False).order_by(Club.club_name.desc()).all()
  
  if not clubs:
    return jsonify([]), 200
  
  result = []
  for club in clubs:
    result.append({
      "id": club.id,
      "club_name": club.club_name,
      "address": club.address,
      "photo": club.photo,
      "open_hour": club.open_hour.strftime("%H:%M"),
      "close_hour": club.close_hour.strftime("%H:%M"),
      "game_duration": club.game_duration,
    })
    
  return jsonify(result), 200

@owner_bp.route('/pistas/club/<int:id>', methods=['GET'])
def get_courts(id):
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()

  # Comprobar el rol del usuario
  claims = get_jwt()
  if claims.get("rol") != "owner":
    return jsonify({"error": "No autorizado"}), 403

  club = Club.query.get(id)
  if club.active == False:
    return jsonify({"error": "El club está eliminado"}), 404
  
  courts = Court.query.filter(Court.club_id == club.id)
  if not courts:
    return jsonify([]), 200
    
  result = []
  for court in courts:
    courts.append({
      "id": court.id,
      "number_court": court.number_court,
      "court_type": court.court_type,
      "covered": court.covered,
      "wall": court.wall,
      "surface": court.surface,
      "active": court.active,
    })

  return jsonify(result), 200

def create_club():
  new_club = Club(owner_id = 3, club_name = "PruebaCrearClub2", address = "Calle prueba, 2", open_hour = time(10, 0, 0), close_hour = time(21, 0, 0), game_duration = 90, municipality = "Marratxí", photo = "app/static/images/clubs/clubPadel.jpg")
  existing_club = Club.query.filter_by(club_name = new_club.club_name).first()
  user = User.query.filter_by(id = new_club.owner_id).first()
  
  if user is None:
    print("El usuario no existe")
    return
  
  if user.rol.value != "owner":
    print("El usuario no es propietario")
    return
  
  if existing_club is None:
    db.session.add(new_club)
    db.session.commit()
    print(f"Club {new_club.club_name} creado correctamente")
  else:
    print("Ya existe un club con ese nombre.")

def delete_club(club_id = 1, owner_id = 3):
  existing_club = Club.query.filter_by(id = club_id).first()
  
  if existing_club is None:
    print("No existe el club")
    return
  
  if existing_club.owner_id != owner_id:
    print("No eres el propietario del club")
    return
  
  if not existing_club.active:
    print("El club ya está inactivo")
    return
  
  existing_club.active = False
  db.session.commit()
  print("El club marcado como inactivo")

def create_court():
  new_court = Court(club_id = 2, number_court = 2, court_type = CourtType.individual, covered = True, wall = WallType.concrete, surface = SurfaceType.concrete)
  existing_club = Club.query.filter_by(id = new_court.club_id).first()
  owner_id = 3
  
  if existing_club is None:
    print("No existe el club")
    return
  
  if existing_club.owner_id != owner_id:
    print("No eres el propietario del club")
    return
  
  if not existing_club.active:
    print("El club no está activo")
    return
  
  existing_court = Court.query.filter_by(club_id = existing_club.id, number_court = new_court.number_court).first()
  if existing_court is None:
    db.session.add(new_court)
    db.session.commit()
    print(f"Pista número {new_court.number_court} creada correctamente")
  else:
    print(f"El club {existing_club.club_name} ya tiene la pista número {new_court.number_court}, no se puede añadir")

def delete_court(club_id = 2, owner_id = 3, number_court = 2):
  existing_club = Club.query.filter_by(id = club_id).first()
  
  if existing_club is None:
    print("No existe el club")
    return
  
  if existing_club.owner_id != owner_id:
    print("No eres el propietario del club")
    return
  
  if not existing_club.active:
    print("El club no está activo")
    return
  
  existing_court = Court.query.filter_by(club_id = club_id, number_court = number_court).first()
  if existing_court is None:
    print(f"El club no tiene la pista número {number_court}")
    return
  
  if not existing_court.active:
    print("Esta pista ya está inactiva")
    return
  
  existing_court.active = False
  db.session.commit()
  print(f"Pista número {number_court} del club {existing_club.club_name} marcada como inactiva")

def cancel_reservation(club_id = 2, owner_id = 3, court_id = 1, reservation_id = 1):
  existing_club = Club.query.filter_by(id = club_id).first()
  
  if existing_club is None:
    print("No existe el club")
    return
  
  if existing_club.owner_id != owner_id:
    print("No eres el propietario del club")
    return
  
  if not existing_club.active:
    print("El club no está activo")
    return
  
  existing_court = Court.query.filter_by(id = court_id, club_id = club_id).first()
  if existing_court is None:
    print("El club no tiene esta pista")
    return
  
  if not existing_court.active:
    print("No es posible cancelar la reserva de una pista inactiva")
    return
  
  existing_reservation = Reservation.query.filter_by(id = reservation_id, court_id = existing_court.id).first()
  if existing_reservation is None:
    print("No existe la reserva")
    return
  
  reservation_status = existing_reservation.status_game.value
  if reservation_status in ["pending_result", "finalized"]:
    print("No se puede cancelar un partido finalizado o en curso")
    return
    
  if reservation_status == "canceled":
    print("La reserva ya está cancelada")
    return

  if datetime.now() + timedelta(hours=3) > existing_reservation.start_date:
    print("Solo se puede cancelar con al menos 3 horas de antelación")
    return

  existing_reservation.status_game = StatusGame.canceled
  existing_reservation.closed_at = datetime.now()
  db.session.commit()
  print(f"Reserva para el {existing_reservation.start_date} cancelada correctamente")