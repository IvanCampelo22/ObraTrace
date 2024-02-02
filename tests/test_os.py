import requests
import unittest 
from unittest.mock import patch, Mock
import json

API_BASE_URL = 'http://0.0.0.0:8080/'

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

def make_get_request(url):
    response = requests.get(url)
    return response.status_code, response.json()

def make_post_request(url ,json_data):
    response = requests.post(url, json=json_data)
    return response.status_code, response.json()

def make_put_request(url, json_data):
    response = requests.put(url, json_data)
    return response.status_code, response.json()

def make_delete_request(url):
    response = requests.delete(url)
    return response.status_code, response.json()

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
        
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        os_status, os_data = make_get_request(API_BASE_URL + 'os/list-os')
        self.assertEqual(os_data, response_dict)
        self.assertEqual(os_status, 200)

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
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        os_status, os_data = make_get_request(API_BASE_URL + 'os/get-one-os/1')
        self.assertEqual(os_data, response_dict)
        self.assertEqual(os_status, 200)

    @patch('requests.post')
    def test_post_os_data(self, mock_post):
        mock_response = Mock()
        message_response = {"message":"Ordem de serviço para manutenção criada com sucesso"}
        json_data = json.dumps(data)
        mock_response.status_code, mock_response.json.return_value = 200, message_response
        mock_post.return_value = mock_response
        user_status, user_data = make_post_request(API_BASE_URL + 'os/register-os', json_data)
        self.assertEqual(user_data, message_response)
        self.assertEqual(user_status, 200)
    
    @patch('requests.put')
    def test_put_os_data(self, mock_put):
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
        mock_response.status_code, mock_response.json.return_value = 200, response
        mock_put.return_value = mock_response
        os_status, os_data = make_put_request(API_BASE_URL + 'os/update-os/1', json_data)
        self.assertEqual(os_data, response)
        self.assertEqual(os_status, 200)

    @patch('requests.delete')
    def test_delete_os_data(self, mock_delete):
        mock_response = Mock()
        response = {"message": "Ordem de Serviço deletada com sucesso"}
        mock_response.status_code, mock_response.json.return_value = 200, response
        mock_delete.return_value = mock_response
        os_status, os_data = make_delete_request(API_BASE_URL + 'os/delete-os/1')
        self.assertEqual(os_data, response)
        self.assertEqual(os_status, os_status)

if __name__ == '__main__':
    unittest.main()
