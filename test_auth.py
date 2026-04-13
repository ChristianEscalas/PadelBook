from app import app
from app.routes.player import unfollow
# Para poder usar la BD de Flask
with app.app_context():    
  # Probar login correcto
  unfollow()