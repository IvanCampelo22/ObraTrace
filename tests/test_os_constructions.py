from tests.utils import make_get_request, make_post_request, make_put_request, make_delete_request
import unittest 
from unittest.mock import patch, Mock
import json

API_BASE_URL = 'http://0.0.0.0:8080/'

data = {
  "employee_id": 1,
  "client_id": 1,
  "construction_id": 1,
  "checklist": "string",
  "scheduling": "2024-02-03",
  "end_date": "2024-02-03",
  "info": "string",
  "solution": "string",
  "sale": "string",
  "signature_emplooye": "string",
  "signature_client": "string"
}


class TesteOsConstructionsData(unittest.TestCase):

    @patch('requests.get')
    def test_get_os_constructions_data(self, mock_get):
        mock_response = Mock()
        response_dict = {
            "employee_id": 1,
            "client_id": 1,
            "construction_id": 1,
            "checklist": "string",
            "scheduling": "2024-02-03",
            "end_date": "2024-02-03",
            "info": "string",
            "solution": "string",
            "sale": "string",
            "signature_emplooye": "string",
            "signature_client": "string"
            }
        
        mock_response.status_code, mock_response.json.return_value = 200, response_dict
        mock_get.return_value = mock_response
        os_status, os_data = make_get_request(API_BASE_URL + 'os_constructions/list-os-construction')
        self.assertEqual(os_data, response_dict)
        self.assertEqual(os_status, 200)

    @patch('requests.get')
    def test_get_one_os_constructions_data(self, mock_get):
        mock_response = Mock()
        response_dict = {
            "employee_id": 1,
            "client_id": 1,
            "construction_id": 1,
            "checklist": "string",
            "scheduling": "2024-02-03",
            "end_date": "2024-02-03",
            "info": "string",
            "solution": "string",
            "sale": "string",
            "signature_emplooye": "string",
            "signature_client": "string"
            }
                    
        mock_response.json.return_value = response_dict
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        os_status, os_data = make_get_request(API_BASE_URL + 'os_constructions/get-one-os-constructions/1')
        self.assertEqual(os_data, response_dict)
        self.assertEqual(os_status, 200)

    
    @patch('requests.post')
    def test_post_os_construction_data(self, mock_post):
        mock_response = Mock()
        message_response = {"message":"Ordem de serviço para obra criada com sucesso"}
        json_data = json.dumps(data)
        mock_response.status_code, mock_response.json.return_value = 200, message_response
        mock_post.return_value = mock_response
        user_status, user_data = make_post_request(API_BASE_URL + '/os_constructions/register-os-construction', json_data)
        self.assertEqual(user_data, message_response)
        self.assertEqual(user_status, 200)
    
    @patch('requests.put')
    def test_put_os_construction_data(self, mock_put):
        mock_response = Mock()
        response = {
            "employee_id": 1,
            "client_id": 1,
            "construction_id": 1,
            "checklist": "string",
            "scheduling": "2024-02-03",
            "end_date": "2024-02-03",
            "info": "string",
            "solution": "string",
            "sale": "string",
            "signature_emplooye": "string",
            "signature_client": "string"
            }
        json_data = json.dumps(data)
        mock_response.status_code, mock_response.json.return_value = 200, response
        mock_put.return_value = mock_response
        os_status, os_data = make_put_request(API_BASE_URL + '/os_constructions/update-os-constructions/1', json_data)
        self.assertEqual(os_data, response)
        self.assertEqual(os_status, 200)

    @patch('requests.delete')
    def test_delete_os_construction_data(self, mock_delete):
        mock_response = Mock()
        response = {"message": "Ordem de Serviço deletada com sucesso"}
        mock_response.status_code, mock_response.json.return_value = 200, response
        mock_delete.return_value = mock_response
        os_status, os_data = make_delete_request(API_BASE_URL + '/os_constructions/delete-os-constructions/1')
        self.assertEqual(os_data, response)
        self.assertEqual(os_status, os_status)


if __name__ == '__main__':
    unittest.main()