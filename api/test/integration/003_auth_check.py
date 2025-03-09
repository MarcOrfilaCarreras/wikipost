import requests

BASE_URL = 'http://localhost:8080'

JWT_TOKEN = None


def test_get_token():
    global JWT_TOKEN

    payload = {
        'email': 'validuser@example.com',
        'password': 'SecurePassword123'
    }

    response = requests.post(f'{BASE_URL}/auth/login', json=payload)

    if response.status_code == 200:
        JWT_TOKEN = response.json()['data']['token']


def test_check_authorization_success():
    global JWT_TOKEN

    headers = {
        'Authorization': f'Bearer {JWT_TOKEN}'
    }

    response = requests.get(f'{BASE_URL}/auth/check', headers=headers)

    if response.status_code != 200:
        print(f'❌ Test Failed: Failed with status code {response.status_code}')
        return

    response_data = response.json()
    if (response_data.get('status') != 'success') or ('data' not in response_data):
        print(f'❌ Test Failed: Unexpected response data')
        return

    print('✅ Test Passed: Authorization successful and response is as expected')


def test_check_missing_authorization():
    response = requests.get(f'{BASE_URL}/auth/check')

    if response.status_code == 401:
        print('✅ Test Passed: Missing Authorization header returned status code 401')
    else:
        print(
            f'❌ Test Failed: Missing Authorization header returned unexpected status code {response.status_code}')


def test_check_invalid_token():
    headers = {
        'Authorization': 'Bearer invalid_token'
    }

    response = requests.get(f'{BASE_URL}/auth/check', headers=headers)

    if response.status_code == 401:
        print('✅ Test Passed: Invalid Authorization token returned status code 401')
    else:
        print(
            f'❌ Test Failed: Invalid Authorization token returned unexpected status code {response.status_code}')
        print('Response body:', response.text)


test_get_token()
test_check_authorization_success()
test_check_missing_authorization()
test_check_invalid_token()
