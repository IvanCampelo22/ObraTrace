from tests.utils import make_get_request, make_post_request, make_put_request, make_delete_request
import unittest 
from unittest.mock import patch, Mock
import json

API_BASE_URL = 'http://0.0.0.0:8080/'

data_register = {
    "username": "John Doe",
    "email": "johndoe@gmail.com",
    "password": "12345678",
    "work_type": "Comercial"
  }

data_login = {
  "email": "string",
  "password": "string"
}

data_put = {
  "username": "john12",
  "email": "john@gmail.com",
  "work_type": "Comercial"
}

data_change_password = {
  "email": "john@gmail.com",
  "old_password": "12345678",
  "new_password": "87654321"
}

class TestEmployeesData(unittest.TestCase):
    @patch('requests.post')
    def test_post_employee_register_data(self, mock_post):
        mock_response = Mock()
        message_response = {"message":"funcionário criado com sucesso"}
        json_data = json.dumps(data_register)
        mock_response.status_code, mock_response.json.return_value = 200, message_response
        mock_post.return_value = mock_response
        employee_status, employee_data = make_post_request(API_BASE_URL + 'employee/register', json_data)
        self.assertEqual(employee_data, message_response)
        self.assertEqual(employee_status, 200)

    @patch('requests.post')
    def test_post_employee_login_data(self, mock_post):
        mock_response = Mock()
        message_response = {
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDcwMDU3OTMsInN1YiI6IjEifQ.v8u2J0eh5e27P8IkFNbHmHeKPV0tYlvlCgYxDItYlKw",
                            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDc2MDg3OTMsInN1YiI6IjEifQ.RA6cyq3mJV7j9U3B7EqthXgimBEAt5sEADNJviNKey0"
                            }
        json_data = json.dumps(data_login)
        mock_response.status_code, mock_response.json.return_value = 200, message_response
        mock_post.return_value = mock_response
        employee_status, employee_data = make_post_request(API_BASE_URL + 'employee/login', json_data)
        self.assertEqual(employee_data, message_response)
        self.assertEqual(employee_status, 200)

    @patch('requests.get')
    def test_get_employees_data(self, mock_get):
        mock_response = Mock()
        response_dict = {
            "username": "John",
            "email": "john@1973@gmail.com",
            "work_type": "Comercial",
            "created_at": "2024-01-19T15:31:08.044841",
            "id": 1,
            "password": "$2b$12$Fh9zUfXf1QesaVm/e4VEku39hMDk3mJYOuJscncT2w/QF1aaRVVj.",
            "updated_at": "2024-01-19T15:31:08.044813",
            "is_active": True
            }
        
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        employee_status, employee_data = make_get_request(API_BASE_URL + 'employee/getusers')
        self.assertEqual(employee_data, response_dict)
        self.assertEqual(employee_status, 200)

    @patch('requests.get')
    def test_get_one_employee_data(self, mock_get):
        mock_response = Mock()
        response_dict = {
            "username": "John",
            "email": "john@1973@gmail.com",
            "work_type": "Comercial",
            "created_at": "2024-01-19T15:31:08.044841",
            "id": 1,
            "password": "$2b$12$Fh9zUfXf1QesaVm/e4VEku39hMDk3mJYOuJscncT2w/QF1aaRVVj.",
            "updated_at": "2024-01-19T15:31:08.044813",
            "is_active": True
            }
                    
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        employee_status, employee_data = make_get_request(API_BASE_URL + 'employee/get-one-employee/1')
        self.assertEqual(employee_data, response_dict)
        self.assertEqual(employee_status, 200)

    @patch('requests.put')
    def test_put_employee_data(self, mock_put):
        mock_response = Mock()
        response = {
            "username": "john12",
            "email": "john@gmail.com",
            "work_type": "Comercial",
            "created_at": "2024-01-19T15:31:08.044841",
            "id": 1,
            "password": "$2b$12$Fh9zUfXf1QesaVm/e4VEku39hMDk3mJYOuJscncT2w/QF1aaRVVj.",
            "updated_at": "2024-01-19T15:31:08.044813",
            "is_active": True
        }
        json_data = json.dumps(data_put)
        mock_response.status_code, mock_response.json.return_value = 200, response
        mock_put.return_value = mock_response
        employee_status, employee_data = make_put_request(API_BASE_URL + 'employee/update-employee/1', json_data)
        self.assertEqual(employee_data, response)
        self.assertEqual(employee_status, 200)

    @patch('requests.post')
    def test_post_change_password_data(self, mock_post):
        mock_response = Mock()
        message_response = {"message": "Senha alterada com sucesso"}
        json_data = json.dumps(data_change_password)
        mock_response.status_code, mock_response.json.return_value = 200, message_response
        mock_post.return_value = mock_response
        employee_status, employee_data = make_post_request(API_BASE_URL + 'employee/change-password', json_data)
        self.assertEqual(employee_data, message_response)
        self.assertEqual(employee_status, 200)

    @patch('requests.post')
    def test_post_logout_data(self, mock_post):
        mock_response = Mock()
        message_response = {"message": "Logout realizado com sucesso"}
        json_data = json.dumps(data_change_password)
        mock_response.status_code, mock_response.json.return_value = 200, message_response
        mock_post.return_value = mock_response
        employee_status, employee_data = make_post_request(API_BASE_URL + 'employee/logout', json_data)
        self.assertEqual(employee_data, message_response)
        self.assertEqual(employee_status, 200)

    @patch('requests.get')
    def test_get_is_activate_employee_data(self, mock_get):
        mock_response = Mock()
        response_dict = {
            "username": "John",
            "email": "john@1973@gmail.com",
            "work_type": "Comercial",
            "created_at": "2024-01-19T15:31:08.044841",
            "id": 1,
            "password": "$2b$12$Fh9zUfXf1QesaVm/e4VEku39hMDk3mJYOuJscncT2w/QF1aaRVVj.",
            "updated_at": "2024-01-19T15:31:08.044813",
            "is_active": True
            }
                    
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        employee_status, employee_data = make_get_request(API_BASE_URL + 'employee/get-employees?is_activate=true')
        self.assertEqual(employee_data, response_dict)
        self.assertEqual(employee_status, 200)

    @patch('requests.get')
    def test_get_is_deactivate_employee_data(self, mock_get):
        mock_response = Mock()
        response_dict = {
            "username": "John",
            "email": "john@1973@gmail.com",
            "work_type": "Comercial",
            "created_at": "2024-01-19T15:31:08.044841",
            "id": 1,
            "password": "$2b$12$Fh9zUfXf1QesaVm/e4VEku39hMDk3mJYOuJscncT2w/QF1aaRVVj.",
            "updated_at": "2024-01-19T15:31:08.044813",
            "is_active": False
            }
                    
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        employee_status, employee_data = make_get_request(API_BASE_URL + 'employee/get-employees?is_activate=false')
        self.assertEqual(employee_data, response_dict)
        self.assertEqual(employee_status, 200)

    @patch('requests.delete')
    def test_deactivate_employee_data(self, mock_delete):
        mock_response = Mock()
        response = {"message": "funcionário desativado"}
        mock_response.status_code, mock_response.json.return_value = 200, response
        mock_delete.return_value = mock_response
        os_status, os_data = make_delete_request(API_BASE_URL + '/employee/deactivate-employee/1')
        self.assertEqual(os_data, response)
        self.assertEqual(os_status, os_status)