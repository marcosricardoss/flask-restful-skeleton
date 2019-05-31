import functools

from flask import Blueprint

bp = Blueprint('index', __name__, url_prefix='')

@bp.route('/', methods=['GET'])
def index():    
    """Show a simple text indicating the server is running."""
    
    return "The server is runing!"
    