from app import db
from app.models.users import User
from app.enums import UserRole
from app.utils.security import new_password_hash, check_password

def register():
  new_user = User(username = "usuario4", email = "usuario4@gmail.com", password_hash = new_password_hash("usuario4"), mobile = "123456789", age = 20, firstname = "Joan", lastname = "Martínez Riera", rol = UserRole.player, photo = "app/static/images/users/descarga.jpg")
  user_email = User.query.filter_by(email  = new_user.email).first()
  user_username = User.query.filter_by(username = new_user.username).first()
  
  if user_email is None and user_username is None:
    db.session.add(new_user)
    db.session.commit()
    print(f"Usuario {new_user.username} registrado correctamente.")
  elif user_username is not None:
    print(f"Nombre de usuario {new_user.username} ya registrado, prueba otro.")
  elif user_email is not None:
    print(f"Email {new_user.email} ya registrado, prueba otro")
  

def login(email_to_check = "nologuin@gmail.com", password_to_check = "nologuin"):
  user = User.query.filter_by(email = email_to_check).first()
  if user is None or not check_password(password_to_check, user.password_hash):
    print("Email o contraseña incorrectos")
  else:
    print("Bienvenido")
