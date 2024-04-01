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

# ホスト情報を取得する関数
def get_hosts(url, username, password):
    auth_token = get_auth_token(url, username, password)
    headers = {'Content-Type': 'application/json-rpc'}
    data = {
        'jsonrpc': '2.0',
        'method': 'host.get',
        'params': {
            'output': ['host', 'hostid']
        },
        'auth': auth_token,
        'id': 1
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    host_data = response.json()['result']
    hosts = {}
    for host in host_data:
        hosts[host['hostid']] = host['host']
    return hosts

# ホスト一覧を取得
hosts = get_hosts(url, username, password)
print("Hosts:", hosts)
