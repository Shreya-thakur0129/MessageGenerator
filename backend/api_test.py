# Test the message generation endpoint
import requests

def test_generate_message():
    url = 'http://localhost:8000/generate-message'
    headers = {'Content-Type': 'application/json'}
    test_cases = [
        {"prompt": "Send Diwali wishes to customers"},
        {"prompt": "Send new year message"},
        {"prompt": "Send birthday wishes"},
        {"prompt": "Send a general greeting"}
    ]
    
    for test_case in test_cases:
        try:
            print(f"\nTesting prompt: {test_case['prompt']}")
            response = requests.post(url, json=test_case, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json() if response.ok else response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_generate_message()