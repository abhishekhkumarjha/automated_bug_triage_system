import requests
import json

# Test multiple examples
test_cases = [
    {
        'title': 'Login page not loading on mobile',
        'description': 'Users report that the login page is completely blank when accessed from mobile devices'
    },
    {
        'title': 'Database connection failing',
        'description': 'The application cannot connect to the database server during peak hours'
    },
    {
        'title': 'Button styling broken in Chrome',
        'description': 'The submit button appears grayed out and unclickable in Google Chrome browser'
    },
    {
        'title': 'API returning 500 errors',
        'description': 'The REST API endpoints are intermittently returning 500 internal server errors'
    }
]

url = 'http://localhost:8000/predict'

print("Testing Bug Triage API with Enhanced Model")
print("=" * 50)

for i, test_case in enumerate(test_cases, 1):
    print(f'\nTest Case {i}:')
    print(f'Title: {test_case["title"]}')

    try:
        response = requests.post(url, json=test_case)
        if response.status_code == 200:
            result = response.json()
            print(f'Assigned to: {result["assigned_to"]} (confidence: {result["assignment_confidence"]:.3f})')
            print(f'Priority: {result["priority"]} (confidence: {result["priority_confidence"]:.3f})')
            print(f'Duplicate: {result["is_duplicate"]}')
        else:
            print(f'API Error: {response.status_code}')
            print(response.text)
    except Exception as e:
        print(f'Request failed: {e}')

print("\n" + "=" * 50)
print("Summary: The model has been enhanced with synthetic data")
print("and should provide more accurate predictions!")