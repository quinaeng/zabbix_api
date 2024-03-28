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
def get_template_id(url, username, password, template_name):
    auth_token = get_auth_token(url, username, password)
    headers = {'Content-Type': 'application/json-rpc'}
    data = {
        'jsonrpc': '2.0',
        'method': 'template.get',
        'params': {
            'output': 'extend',
            'filter': {
                'host': [template_name]
            }
        },
        'auth': auth_token,
        'id': 1
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    template_data = response.json()['result']
    if template_data:
        return template_data[0]['templateid']  # 最初に一致したテンプレートのtemplateidを返す
    else:
        return None

# テンプレート名からテンプレートIDを取得
template_id = get_template_id(url, username, password, 'Zabbix-Template-Linux')
print("Template ID:", template_id)
