"""It contains tests for the account exclusion endpoint."""


from ..util import create_user, create_tokens


def test_patch_delete_with_all_data_passed_returning_200_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(user.username)
    endpoint = '/account'
    # assert user was deleted
    response = client.delete(endpoint, 
                             headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 201

    from app.model import Token
    tokens = session.query(Token).filter_by(user_identity=user.username, revoked=False).all()
    assert len(tokens) == 0


def test_patch_delete_with_inexistent_user_id_returning_404_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(user.username)
    # delete the user
    session.delete(user)
    session.commit()
    # request
    response = client.patch('/account',
                            headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})

    endpoint = '/account'
    response = client.delete(endpoint, 
                             headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'not Found'
