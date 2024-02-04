from tests.utils import make_get_request, make_post_request, make_put_request, make_delete_request
import unittest 
from unittest.mock import patch, Mock
import json

API_BASE_URL = 'http://0.0.0.0:8080/'

data_register = {
  "client_id": 1,
  "employee_id": 1,
  "adress": "teste",
  "number": "02",
  "cep": "23211",
  "city": "cidade",
  "state": "pe",
  "name_building": "nome do prédio",
  "reference_point": "string",
  "complement": "string"
}

data_get =   {
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

data_put = {
  "client_id": 1,
  "employee_id": 1,
  "adress": "rua de teste",
  "number": "02",
  "cep": "1234567-032",
  "city": "teste",
  "state": "pe",
  "name_building": "string",
  "reference_point": "string",
  "complement": "string"
}

class TestClientData(unittest.TestCase):
    @patch('requests.post')
    def test_post_client_adress_data(self, mock_post):
        mock_response = Mock()
        message_response = {"message":"Endereço do cliente registrado com sucesso"}
        json_data = json.dumps(data_register)
        mock_response.status_code, mock_response.json.return_value = 200, message_response
        mock_post.return_value = mock_response
        client_adress_status, client_adress_data = make_post_request(API_BASE_URL + 'client_adress/register-client-adress', json_data)
        self.assertEqual(client_adress_data, message_response)
        self.assertEqual(client_adress_status, 200)

    @patch('requests.get')
    def test_get_client_adress_data(self, mock_get):
        mock_response = Mock()
        response_dict = data_get
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        os_status, os_data = make_get_request(API_BASE_URL + 'client_adress/list-client-adresses')
        self.assertEqual(os_data, response_dict)
        self.assertEqual(os_status, 200)

    @patch('requests.get')
    def test_get_one_client_adress_data(self, mock_get):
        mock_response = Mock()
        response_dict = data_get
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        os_status, os_data = make_get_request(API_BASE_URL + 'client_adress/get-one-client-adress/1')
        self.assertEqual(os_data, response_dict)
        self.assertEqual(os_status, 200)

    @patch('requests.put')
    def test_put_client_adress_data(self, mock_put):
        mock_response = Mock()
        response = {
            "id": 1,
            "adress": "string",
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
        json_data = json.dumps(data_put)
        mock_response.status_code, mock_response.json.return_value = 200, response
        mock_put.return_value = mock_response
        client_status, client_data = make_put_request(API_BASE_URL + 'client_adress/update-client-adress/1', json_data)
        self.assertEqual(client_data, response)
        self.assertEqual(client_status, 200)

    @patch('requests.delete')
    def test_deactivate_client_adress_data(self, mock_delete):
        mock_response = Mock()
        response = {"message": "Endereço deletado com sucesso"}
        mock_response.status_code, mock_response.json.return_value = 200, response
        mock_delete.return_value = mock_response
        client_adress_status, client_adress_data = make_delete_request(API_BASE_URL + 'client_adress/delete-client-adress/1')
        self.assertEqual(client_adress_data, response)
        self.assertEqual(client_adress_status, client_adress_status)