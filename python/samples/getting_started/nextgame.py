import requests

# Replace 'YOUR_API_TOKEN' with your actual Sportmonks API token
api_token = 'uAGgkpv5iN1tjFFrGYdH9CUERiZz65BpGiUkmbQUYOsZb4A0MVBWDawfm7hy'

# The endpoint for fixtures (matches)
url = "https://soccer.sportmonks.com/api/v2.0/fixtures"

# Parameters for the API request
# 'team_id' should be replaced with the actual ID of Manchester United in the Sportmonks database
# 'from' and 'to' specify the date range for the fixtures. Adjust these as needed.
params = {
    'api_token': api_token,
    'team_id': '1',
    'from': '2024-02-17',
    'to': '2024-12-31'
}

# Send the API request
response = requests.get(url, params=params)

# Parse the JSON response
data = response.json()

# Check if 'data' key exists and if it contains any elements
if 'data' in data and len(data['data']) > 0:
    # Print the next fixture
    print(data['data'][0])
else:
    print("No fixture data available.")
