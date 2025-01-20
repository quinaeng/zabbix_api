#!/bin/bash

# Zabbix API接続情報
zabbix_url='http://192.168.10.20/zabbix/api_jsonrpc.php'
zabbix_user='Admin'
zabbix_password='zabbix'

# jqコマンドの存在チェック
if ! command -v jq &> /dev/null; then
    echo "Error: jq コマンドが見つかりません。インストールしてください。"
    exit 1
fi

# Zabbix APIキー取得リクエスト
secret=$(cat <<EOF
{
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "username": "${zabbix_user}",
        "password": "${zabbix_password}"
    },
    "id": 1
}
EOF
)

# APIキー取得
api_key=$(curl -s -X POST -H "Content-Type: application/json" -d "$secret" "$zabbix_url" | jq -r '.result')

if [ -z "$api_key" ] || [ "$api_key" == "null" ]; then
    echo "Error: APIキーの取得に失敗しました。"
    exit 1
fi

# 引数チェック
if [ $# -lt 1 ]; then
    echo "Usage: bash zabbix-api.sh [json file] [option]..."
    exit 1
elif [ ! -f "$1" ]; then
    echo "Error: 指定されたファイル '$1' が存在しません。"
    exit 1
fi

# JSONデータの読み込み
json_file="$1"
data=$(cat "$json_file")

# JSON内の変数抽出 (${変数名} 形式。ただし api_key を除外）
json_vars=$(echo "$data" | grep -o "\${[^}]*}" | sed 's/[${}]//g' | grep -v '^api_key$')

# JSON内の変数を配列に格納
json_vars_array=($json_vars)

# オプション引数処理
args=("$@")
arg_length=$#
count=2

# 渡された引数の変数名を収集
provided_vars=()
while [ $count -le $arg_length ]; do
    word=$(echo "${args[$((count-1))]}" | cut -d'=' -f1)
    provided_vars+=("$word")
    ((count++))
done

# JSON変数と引数の整合性チェック（api_keyを除外）
for json_var in "${json_vars_array[@]}"; do
    if [[ ! " ${provided_vars[*]} " =~ " $json_var " ]]; then
        echo "Error: JSON内で使用されている変数 '${json_var}' の値が指定されていません。"
        exit 1
    fi
done

# 引数で指定された余分な変数のチェック（api_keyを除外）
for provided_var in "${provided_vars[@]}"; do
    if [[ ! " ${json_vars_array[*]} " =~ " $provided_var " ]]; then
        echo "Error: 引数で指定された変数 '${provided_var}' はJSON内で使用されていません。"
        exit 1
    fi
done

# JSON内の変数を置換
for json_var in "${json_vars_array[@]}"; do
    value=$(echo "${args[@]:1}" | tr ' ' '\n' | grep "^${json_var}=" | cut -d'=' -f2)
    data=$(echo "$data" | sed "s|\${${json_var}}|${value}|g")
done

# APIキーをJSONデータに置換
data=$(echo "$data" | sed "s|\${api_key}|${api_key}|g")

# Zabbix APIリクエスト
response=$(curl -s -X POST -H "Content-Type: application/json" -d "$data" "$zabbix_url")
if [ $? -ne 0 ]; then
    echo "Error: Zabbix APIへのリクエストに失敗しました。"
    exit 1
fi

# レスポンスの処理
result=$(echo "$response" | jq '.result')
if [ "$result" == "null" ]; then
    error=$(echo "$response" | jq '.error')
    echo "Error: $error"
    exit 1
else
    echo "Success: $result"
fi

