# import jwt


# def test_login_given_valid_input_then_returns_data_with_status_code_200(client, monkeypatch):
#     response = client.post('/login', json={
#         'email': 'test@test.com',
#         'password': 'password'
#     })

#     decoded_jwt = jwt.decode(response.headers['set-cookie'], 'secret', algorithms=['HS256'])
#     assert decoded_jwt == {'user_id': 'user_id'}
#     assert response.status_code == 200
#     assert response.get_json() == {
#         'message': 'Login request was successful.'
#     }


# def test_login_on_exception_from_service_layer_returns_status_code_500(client_raises_exception):
#     response = client_raises_exception.post('/login', json={
#         'email': 'user_id@test.com',
#         'password': 'password'
#     })
#     assert response.status_code == 500
#     assert response.get_json() == {'error': {'code': 500, 'message': 'Internal server error'}}


# def test_login_given_invalid_email_returns_400(client):
#     response = client.post('/login', json={
#         'email': 'invalid',
#         'password': 'password'
#     })
#     assert response.status_code == 400
#     assert response.get_json() == {
#         'error': {
#             'code': 400,
#             'errors': [
#                 {
#                     'field': 'email',
#                     'message': 'Please provide a valid email.'
#                 }
#             ],
#             'message': 'Payload contains missing or invalid data.'
#         }
#     }
