from app import db
from app.models.users import User
from app.utils.security import new_password_hash, check_password
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import create_access_token
import time, os

# Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registrar', methods=['POST'])
def register():
  # obtenemos datos del formulario
  data = request.form
  photo = request.files.get("photo")
  
  required_fields = ['username', 'email', 'password', 'mobile', 'age', 'firstname', 'rol', 'category']
  
  # comprovamos que vengan los datos necesarios
  if not data or not all(field in data for field in required_fields) or not photo:
    return jsonify({"error": "Faltan datos obligatorios"}), 400 
  
  # comprovamos que no existe un usuario con el mismo email o username
  user_email = User.query.filter_by(email  = data['email']).first()
  user_username = User.query.filter_by(username = data['username']).first()
  if user_email or user_username:
    return jsonify({"error": "usuario ya registrado"}), 409
  
  try:
    # miramos en que carpeta se va a guardar la foto del usuario
    folder = "images/users"
    extension = photo.filename.split('.')[-1]
    filename = f"{data['username']}_{int(time.time())}.{extension}"
    save_path = os.path.join('app', 'static', folder)
      
    if not os.path.exists(save_path):
      os.makedirs(save_path)

    file_path = os.path.join(save_path, filename)
    photo.save(file_path)
    db_path = f"{folder}/{filename}"
    
    # si no existe creamos nuevo usuario y lo añadimos a la base de datos
    new_user = User(
      username = data['username'],
      email = data['email'],
      password_hash = new_password_hash(data['password']),
      mobile = data['mobile'],
      address = data.get('address'),
      age = data['age'],
      firstname = data['firstname'],
      lastname = data.get('lastname'),
      category = data['category'],
      rol = data['rol'],
      photo = db_path
    )
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "usuario registrado", "user_id": new_user.id}), 201
  except Exception as ex:
    db.session.rollback()
    return jsonify({"error": str(ex)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
  # obtenemos datos del formulario
  data = request.get_json()
  
  # comprovamos que vengan los datos necesarios
  if not data or 'username' not in data or 'password' not in data:
    return jsonify({"message": "Faltan datos obligatorios"}), 400
  
  # comprovamos que existe un usuario con el mismo email
  user = User.query.filter_by(username = data['username']).first()
  if user is None or not check_password(data['password'], user.password_hash):
    return jsonify({"error": "Datos incorrectos"}), 401
  
  access_token = create_access_token(identity=str(user.id), additional_claims={"rol": user.rol.value})
  response = make_response(jsonify({"access_token": access_token}), 200)
  response.set_cookie("rol", user.rol.value)
  return response
