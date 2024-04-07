import requests
import json
import sys

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

# ホストの作成用のAPIリクエストを作成

def update_host(url, auth_token):
    args = sys.argv
    hostid = args[1]
    headers = {'Content-Type': 'application/json-rpc'}
    data = {
        'jsonrpc': '2.0',
        'method': 'host.update',
        'params': {
            'hostid': hostid,
            'proxy_hostid': '10438',
        },
        'auth': auth_token,
        'id': 1
    }

    # APIリクエストの送信
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # レスポンスの表示
    print(response.json())

update_host(url, auth_token)
