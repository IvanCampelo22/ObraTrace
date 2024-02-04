from tests.utils import make_get_request, make_post_request, make_put_request, make_delete_request
import unittest 
from unittest.mock import patch, Mock
import json

API_BASE_URL = 'http://0.0.0.0:8080/'

response_get = {
                "id": 1,
                "client_adress_id": 1,
                "created_at": "2024-02-02T08:47:20.394683",
                "employee_id": 1,
                "client_id": 1,
                "updated_at": "2024-02-02T08:47:20.394628",
                "is_done": True,
                "os_construction": [
                {
                    "id": 1,
                    "construction_id": 1,
                    "image": None,
                    "end_date": "2024-02-02T03:00:00",
                    "sale": "string",
                    "signature_client": "string",
                    "created_at": "2024-02-02T10:08:22.585335",
                    "employee_id": 1,
                    "client_id": 1,
                    "checklist": "string",
                    "scheduling": "2024-02-02T03:00:00",
                    "info": "string",
                    "signature_emplooye": "string",
                    "update_at": "2024-02-02T10:08:22.585314",
                    "is_active": True
                }
                ],
                "client_adress": {
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
                },
                "client": {
                "id": 1,
                "email": "test",
                "updated_at": "2024-02-02T08:42:08.496007",
                "is_active": True,
                "username": "ivan",
                "password": "$2b$12$HpA5UjsWJweVZ86HVaYDLuIMgWB.4azfAGiMHkLhEkoKs1mEcHcia",
                "created_at": "2024-02-02T08:42:08.496102"
                },
                "employee": {
                "username": "john12",
                "email": "string",
                "work_type": "Comercial",
                "created_at": "2024-01-19T15:31:08.044841",
                "id": 1,
                "password": "$2b$12$HoPiMRBt/WnrkQ/iWQt7hOpJ3UCCSzNoqQejxXxpRAySo0NFDZ2Zi",
                "updated_at": "2024-01-19T15:31:08.044813",
                "is_active": True
                }
            }

data = {
    "is_done": False,
    "employee_id": 1,
    "client_id": 1,
    "client_adress_id": 1
    }

data_put = {
  "is_done": False,
  "employee_id": None,
  "client_id": None,
  "client_adress_id": None
}

class TestConstructionData(unittest.TestCase):

    @patch('requests.get')
    def test_get_constructions_data(self, mock_get):
        mock_response = Mock()
        response_dict = response_get
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        os_status, os_data = make_get_request(API_BASE_URL + 'constructions/list-construction')
        self.assertEqual(os_data, response_dict)
        self.assertEqual(os_status, 200)

    @patch('requests.get')
    def test_get_one_constructions_data(self, mock_get):
        mock_response = Mock()
        response_dict = response_get
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        os_status, os_data = make_get_request(API_BASE_URL + 'constructions/get-one-construction')
        self.assertEqual(os_data, response_dict)
        self.assertEqual(os_status, 200)

    @patch('requests.post')
    def test_post_construction_data(self, mock_post):
        mock_response = Mock()
        message_response = {"message":"Obra registrada com sucesso"}
        json_data = json.dumps(data)
        mock_response.status_code, mock_response.json.return_value = 200, message_response
        mock_post.return_value = mock_response
        user_status, user_data = make_post_request(API_BASE_URL + 'constructions/register-construction', json_data)
        self.assertEqual(user_data, message_response)
        self.assertEqual(user_status, 200)

    @patch('requests.put')
    def test_put_construction_data(self, mock_put):
        mock_response = Mock()
        response = {
            "id": 1,
            "client_adress_id": 1,
            "created_at": "2024-02-02T08:47:20.394683",
            "employee_id": 1,
            "client_id": 1,
            "updated_at": "2024-02-02T08:47:20.394628",
            "is_done": False
            }
        json_data = json.dumps(data_put)
        mock_response.status_code, mock_response.json.return_value = 200, response
        mock_put.return_value = mock_response
        os_status, os_data = make_put_request(API_BASE_URL + 'constructions/update-construction/1', json_data)
        self.assertEqual(os_data, response)
        self.assertEqual(os_status, 200)

    @patch('requests.delete')
    def test_delete_construction_data(self, mock_delete):
        mock_response = Mock()
        response = {"message": "Obra deletada com sucesso"}
        mock_response.status_code, mock_response.json.return_value = 200, response
        mock_delete.return_value = mock_response
        os_status, os_data = make_delete_request(API_BASE_URL + 'constructions/delete-construction/1')
        self.assertEqual(os_data, response)
        self.assertEqual(os_status, os_status)