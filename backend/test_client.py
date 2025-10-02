# Test the message generation endpoint
import requests

def test_generate_message():
    # Test cases
    test_prompts = [
        "Send Diwali wishes to customers",
        "Send new year message",
        "Send birthday wishes",
        "Send a general greeting"
    ]
    
    for prompt in test_prompts:
        print(f"\nTesting prompt: {prompt}")
        try:
            response = requests.post(
                'http://localhost:8000/generate-message',
                json={"prompt": prompt}
            )
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_generate_message()