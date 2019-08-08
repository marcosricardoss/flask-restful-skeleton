"""It contains TokenRepository class."""

from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token

from app.exceptions import TokenNotFound

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

      return self.session.query(Token).filter_by(user_identity=user_identity).all()

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

      self.session.add(token)
      self.session.commit()

      return token


   def change_token_revoking(self, token_id:int, username:str, value:bool) -> None:
      """Changes the revoking status of the given token. Raises a 
      TokenNotFound error if the token does not exist in the database.

      Parameters:
         token_id (str): Token's id.
         username (str): User's username.
         value (bool): value to apply on the token.
      """

      try:
         token = self.session.query(Token).filter_by(id=token_id, user_identity=username).one()
         token.revoked = value
         self.session.commit()
      except NoResultFound:
         raise TokenNotFound("Could not find the token {}".format(token_id))

   
   def revoke_all_tokens(self, username:str) -> None:
      """Revoke all tokens of the given user.

      Parameters:
         username (str): User's username.
      """

      self.session.query(Token).filter_by(user_identity=username).update({Token.revoked:True})
      self.session.commit()


   def is_token_revoked(self, decoded_token:str) -> bool:
      """Checks if the given token is revoked or not. Because we are adding all the
      tokens that we create into this database, if the token is not present
      in the database we are going to consider it revoked, as we don't know where
      it was created.

      Parameters:
         encoded_token (str): The encoded JWT token.      

      Returns:
        A boolean indicating the revoking status.
      """

      jti = decoded_token['jti']
      try:
         token = self.session.query(Token).filter_by(jti=jti).one()
         return token.revoked
      except NoResultFound:
         return True


   def is_invalid(self, token: Token) -> list:
      """Checks if a given model object is valid.

      Parameters:
         user (User): The User model object.
         editing (bool): Indicates whether the validation is for an editing.

      Returns:
         list: A list containing the fields errors.
      """

      invalid = list()       

      return invalid
