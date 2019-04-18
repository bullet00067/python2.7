#!/bin/bash

dir=$1
start_time=$(echo $dir | awk -F[_] '{print $1}'| awk -F[-] '{print $1"-"$2"-"$3" "$4":"$5":00"}')
end_time=$(echo $dir | awk -F[_] '{print $2}' | awk -F[-] '{print $1"-"$2"-"$3" "$4":"$5":00"}')
round=1

output="output"

if [  -d $output ]; then rm -rf $output; fi

mkdir -p $output

mqtt_log="./$dir/20190114-1834_MQTT.log"

ips=

echo "$start_time to $end_time"

for file in $(find $dir -name "SyslogCatchAll-*_*.txt" | sort); do
	echo "[$ip] $file"
	
	ip=$(basename $file | awk -F[_.] '{print "192.168.1."$2}')
	
	ips="$ips $ip"
	
	mkdir -p $output/$ip
		
	syslog_file="$output/$ip/syslog.txt"
	mqtt_file="$output/$ip/mqtt.txt"
	
#	cat $file >> $syslog_file #20190417 filter the ip we focus on.
	cat $file | grep -a $ip  > $syslog_file
	cat $mqtt_log | grep $ip | sed -e 's|/eslps/[^ ]*|& ip |g'> $mqtt_file
done;

for ip in $ips; do
	syslog_file="$output/$ip/syslog.txt"
	mqtt_file="$output/$ip/mqtt.txt"

	ip_file="$output/$ip/device.txt"
	csv_file=$output/$ip/[$ip].csv
	csv_classifier=$output/$ip/[$ip]

	cat $syslog_file $mqtt_file | sort -n > $ip_file
	
	echo "[$ip] $ip_file to $csv_file"
	
	if [ ! -f $csv_file ]; then
		echo "ROUND,LOOP,STARTTIME,ENDTIME,IP,LOGCOUNT,LOG,STATUS,ONCOUNT,OFFCOUNT" > $csv_file
	fi

#	echo ./parser2.sh $ip_file \"$start_time\" \"$end_time\" $csv_file 1
	time ./parser2.sh $ip_file "$start_time" "$end_time" $csv_file 1
	python syslog_classifierv2.py $csv_classifier 
	python syslog_statisticsv2.py $csv_classifier
done
