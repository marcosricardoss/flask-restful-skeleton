"""It contains tests for the account retrieving endpoint."""

from tests.util import create_user, create_tokens


def test_get_account_with_an_existent_user_returning_200_status_code(client, auth):
    """
    GIVEN a Flask application
    WHEN the '/account' URL is requested (GET)
    THEN check the response is valid
    """

    response = client.get('/account',
                          headers=auth['access_token'])
    # asserts
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['data']['username'] == 'test'


def test_get_account_with_an_user_already_excluded_returning_404_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/account' URL is requested (GET) with inexistent user
    THEN check the response HTTP 404 response
    """

    user = create_user(session)
    tokens = create_tokens(user.username)
    # delete the user
    session.delete(user)
    session.commit()
    # request
    response = client.get('/account',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    # asserts
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'not Found'
