import requests

response = requests.post('http://localhost:8000/lockcolor/invoke', json={'input': {'input': 'What happens in dark brown skies?'}})

print(response.json())