#Get access token

import requests
import requests.auth
client_auth = requests.auth.HTTPBasicAuth('52b_-ogrKMs1rpbT0d-TJQ', 'IQF_XzdHCsPHXvWcNqGbD1YCmZurGA')
post_data = {"grant_type": "password", "username": "Otto_kuosmanen", "password": "reddIt3?"}
headers = {"User-Agent": "advicedata/0.1 by Otto_kuosmanen"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
TOKEN = response.json()['access_token']

headers['Authorization'] = f'bearer {TOKEN}'

#print(requests.get('https://oauth.reddit.com/api/v1/me', headers=headers).json())

res = requests.get('https://oauth.reddit.com/r/advice/hot', headers = headers)
print(res.json())

