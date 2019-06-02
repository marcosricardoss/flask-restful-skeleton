import os

from dotenv import load_dotenv

class Default(object):        
    SQLALCHEMY_TRACK_MODIFICATIONS = False    


class Production(Default):
    """Class containing the settings of the production environment . 
    
    It load some values from the environment to be used in the internal Flask config.
    """

    SECRET_KEY = b'\xacP=\x12\xa6\xa2\x19`\xbcu{\x0b\xe4&H\x8d'    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    

class Development(Default):
    """Class containing the settings of the development environment. 
    
    It uses the dotenv library to load some values from the .env file to environment. 
    After that, theses values are load from the environment to be use in the internal Flask config.
    """
    
    load_dotenv() # load .env file
    SECRET_KEY = 'dev'            
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')    