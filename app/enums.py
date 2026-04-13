import enum

# Posibles valores de rol de usuario
class UserRole(enum.Enum):
  player = "player"
  owner = "owner"

# Posibles valores de tipo de pista
class CourtType(enum.Enum):
  individual = "individual"
  double = "double"

# Posibles valores de tipo de muro
class WallType(enum.Enum):
  glass = "glass"
  concrete = "concrete"

# Posibles valores de tipo de superfície
class SurfaceType(enum.Enum):
  grass = "grass"
  concrete = "concrete"

# Posibles valores de tipo de estado de un partido
class StatusGame(enum.Enum):
  open = "open"
  complete = "complete"
  canceled = "canceled"
  pending_result = "pending_result"
  finalized = "finalized"

# Posibles valores de equipo ganador
class WinnerTeam(enum.Enum):
  a = "a"
  b = "b"

# Posibles valores de equipo
class Team(enum.Enum):
  a = "a"
  b = "b"

# Posibles valores de razón de cambio de puntos
class ReasonType(enum.Enum):
  win = "win"
  lose = "lose"