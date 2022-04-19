##########################################################################
# File Name: ota.sh
# Author: ThierryCao
# mail: iamthinker@163.com
# Created Time: Fri 08 May 2020 04:20:35 PM CST
#########################################################################
#!/bin/bash

URL="https://ota.iflyos.cn/ota/client/packages"

# CLIENT_ID  DEVICE_ID  SECRET
# 需要自己修改

CLIENT_ID="ad9f3c5d-38fd-4383-8d8d-8d460590de22"
DEVICE_ID="12345"
TIMESTAMP=$(date +%s)
NONCE=$(date +%s)
SECRET="" #填写自己的SECRET
str="${CLIENT_ID}:${DEVICE_ID}:${TIMESTAMP}:${NONCE}:${SECRET}"
SIGNATURE=$(echo -n $str | sha1sum | awk '{ print $1}')
echo "CLIENT_ID="$CLIENT_ID
echo "DEVICE_ID="$DEVICE_ID
echo "TIMESTAMP="$TIMESTAMP
echo "NONCE="$NONCE
echo "SECRET="$SECRET
echo "SIGNATURE="$SIGNATURE


result=$(curl -H "X-Client-ID: $CLIENT_ID" -H "X-Device-ID: $DEVICE_ID" -H "X-Timestamp: $TIMESTAMP" -H "X-Nonce: $TIMESTAMP" -H "X-Signature: $SIGNATURE" $URL)

if [ $(echo $result | jq '.[0]' | jq 'has("url")') == 'true' ];then
	result_url=$(echo $result | jq '.[0].url')
	result_url_del_quotes=$(echo $result_url |sed 's/\"//g')
	result_file=${result_url_del_quotes##*/}
	result_url_prefix=${result_url_del_quotes%*/$result_file}
	echo $result
	echo "url:"$result_url
	echo "file:"${result_file}
	echo "url_prefix:"$result_url_prefix


	if [ "$result_file" == 'info.txt' ];then
		(
        # wget --no-check-certificate "$result_url_del_quotes" > /dev/null 2>&1
			wget --no-check-certificate "$result_url_del_quotes" > /dev/null
		)&
		wait
		echo "等待下载info.txt"

		if [ -e "info.txt" ];then
			for i in $(cat info.txt);do
				file_sub=${i##*file=}

                if  [[ $i =~ ^file= ]];then
                     echo "file_sub:"$file_sub "i:"$i
				      file_sub_absolute="$result_url_prefix/files/$file_sub"
				     (
                     # wget --no-check-certificate -c -L $file_sub_absolute > /dev/null 2>&1
					      wget --no-check-certificate -c -L $file_sub_absolute
				     )&
                fi
			done

		fi
	else
		(
        # wget --no-check-certificate -c "$result_url_del_quotes" > /dev/null 2>&1
			wget --no-check-certificate -c "$result_url_del_quotes"
		)&
	fi

	wait
	echo "完成下载任务!"

fi
