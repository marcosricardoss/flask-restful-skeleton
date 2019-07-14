"""This module registers the error handler on the application."""


from flask import make_response, jsonify


def register_handler(app):
    """Registers the error handler is a function to common error HTTP codes

    Parameters:    
        app (flask.app.Flask): The application instance.
    """

    @app.errorhandler(400)
    def bad_request(error):
        """Deal with HTTP BadRequest exceptions.

        Parameters:
            error (BadRequest): A werkzeug.exceptions.BadRequest exception object.

        Returns:
            A flask response object.
        """

        return make_response(jsonify({
            'status': 'fail',
            'message': 'bad request'
        }), 400)

    @app.errorhandler(404)
    def not_found(error):
        """ Deal with HTTP NotFound exceptions.

        Parameters:
            error (NotFound): A werkzeug.exceptions.NotFound exception object.

        Returns:
            A flask response object.
        """

        return make_response(jsonify({
            'status': 'error',
            'message': 'not Found'
        }), 404)