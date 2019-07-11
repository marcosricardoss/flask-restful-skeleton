"""It contains tests for user exclusion endpoints."""


from ..util import create_user, get_unique_id


def test_user_delete_with_all_data_passed_returning_200_status_code(client, session, auth):
    user = create_user(session)
    endpoint = '/users/{}'.format(user.id)
    # assert user was deleted
    response = client.delete(endpoint, headers=auth['access_token'])
    assert response.status_code == 201
    # assert the user no longer exist
    response = client.get(endpoint, headers=auth['access_token'])
    assert response.status_code == 404


def test_user_delete_with_inexistent_user_id_returning_404_status_code(client, auth):
    endpoint = '/users/{}'.format(get_unique_id())
    response = client.delete(endpoint, headers=auth['access_token'])
    assert response.status_code == 404
