"""This module contains funções to format the output of API."""


from flask import jsonify


def create_response(status_code: int, status: str = None, message: str = None, data: list = None):
    """Create a Response.

    Parameters:
        status_code (int): The request status code
        status (str): A status text
        message (str): A message text
        data (list): A data list come back from the API

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    output = dict()

    if status:
        output["status"] = status

    if message:
        output["message"] = message

    if data:
        output["data"] = data

    response = jsonify(output)
    response.status_code = status_code

    return response
