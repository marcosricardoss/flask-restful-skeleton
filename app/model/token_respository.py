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

   def get_user_tokens(self, user_identity:str) -> list:
      """Returns all of the tokens, revoked and unrevoked, 
      that are stored for the given user.

      Parameters:
         identity_claim (str): The key of the identity claim in the decoded token dictionary.

      Returns:
         list: A token list of a user.
      """

      return db_session.query(Token).filter_by(user_identity=user_identity).all()

   def save(self, encoded_token:str, identity_claim:str=None) -> None:
      """Adds a new token to the database. It is not revoked when it is added.

      Parameters:
         encoded_token (str): The encoded JWT token.
         identity_claim (str): The key of the identity claim in the decoded token dictionary.
      """

      decoded_token = decode_token(encoded_token)
      jti = decoded_token['jti']
      token_type = decoded_token['type']
      user_identity = decoded_token[identity_claim]
      expires = datetime.fromtimestamp(decoded_token['exp'])
      revoked = False

      token = Token(jti=jti, token_type=token_type, user_identity=user_identity,
                    expires=expires, revoked=revoked)

      db_session.add(token)
      db_session.commit()
        

   def is_invalid(self, token: Token, editing: bool = False) -> list:
      """Checks if a given model object is valid.

      Parameters:
         user (User): The User model object.
         editing (bool): Indicates whether the validation is for an editing.

      Returns:
         list: A list containing the fields errors.
      """

      invalid = list()       

      return invalid
