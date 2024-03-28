import requests
import json

# Zabbixサーバーの情報
url = 'http://192.168.10.70/zabbix/api_jsonrpc.php'
username = 'Admin'
password = 'zabbix'

# ログイン用のAPIリクエストを作成
headers = {'Content-Type': 'application/json-rpc'}
data = {
    'jsonrpc': '2.0',
    'method': 'user.login',
    'params': {
        'user': username,
        'password': password
    },
    'auth': None,
    'id': 1
}

# APIリクエストを送信
response = requests.post(url, headers=headers, data=json.dumps(data))

# 認証トークンを取得
auth_token = response.json()['result']
print("Authentication token:", auth_token)

