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

# ホストのステータスを更新する関数
def disable_host(url, auth_token, host_id):
    headers = {'Content-Type': 'application/json-rpc'}
    data = {
        'jsonrpc': '2.0',
        'method': 'host.update',
        'params': {
            'hostid': host_id,
            'status': 1  # ステータスを無効にする
        },
        'auth': auth_token,
        'id': 1
    }

    # APIリクエストの送信
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # レスポンスの表示
    print(response.json())

# ホストIDを取得する関数
def get_host_id(url, auth_token, hostname):
    headers = {'Content-Type': 'application/json-rpc'}
    data = {
        'jsonrpc': '2.0',
        'method': 'host.get',
        'params': {
            'filter': {
                'host': [
                    hostname
                ]
            },
            'output': [
                'hostid'
            ]
        },
        'auth': auth_token,
        'id': 1
    }

    # APIリクエストの送信
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()['result']

    if result:
        return result[0]['hostid']
    else:
        print("ホストが見つかりませんでした。")
        return None

# ホストを無効にする
hostname = input("無効にしたいホスト名を入力してください: ")
host_id = get_host_id(url, auth_token, hostname)
if host_id:
    disable_host(url, auth_token, host_id)

