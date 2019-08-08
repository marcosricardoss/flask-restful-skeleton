"""It contains tests for the /account exclusion endpoint."""


from tests.util import create_user, create_tokens


def test_delete_with_all_data_passed_returning_200_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/account' URL is requested (DELETE)
    THEN check the response is valid
    """

    user = create_user(session)
    tokens = create_tokens(user.username)
    endpoint = '/account'
    # assert user was deleted
    response = client.delete(endpoint,
                             headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 201

    from app.model import Token
    tokens = session.query(Token).filter_by(
                                            user_identity=user.username, 
                                            revoked=False).all()
    assert len(tokens) == 0


def test_delete_with_inexistent_user_id_returning_404_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/account' URL is requested (DELETE) with inexistent user
    THEN check the response HTTP 404 response
    """

    user = create_user(session)
    tokens = create_tokens(user.username)
    # delete the user
    session.delete(user)
    session.commit()
    # request
    endpoint = '/account'
    response = client.delete(endpoint,
                             headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'not Found'
