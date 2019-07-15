"""It contains tests for the account patching endpoint."""

from datetime import datetime

from flask import json
from ..util import create_user, create_tokens, get_unique_username


def test_patch_account_with_data_well_formatted_returning_200_status_code(client, session, auth):
    user = create_user(session)
    tokens = create_tokens(user.username)
    endpoint = '/account'
    data = {'password': "x123x"}
    response = client.patch(endpoint,
                            data=json.dumps(data),
                            content_type='application/json',
                            headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert int(response.json['data']['id']) == user.id


def test_patch_account_with_password_length_smaller_than_3_character_returning_400_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(user.username)
    endpoint = '/account'
    data = {'password': "xx"}
    response = client.patch(endpoint,
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {"password": "minimum length of 3 characters"} in response.json['data']   


def test_patch_account_with_an_user_already_excluded_returning_404_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(user.username)
    # delete the user
    session.delete(user)
    session.commit()
    # request
    response = client.patch('/account',
                            content_type='application/json',
                            headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    # asserts
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'not Found'


def test_patch_account_without_data_returning_400_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(user.username)
    endpoint = '/account'
    response = client.patch(endpoint,
                            content_type='application/json',
                            headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_patch_account_with_only_password_passed_returning_200_status_code(client, session, auth):
    user = create_user(session)
    tokens = create_tokens(user.username)
    endpoint = '/account'
    data = {'password': "x123x"}
    response = client.patch(endpoint,
                            data=json.dumps(data),
                            content_type='application/json',
                            headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert int(response.json['data']['id']) == user.id