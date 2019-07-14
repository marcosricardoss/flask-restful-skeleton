"""It contains tests for the account retrieving endpoint."""

from ..util import create_user, create_tokens


def test_get_account_with_an_existent_user_returning_200_status_code(client, auth):
    response = client.get('/account',
                          headers=auth['access_token'])
    # asserts
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['data']['username'] == 'test'


def test_get_account_with_an_user_already_excluded_returning_404_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(session, user.username)
    # delete the user
    session.delete(user)
    session.commit()
    # request
    response = client.get('/account',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    # asserts
    assert response.status_code == 404
    
