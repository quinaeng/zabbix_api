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

def create_host(url, auth_token):
    args = sys.argv
    hostname = args[1]
    headers = {'Content-Type': 'application/json-rpc'}
    data = {
        'jsonrpc': '2.0',
        'method': 'host.create',
        'params': {
            'host': hostname,
            'interfaces': [
                {
                    'type': 1,  # agent
                    'main': 1,
                    'useip': 1,
                    'ip': '192.168.10.72',  # ホストのIPアドレス
                    'dns': '',
                    'port': '10050'  # エージェントのポート
                }
            ],
            'groups': [{'groupid': '2'}],  # ホストが所属するグループのID
            'templates': [{'templateid': '10441'}]  # 適用するテンプレートのID
        },
        'auth': auth_token,
        'id': 1
    }

    # APIリクエストの送信
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # レスポンスの表示
    print(response.json())

create_host(url, auth_token)
