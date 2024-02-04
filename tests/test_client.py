from tests.utils import make_get_request, make_post_request, make_put_request, make_delete_request
import unittest 
from unittest.mock import patch, Mock
import json

API_BASE_URL = 'http://0.0.0.0:8080/'

data_register = {
  "username": "john23",
  "email": "john@gmail.com",
  "password": "12345678",
  "is_active": True
}

data_login = {
  "email": "john12",
  "password": "12345678"
}

data_put = {
  "username": "teste",
  "email": "teste@gmail.com"
}

data_get = [{
                "id": 1,
                "email": "teste@gmail.com",
                "updated_at": "2024-02-02T08:42:08.496007",
                "is_active": True,
                "username": "teste",
                "password": "$2b$12$HpA5UjsWJweVZ86HVaYDLuIMgWB.4azfAGiMHkLhEkoKs1mEcHcia",
                "created_at": "2024-02-02T08:42:08.496102",
                "client_adress": [
                {
                    "id": 1,
                    "adress": "teste",
                    "cep": "string",
                    "state": "pe",
                    "reference_point": "string",
                    "updated_at": "2024-02-02T08:42:08.511976",
                    "client_id": 1,
                    "employee_id": 1,
                    "number": "string",
                    "city": "string",
                    "name_building": "string",
                    "complement": "string",
                    "created_at": "2024-02-02T08:42:08.511994"
                }
                ]
            },
            {
                "id": 2,
                "email": "teste@gmail.com",
                "updated_at": "2024-02-03T21:22:20.875703",
                "is_active": True,
                "username": "teste23",
                "password": "$2b$12$j80kSObJbqhbNb7IjI86xuZ2BU0RYqWwCG.RepiMrhF..LfJRt6E2",
                "created_at": "2024-02-03T21:22:20.875794",
                "client_adress": []
            }]


data_change_password = {
  "email": "teste@gmail.com",
  "old_password": "12345678",
  "new_password": "87654321"
}


class TestClientData(unittest.TestCase):
    @patch('requests.post')
    def test_post_client_register_data(self, mock_post):
        mock_response = Mock()
        message_response = 1
        json_data = json.dumps(data_register)
        mock_response.status_code, mock_response.json.return_value = 200, message_response
        mock_post.return_value = mock_response
        client_status, client_data = make_post_request(API_BASE_URL + 'client/register', json_data)
        self.assertEqual(client_data, message_response)
        self.assertEqual(client_status, 200)

    @patch('requests.post')
    def test_post_client_login_data(self, mock_post):
        mock_response = Mock()
        message_response = {
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDcwMDU3OTMsInN1YiI6IjEifQ.v8u2J0eh5e27P8IkFNbHmHeKPV0tYlvlCgYxDItYlKw",
                            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDc2MDg3OTMsInN1YiI6IjEifQ.RA6cyq3mJV7j9U3B7EqthXgimBEAt5sEADNJviNKey0"
                            }
        json_data = json.dumps(data_login)
        mock_response.status_code, mock_response.json.return_value = 200, message_response
        mock_post.return_value = mock_response
        client_status, client_data = make_post_request(API_BASE_URL + 'client/login', json_data)
        self.assertEqual(client_data, message_response)
        self.assertEqual(client_status, 200)

    @patch('requests.get')
    def test_get_client_data(self, mock_get):
        mock_response = Mock()
        response_dict = data_get
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        client_status, client_data = make_get_request(API_BASE_URL + 'client/getusers')
        self.assertEqual(client_data, response_dict)
        self.assertEqual(client_status, 200)

    @patch('requests.get')
    def test_get_one_client_data(self, mock_get):
        mock_response = Mock()
        response_dict = data_get
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        client_status, client_data = make_get_request(API_BASE_URL + 'client/get-one-client/1')
        self.assertEqual(client_data, response_dict)
        self.assertEqual(client_status, 200)

    @patch('requests.put')
    def test_put_client_data(self, mock_put):
        mock_response = Mock()
        response = 1
        json_data = json.dumps(data_put)
        mock_response.status_code, mock_response.json.return_value = 200, response
        mock_put.return_value = mock_response
        client_status, client_data = make_put_request(API_BASE_URL + '/client/update-client/1', json_data)
        self.assertEqual(client_data, response)
        self.assertEqual(client_status, 200)

    @patch('requests.post')
    def test_post_change_password_data(self, mock_post):
        mock_response = Mock()
        message_response = {"message": "Senha alterada com sucesso"}
        json_data = json.dumps(data_change_password)
        mock_response.status_code, mock_response.json.return_value = 200, message_response
        mock_post.return_value = mock_response
        client_status, client_data = make_post_request(API_BASE_URL + 'client/change-password', json_data)
        self.assertEqual(client_data, message_response)
        self.assertEqual(client_status, 200)

    @patch('requests.post')
    def test_post_logout_data(self, mock_post):
        mock_response = Mock()
        message_response = {"message": "Logout realizado com sucesso"}
        json_data = json.dumps(data_change_password)
        mock_response.status_code, mock_response.json.return_value = 200, message_response
        mock_post.return_value = mock_response
        client_status, client_data = make_post_request(API_BASE_URL + 'client/logout', json_data)
        self.assertEqual(client_data, message_response)
        self.assertEqual(client_status, 200)

    @patch('requests.get')
    def test_get_is_activate_client_data(self, mock_get):
        mock_response = Mock()
        response_dict = {
            "username": "John",
            "email": "john@1973@gmail.com",
            "created_at": "2024-01-19T15:31:08.044841",
            "id": 1,
            "password": "$2b$12$Fh9zUfXf1QesaVm/e4VEku39hMDk3mJYOuJscncT2w/QF1aaRVVj.",
            "updated_at": "2024-01-19T15:31:08.044813",
            "is_active": True
            }
                    
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        client_status, client_data = make_get_request(API_BASE_URL + 'client/get-clients?is_activate=true')
        self.assertEqual(client_data, response_dict)
        self.assertEqual(client_status, 200)

    @patch('requests.get')
    def test_get_is_deactivate_client_data(self, mock_get):
        mock_response = Mock()
        response_dict = {
            "username": "John",
            "email": "john@1973@gmail.com",
            "created_at": "2024-01-19T15:31:08.044841",
            "id": 1,
            "password": "$2b$12$Fh9zUfXf1QesaVm/e4VEku39hMDk3mJYOuJscncT2w/QF1aaRVVj.",
            "updated_at": "2024-01-19T15:31:08.044813",
            "is_active": False
            }
                    
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        client_status, client_data = make_get_request(API_BASE_URL + 'client/get-clients?is_activate=false')
        self.assertEqual(client_data, response_dict)
        self.assertEqual(client_status, 200)

    @patch('requests.delete')
    def test_deactivate_client_data(self, mock_delete):
        mock_response = Mock()
        response = {"message": "cliente desativado"}
        mock_response.status_code, mock_response.json.return_value = 200, response
        mock_delete.return_value = mock_response
        client_status, client_data = make_delete_request(API_BASE_URL + '/client/deactivate-client/1')
        self.assertEqual(client_data, response)
        self.assertEqual(client_status, client_status)