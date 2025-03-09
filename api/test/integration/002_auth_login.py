import requests

BASE_URL = 'http://localhost:8080'


def test_login_success():
    payload = {
        'email': 'validuser@example.com',
        'password': 'SecurePassword123'
    }

    response = requests.post(f'{BASE_URL}/auth/login', json=payload)

    if response.status_code != 200:
        print(
            f'❌ Test Failed: Login failed with status code {response.status_code}')
        return

    response_data = response.json()

    if (response_data.get('status') != 'success') or ('token' not in response_data['data']):
        print('❌ Test Failed: Response data is not as expected')
        return

    print('✅ Test Passed: Successful login')


def test_login_invalid_fields():
    fields = {
        'email': 'email',
        'password': 'notsecure'
    }

    for field, value in fields.items():
        payload = {field: value}

        response = requests.post(f'{BASE_URL}/auth/register', json=payload)

        if response.status_code == 400:
            print(
                f"✅ Test Passed: Invalid '{field}' field returned status code 400")
        else:
            print(
                f"❌ Test Failed: Invalid '{field}' field returned unexpected status code {response.status_code}")


def test_login_missing_fields():
    fields = {
        'email': 'email@example.com',
        'password': 'SecurePassword123'
    }

    for field, value in fields.items():
        payload = {field: value}

        response = requests.post(f'{BASE_URL}/auth/register', json=payload)

        if response.status_code == 400:
            print(
                f"✅ Test Passed: Missing '{field}' field returned status code 400")
        else:
            print(
                f"❌ Test Failed: Missing '{field}' field returned unexpected status code {response.status_code}")


def test_user_not_found():
    payload = {
        'email': 'nonexistentuser@example.com',
        'password': 'AnyPassword123'
    }

    response = requests.post(f'{BASE_URL}/auth/login', json=payload)

    if response.status_code == 400:
        print('✅ Test Passed: User not found returned status code 400')
    else:
        print(
            f'❌ Test Failed: User not found returned unexpected status code {response.status_code}')


def test_login_wrong_password():
    payload = {
        'email': 'validuser@example.com',
        'password': 'WrongPassword123'
    }

    response = requests.post(f'{BASE_URL}/auth/login', json=payload)

    if response.status_code == 400:
        print('✅ Test Passed: Incorrect password returned the expected status code 400 and message')
    else:
        print(
            f'❌ Test Failed: Incorrect password returned unexpected status code {response.status_code}')


test_login_success()
test_login_invalid_fields()
test_login_missing_fields()
test_user_not_found()
test_login_wrong_password()
