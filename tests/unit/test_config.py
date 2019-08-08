"""It contains tests for the config.py classes"""

def test_default_config():
  """
  GIVEN the Default model
  THEN check its attributes
  """

  from app.config import Default
  
  assert Default.DEBUG == False
  assert Default.TESTING == False
  assert Default.JWT_BLACKLIST_ENABLED == True
  assert Default.JWT_BLACKLIST_TOKEN_CHECKS == ['access', 'refresh']
  assert Default.SQLALCHEMY_TRACK_MODIFICATIONS == False


def test_production_config():
  """
  GIVEN the Production model
  THEN check production attributes
  """

  from app.config import Production
  
  assert Production.SECRET_KEY
  assert Production.JWT_SECRET_KEY
  assert hasattr(Production, 'SQLALCHEMY_DATABASE_URI')


def test_Development_config():
  """
  GIVEN the Production model
  THEN check development attributes
  """

  from app.config import Development
  
  assert Development.DEBUG
  assert Development.SECRET_KEY == 'dev'
  assert Development.JWT_SECRET_KEY == 'dev'
  assert hasattr(Development, 'SQLALCHEMY_DATABASE_URI')
 