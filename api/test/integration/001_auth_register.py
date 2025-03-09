import requests

BASE_URL = 'http://localhost:8080'


def test_register_success():
    payload = {
        'email': 'validuser@example.com',
        'password': 'SecurePassword123'
    }

    response = requests.post(f'{BASE_URL}/auth/register', json=payload)

    if response.status_code != 201:
        print(
            f'❌ Test Failed: Registration failed with status code {response.status_code}')
        return

    response_data = response.json()

    if (not 'data' in response_data) or (not isinstance(response_data['data'], dict)):
        print("❌ Test Failed: 'data' field is missing or incorrect")
        return

    if (not 'status' in response_data) or (response_data['status'] != 'success'):
        print("❌ Test Failed: 'success' field is missing or incorrect")
        return

    print('✅ Test Passed: User successfully registered')


def test_register_missing_fields():
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


def test_register_invalid_fields():
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


if __name__ == '__main__':
    test_register_missing_fields()
    test_register_invalid_fields()
    test_register_success()
