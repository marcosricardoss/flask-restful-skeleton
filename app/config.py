import os

class Default(object):    
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(Default):
    SECRET_KEY = b'\xacP=\x12\xa6\xa2\x19`\xbcu{\x0b\xe4&H\x8d'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')    


class Development(Default):
    DEBUG = True    
    SECRET_KEY = 'dev'        
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format("postgres", 
                                                                            "123", 
                                                                            "127.0.0.1", 
                                                                            "15432", 
                                                                            "olist_dev")