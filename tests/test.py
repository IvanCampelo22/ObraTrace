import requests
import unittest 
from unittest.mock import patch, Mock
import json

data = {
        "employee_id": 1,
        "client_id": 1,
        "client_adress_id": 1,
        "os_type": "Instalação",
        "checklist": "string",
        "scheduling": "2024-02-02T11:49:42.653Z",
        "end_date": "2024-02-02T11:49:42.653Z",
        "info": "string",
        "solution": "string",
        "sale": "string",
        "signature_emplooye": "string",
        "signature_client": "string"
    }

def get_os_data():
    response = requests.get('http://0.0.0.0:8080/os/list-os')
    return response.json()

def get_one_os_data(os_id):
    response = requests.get(f'http://0.0.0.0:8080/os/get-one-os/{os_id}')
    return response.json()

def post_os_data():
    json_data = json.dumps(data)
    response = requests.post('http://0.0.0.0:8080/os/register-os', json=json_data)
    return response.json()

def put_os_data(os_id):
    json_data = json.dumps(data)
    response = requests.put(f'http://0.0.0.0:8080/os/update-os/{os_id}', json=json_data)
    return response.json()

def delete_os_data(os_id):
    response = requests.delete(f'http://0.0.0.0:8080/os/delete-os/{os_id}')
    return response.json()

class TesteOsData(unittest.TestCase):

    @patch('requests.get')
    def test_get_os_data(self, mock_get):
        mock_response = Mock()
        response_dict = {
            "employee_id": 1,
            "client_id": 1,
            "client_adress_id": 1,
            "os_type": "Instalação",
            "checklist": "string",
            "scheduling": "2024-02-02T11:49:42.653Z",
            "end_date": "2024-02-02T11:49:42.653Z",
            "info": "string",
            "solution": "string",
            "sale": "string",
            "signature_emplooye": "string",
            "signature_client": "string"
            }
        
        mock_response.json.return_value = response_dict
        mock_get.return_value = mock_response
        user_data = get_os_data()
        mock_get.assert_called_with('http://0.0.0.0:8080/os/list-os')
        self.assertEqual(user_data, response_dict)

    @patch('requests.get')
    def test_get_one_os_data(self, mock_get):
        mock_response = Mock()
        response_dict = {
            "employee_id": 1,
            "client_id": 1,
            "client_adress_id": 1,
            "os_type": "Instalação",
            "checklist": "string",
            "scheduling": "2024-02-02T11:49:42.653Z",
            "end_date": "2024-02-02T11:49:42.653Z",
            "info": "string",
            "solution": "string",
            "sale": "string",
            "signature_emplooye": "string",
            "signature_client": "string"
            }
        
        mock_response.json.return_value = response_dict
        mock_get.return_value = mock_response
        user_data = get_one_os_data(1)
        mock_get.assert_called_with('http://0.0.0.0:8080/os/get-one-os/1')
        self.assertEqual(user_data, response_dict)

    @patch('requests.post')
    def test_post_os_data(self, mock_post):
        mock_response = Mock()
        message_response = {"message":"Ordem de serviço para manutenção criada com sucesso"}
        json_data = json.dumps(data)
        mock_response.json.return_value = message_response
        mock_post.return_value = mock_response
        user_data = post_os_data()
        mock_post.assert_called_with('http://0.0.0.0:8080/os/register-os', json=json_data)
        self.assertEqual(user_data, message_response)
    
    @patch('requests.put')
    def test_put_os_data(self, mock_post):
        mock_response = Mock()
        response = {
            "employee_id": 1,
            "client_id": 1,
            "client_adress_id": 1,
            "os_type": "Instalação",
            "checklist": "string",
            "scheduling": "2024-02-02T11:49:42.653Z",
            "end_date": "2024-02-02T11:49:42.653Z",
            "info": "string",
            "solution": "string",
            "sale": "string",
            "signature_emplooye": "string",
            "signature_client": "string"
            }
        json_data = json.dumps(data)
        mock_response.json.return_value = response
        mock_post.return_value = mock_response
        user_data = put_os_data(1)
        mock_post.assert_called_with('http://0.0.0.0:8080/os/update-os/1', json=json_data)
        self.assertEqual(user_data, response)

    @patch('requests.delete')
    def test_delete_os_data(self, mock_post):
        mock_response = Mock()
        response = {"message": "Ordem de Serviço deletada com sucesso"}
        mock_response.json.return_value = response
        mock_post.return_value = mock_response
        user_data = delete_os_data(1)
        mock_post.assert_called_with('http://0.0.0.0:8080/os/delete-os/1')
        self.assertEqual(user_data, response)

if __name__ == '__main__':
    unittest.main()
