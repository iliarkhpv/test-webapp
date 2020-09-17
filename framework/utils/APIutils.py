from framework.utils.assistance import get_config_data, get_test_data, generate_string
import requests
import json

test_data = get_test_data()
config_data = get_config_data()
URL = config_data['api']


def get_token(variant):
    params = {"variant": variant}
    response = requests.post(f'{URL}token/get', params=params)
    return response.text


def get_project_test(project_id):
    params = {"projectId": project_id}
    response = requests.post(f'{URL}test/get/json', params=params)
    return json.loads(response.text)


def post_test(sid, proj_name, test_name, method_name, env):
    params = {"SID": sid,
              "projectName": proj_name,
              "testName": test_name,
              "methodName": method_name,
              "env": env}
    response = requests.post(f'{URL}test/put', params=params)
    return response.text


def add_test_log(test_id, log):
    params = {"testId": test_id,
              "content": log}
    requests.post(f'{URL}test/put/log', params=params)


def add_test_screenshot(test_id, picture):
    params = {"testId": test_id,
              "content": picture,
              "contentType": "image/png"}
    requests.post(f'{URL}test/put/attachment', params=params)

