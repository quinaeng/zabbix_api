import requests
import json

# Zabbixサーバーの情報
url = 'http://192.168.10.70/zabbix/api_jsonrpc.php'
username = 'Admin'
password = 'zabbix'

# APIリクエストの準備
headers = {'Content-Type': 'application/json-rpc'}
data = {
    'jsonrpc': '2.0',
    'method': 'host.create',
    'params': {
        'host': 'host01',
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
    'auth': None,
    'id': 1
}

# APIリクエストの送信
response = requests.post(url, headers=headers, data=json.dumps(data), auth=(username, password))

# レスポンスの表示
print(response.json())

