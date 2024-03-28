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

# テンプレートIDを取得する関数
def get_template_ids(url, username, password):
    auth_token = get_auth_token(url, username, password)
    headers = {'Content-Type': 'application/json-rpc'}
    data = {
        'jsonrpc': '2.0',
        'method': 'template.get',
        'params': {
            'output': ['templateid', 'host']  # テンプレートIDとホスト名を取得するように修正
        },
        'auth': auth_token,
        'id': 1
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    template_data = response.json()['result']
    template_ids = {}
    for template in template_data:
        template_ids[template['host']] = template['templateid']
    return template_ids

# テンプレート名からテンプレートIDを取得
template_ids = get_template_ids(url, username, password)
print("Template IDs:", template_ids)
