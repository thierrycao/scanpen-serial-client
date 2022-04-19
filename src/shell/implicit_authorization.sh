#!/bin/bash

echo "################################################"
echo -n "#   " && date
echo "#               Auth Start!                     "
echo "################################################"
echo ""
echo ""
###############################################

# 扫描笔测试
client_id="ad9f3c5d-38fd-4383-8d8d-8d460590de22"
device_id="12345"

if [ $# -eq 2 ];then
	client_id=$1
	device_id=$2
fi

###############################################
access_token_file="access_token.json"
## 0. check Whether Authorization is overdue

if [ ! $client_id ] && [ ! $device_id ];then
	echo "client_id or device_id is null!"
	exit
fi

echo "client_id:"$client_id
echo "device_id:"$device_id

if [ -e "$access_token_file" ];then
	access_token_local_info=$(cat $access_token_file)
	ret=$(( $(echo $access_token_local_info | jq ".created_at") - $(date +%s) + $(echo $access_token_local_info | jq ".expires_in")))
	echo "################################################"
	echo -n "#   local time:" && date "+%Y-%m-%d %H:%M:%S"
	echo -n "#   created_at:" && date -d "@$(echo $access_token_local_info | jq ".created_at")" "+%Y-%m-%d %H:%M:%S"
	echo -n "#   expired_in:" && echo $(($(echo $access_token_local_info | jq ".expires_in")/3600/24)) "天"
	echo -n "#   The remaining number of days:" && echo $((ret/3600/24)) "天"
	echo "################################################"
	if [ $(($ret-24*60*60)) -gt 0 ];then
		echo "Congratunations, access token is Within the validity period!"
		exit
	else
		echo "Less than one day remaining, now fresh access token"

		url_refresh="https://auth.iflyos.cn/oauth/ivs/token"
		header_refresh="content-type:application/json"
		params_refresh="{\"grant_type\": \"refresh_token\",\"refresh_token\":$(echo $access_token_local_info | jq ".refresh_token")}"
		result_refresh=$(curl -X POST $url_refresh -H $header_refresh -d "$params_refresh")

		echo $result_refresh | jq

		if [ $(echo $result_refresh | grep access_token) ];then
			echo $result_refresh | jq ". | {token_type: .token_type, refresh_token:.refresh_token, expires_in: .expires_in, created_at:.created_at, access_token:.access_token, device_id: ${device_id} }" > $access_token_file
			echo "Congratunations, access token is refreshed OK!"
			exit
		fi
	fi
fi

## 1. post new accesscode
url="https://auth.iflyos.cn/oauth/ivs/device_code"
header="'content-type:application/x-www-form-urlencoded'"
scope_data="{\"user_ivs_all\": {\"device_id\":  \"$device_id\"}}"
scope_data_urlencode=$(echo -n $scope_data | sed -e 's/\"/%22/g' -e 's/\:/%3A/g' -e 's/{/%7B/g' -e 's/\}/%7D/g' -e 's/ /%20/g' )
params="client_id=${client_id}&scope=user_ivs_all user_device_text_in&scope_data=$scope_data_urlencode"

echo "------------params--------------"
echo $params

commands="curl -X POST $url -H $header -d $params"
echo "------------------------------------------------"
echo $commands
echo "################################################"
echo "#      1. request device_code user_code         "
echo -n "#   " && date
echo "################################################"
ret=$(curl -X POST $url -H $header -d "$params")
echo $ret | jq

user_code=$(echo $ret | jq '.user_code')
device_code=$(echo $ret | jq '.device_code')
verification_uri=$(echo $ret | jq '.verification_uri')

#######################################################################################################
## 3. query result
url_query="https://auth.iflyos.cn/oauth/ivs/token"
header_query="content-type:application/json"
params_query="{\"client_id\": \"$client_id\", \"grant_type\":\"urn:ietf:params:oauth:grant-type:device_code\", \"device_code\":$device_code}"

echo $params_query

{
	sleep 1
	echo "################################################"
	echo "#      3. query result                          "
	echo -n "#   " && date
	echo "################################################"
	for i in `seq 30`
	do
		{
			sleep 1
			result_query=$(curl -X POST $url_query -H $header_query -d "$params_query" 2>/dev/null)
			echo "result_query:"$result_query
			echo $result_query | jq
			if [ $(echo $result_query | grep access_token) ];then
				echo $result_query | jq ". | {token_type: .token_type, refresh_token:.refresh_token, expires_in: .expires_in, created_at:.created_at, access_token:.access_token, device_id:\"${device_id}\" }" > $access_token_file
				exit
			fi
		}
	done
}&

#######################################################################################################
## 2. Implicit authorization

url_implicit_auth="https://api.iflyos.cn/thirdparty/general/auth"
header_implicit_auth="content-type:application/json"
params_second="{\"client_id\":\"$client_id\",\"thirdparty_id\":\"$device_id\",\"user_code\":$user_code}"


echo "#########################################"
echo "#      2. Implicit authorization         "
echo "#               start                    "
echo -n "#   " && date
echo "#########################################"

result_implicit_auth=$(curl -X POST $url_implicit_auth -H $header_implicit_auth -d "$params_second" 2>/dev/null)

echo "#########################################"
echo "#      2. Implicit authorization         "
echo "#              result                    "
echo -n "#      " && echo $result_implicit_auth
echo "#########################################"

wait  ##等待所有子后台进程结束
echo "############################################"
echo -n "#   " && date
echo "#               Auth End!                   "
echo "############################################"
