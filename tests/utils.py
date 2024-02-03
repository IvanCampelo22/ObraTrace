import requests


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
