import os
import time
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from app import db
from app.models.clubs import Club
from app.models.users import User
from app.models.courts import Court
from app.models.reservations import Reservation
from app.enums import CourtType, WallType, SurfaceType, StatusGame
from datetime import datetime, timedelta

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
  clubs = Club.query.filter(Club.owner_id == user_id).order_by(Club.club_name.desc()).all()
  
  if not clubs:
    return jsonify([]), 200
  
  result = []
  for club in clubs:
    result.append({
      "id": club.id,
      "club_name": club.club_name,
      "address": club.address,
      "open_hour": club.open_hour.strftime("%H:%M"),
      "close_hour": club.close_hour.strftime("%H:%M"),
      "game_duration": club.game_duration,
      "municipality": club.municipality,
      "photo": club.photo,
      "active": club.active
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
    result.append({
      "id": court.id,
      "number_court": court.number_court,
      "court_type": court.court_type.value,
      "covered": court.covered,
      "wall": court.wall.value,
      "surface": court.surface.value,
      "active": court.active,
    })

  return jsonify(result), 200

@owner_bp.route('/crear_club', methods=['POST'])
def create_club():
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()

  # Comprobar el rol del usuario
  claims = get_jwt()
  if claims.get("rol") != "owner":
    return jsonify({"error": "No autorizado"}), 403
  
  data = request.form
  photo = request.files.get("photo")
  
  required_fields = ["nombre", "direccion", "horaApertura", "horaCierre", "duracion", "municipio", "activo"]
  if not data or not all(field in data for field in required_fields) or not photo:
    return jsonify({"error": "Faltan campos obligatorios"}), 400
  
  club_name = Club.query.filter(Club.club_name == data["nombre"]).first()
  if club_name:
    return jsonify({"error": "Ya existe un club con este nombre"}), 409
  
  try:
    # miramos en que carpeta se va a guardar la foto del club
    folder = "images/clubs"
    extension = photo.filename.split('.')[-1]
    filename = f"{data['nombre']}_{int(time.time())}.{extension}"
    save_path = os.path.join('app', 'static', folder)
      
    if not os.path.exists(save_path):
      os.makedirs(save_path)

    file_path = os.path.join(save_path, filename)
    photo.save(file_path)
    db_path = f"{folder}/{filename}"
    
    owner_id = int(get_jwt_identity())
    open_hour = datetime.strptime(data["horaApertura"], "%H:%M").time()
    close_hour = datetime.strptime(data["horaCierre"], "%H:%M").time()
    
    new_club = Club(
      owner_id = owner_id,
      club_name = data["nombre"],
      address = data["direccion"],
      open_hour = open_hour,
      close_hour = close_hour,
      game_duration = int(data["duracion"]),
      municipality = data["municipio"],
      photo = db_path
      )
  
    db.session.add(new_club)
    db.session.commit()
    
    return jsonify({"message": "Club creado correctamente"}), 201
  except Exception as ex:
    db.session.rollback()
    return jsonify({"error": str(ex)}), 500

@owner_bp.route('/club/<int:id>', methods=['GET'])
def get_club(id):
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()

  # Comprobar el rol del usuario
  claims = get_jwt()
  if claims.get("rol") != "owner":
    return jsonify({"error": "No autorizado"}), 403
  
  club = Club.query.get(id)
  if not club:
    return jsonify({"error": "No existe el club"}), 404
  
  return jsonify({
    "club_name": club.club_name,
    "address": club.address,
    "open_hour": club.open_hour.strftime("%H:%M"),
    "close_hour": club.close_hour.strftime("%H:%M"),
    "game_duration": club.game_duration,
    "municipality": club.municipality,
    "photo": club.photo,
    "active": club.active,
  }), 200

@owner_bp.route('/editar_club/<int:id>', methods=['PUT'])
def update_club(id):
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()

  # Comprobar el rol del usuario
  claims = get_jwt()
  if claims.get("rol") != "owner":
    return jsonify({"error": "No autorizado"}), 403
  
  club = Club.query.get(id)
  if not club:
    return jsonify({"error": "No existe el club"}), 404
  
  user_id = int(get_jwt_identity())
  if club.owner_id != user_id:
    return jsonify({"error": "No eres el propietario del club"}), 409
  
  data = request.form
  photo = request.files.get("photo")
  
  # comprovamos que no existe un club con el mismo nombre
  if data.get("nombre"):
    existing_club = Club.query.filter(Club.club_name == data.get("nombre")).first()
    if existing_club and existing_club.id != club.id:
      return jsonify({"error": "El club ya existe"}), 409

  if data.get("horaApertura"):
    club.open_hour = datetime.strptime(data.get("horaApertura"), "%H:%M").time()

  if data.get("horaCierre"):
    club.close_hour = datetime.strptime(data.get("horaCierre"), "%H:%M").time()

  if data.get("duracion"):
    club.game_duration = int(data.get("duracion"))

  if data.get("activo") is not None:
    club.active = data.get("activo") == "true"

  club.club_name = data.get("nombre", club.club_name)
  club.address = data.get("direccion", club.address)
  club.municipality = data.get("municipio", club.municipality)
  
  if photo and photo.filename:
    folder = "images/clubs"
    extension = photo.filename.split('.')[-1]
    
    club_name = data.get("nombre", club.club_name)
    filename = f"{club_name}_{int(time.time())}.{extension}"
    
    save_path = os.path.join('app', 'static', folder)
    
    if not os.path.exists(save_path):
      os.makedirs(save_path)

    file_path = os.path.join(save_path, filename)
    photo.save(file_path)
    
    club.photo = f"{folder}/{filename}"
    
  db.session.commit()

  return jsonify({"message": "Club actualizado"}), 200

@owner_bp.route('/club/<int:id>/crear_pista', methods=['POST'])
def create_court(id):
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()
  
  # Comprobar el rol del usuario
  claims = get_jwt()
  if claims.get("rol") != "owner":
    return jsonify({"error": "No autorizado"}), 403
  
  club = Club.query.get(id)
  if not club:
    return jsonify({"error": "No existe el club"}), 404
  
  if club.active == False:
    return jsonify({"error": "El club no está activo"}), 409
  
  user_id = int(get_jwt_identity())
  if club.owner_id != user_id:
    return jsonify({"error": "No eres el propietario del club"}), 403
  
  data = request.form
  
  required_fields = ["numero", "tipo", "cubierta", "pared", "superficie", "activa"]
  if not data or not all(field in data for field in required_fields):
    return jsonify({"error": "Faltan campos obligatorios"}), 400
  
  existing_court = Court.query.filter(Court.club_id == club.id, Court.number_court == data["numero"]).first()
  if existing_court:
    return jsonify({"error": "El club ya tiene una pista con el mismo número"}), 409
    
  try:    
    new_court = Court(
      club_id = club.id,
      number_court = data["numero"],
      court_type = CourtType(data["tipo"]),
      covered = data["cubierta"] == "true",
      wall = WallType(data["pared"]),
      surface = SurfaceType(data["superficie"]),
      active = data["activa"] == "true",
      )
    
    db.session.add(new_court)
    db.session.commit()
    
    return jsonify({"message": "Pista creada correctamente"}), 201
  except Exception as ex:
    db.session.rollback()
    return jsonify({"error": str(ex)}), 500

@owner_bp.route('/club/<int:club_id>/pista/<int:court_id>', methods=['GET'])
def get_court(club_id, court_id):
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()
  
  # Comprobar el rol del usuario
  claims = get_jwt()
  if claims.get("rol") != "owner":
    return jsonify({"error": "No autorizado"}), 403
  
  club = Club.query.get(club_id)
  if not club:
    return jsonify({"error": "No existe el club"}), 404
  
  user_id = int(get_jwt_identity())
  if club.owner_id != user_id:
    return jsonify({"error": "No eres el propietario del club"}), 403
  
  court = Court.query.get(court_id)
  if not court:
    return jsonify({"error": "No existe la pista"}), 404
  
  existing_court = Court.query.filter(Court.club_id == club.id, Court.id == court.id).first()
  if not existing_court:
    return jsonify({"error": "El club no tiene esta pista creada"}), 409
  
  return jsonify({
    "number_court": court.number_court,
    "court_type": court.court_type,
    "covered": court.covered,
    "wall": court.wall,
    "surface": court.surface,
    "active": court.active,
  }), 200

@owner_bp.route('/club/<int:club_id>/editar_pista/<int:court_id>', methods=['PUT'])
def update_court(club_id, court_id):
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()

  # Comprobar el rol del usuario
  claims = get_jwt()
  if claims.get("rol") != "owner":
    return jsonify({"error": "No autorizado"}), 403
  
  club = Club.query.get(club_id)
  if not club:
    return jsonify({"error": "No existe el club"}), 404
  
  user_id = int(get_jwt_identity())
  if club.owner_id != user_id:
    return jsonify({"error": "No eres el propietario del club"}), 403
  
  court = Court.query.get(court_id)
  if not court:
    return jsonify({"error": "No existe la pista"}), 404
  
  if court.club_id != club.id:
    return jsonify({"error": "El club no tiene esta pista creada"}), 409
  
  data = request.form
  
  # comprovamos que no existe una pista con el mismo número
  if data.get("numero"):
    existing = Court.query.filter(Court.club_id == club_id, Court.number_court == data.get("numero")).first()
    if existing and existing.id != court.id:
      return jsonify({"error": "El club ya tiene este número de pista"}), 409
    
  if data.get("activa") is not None:
    court.active = data.get("activa") == "true"
    
  court.number_court = data.get("numero", court.number_court)
  if data.get("tipo"):
    court.court_type = CourtType(data["tipo"])
    
  if data.get("cubierta"):
    court.covered = data["cubierta"] == "true"
      
  if data.get("pared"):
    court.wall = WallType(data["pared"])
    
  if data.get("superficie"):
    court.surface = SurfaceType(data["superficie"])
  
  db.session.commit()
  
  return jsonify({"message": "Pista actualizada"}), 200

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