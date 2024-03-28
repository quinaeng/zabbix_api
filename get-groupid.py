import requests
import json

# Zabbixサーバーの情報
url = 'http://192.168.10.70/zabbix/api_jsonrpc.php'
username = 'Admin'
password = 'zabbix'

# 認証トークンを取得する関数
def get_auth_token(url, username, password):
    headers = {'Content-Type': 'application/json-rpc'}
    data = {
        'jsonrpc': '2.0',
        'method': 'user.login',
        'params': {
            'user': username,
            'password': password
        },
        'id': 1
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()['result']

# すべてのグループのグループIDを取得する関数
def get_all_group_ids(url, username, password):
    auth_token = get_auth_token(url, username, password)
    headers = {'Content-Type': 'application/json-rpc'}
    data = {
        'jsonrpc': '2.0',
        'method': 'hostgroup.get',
        'params': {
            'output': ['groupid', 'name']
        },
        'auth': auth_token,
        'id': 1
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    group_data = response.json()['result']
    group_ids = {}
    for group in group_data:
        group_ids[group['name']] = group['groupid']
    return group_ids

# すべてのグループのグループIDを取得
all_group_ids = get_all_group_ids(url, username, password)
print("All Group IDs:", all_group_ids)
