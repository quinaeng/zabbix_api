import requests
import json

# Zabbixサーバーの情報
url = 'http://192.168.10.70/zabbix/api_jsonrpc.php'
username = 'Admin'
password = 'zabbix'

# ログイン用のAPIリクエストを作成
auth_headers = {'Content-Type': 'application/json-rpc'}

# 認証トークンを取得する関数
def get_auth_token(url, username, password):
    auth_data = {
        'jsonrpc': '2.0',
        'method': 'user.login',
        'params': {
            'user': username,
            'password': password
        },
        'id': 1
    }
    response = requests.post(url, headers=auth_headers, data=json.dumps(auth_data))
    return response.json()['result']

auth_token = get_auth_token(url, username, password)
print(auth_token)