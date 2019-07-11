"""It contains TokenRepository class."""

from datetime import datetime

from flask_jwt_extended import decode_token

from app.database import db_session
from .models import Token
from .repository import Repository


class TokenRepository(Repository):
   """It Contains specific method related to de Token model."""

   def __init__(self):
      Repository.__init__(self, Token)  