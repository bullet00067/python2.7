#!/bin/sh

filename=$1
startdatetime=$2
enddatetime=$3
out_csv=$4
round=$5

duration=360
on_duration=180
name=$(basename $filename)

startime=$(date -d "$startdatetime" +%s)
endtime=$(date -d "$enddatetime" +%s)

out_start_datetime=$(date -d @$startime '+%Y%m%d-%H%M')
out_end_datetime=$(date -d @$endtime '+%Y%m%d-%H%M')

loop=0
loop_start=$startime
loop_end=$startime
loop_switch=$(( $loop_start + $on_duration ))

datetime=$(cat $filename | head -n 1 | awk '{print $1 " " $2}')
time=$(date -d "$datetime" +%s)
ip=$(cat $filename | head -n 1 | awk '{print $4}')

#echo "ROUND,LOOP,STARTTIME,ENDTIME,IP,LOGCOUNT,LOG,STATUS" > $out_csv
log_count=0
log_count_on=0
log_count_off=0
log_file=csv_log_text.txt
log_text=

datetime=$(cat $filename | head -n 1 | awk '{print $1 " " $2}')
time=$(date -d "$datetime" +%s)

if [ $time -le $loop_start ];then 
	while [ $time -gt $loop_start ]; do
		loop=$(( $loop + 1 ))
		loop_start=$loop_end
		loop_end=$(( $loop_start + $duration ))
		loop_switch=$(( $loop_start + $on_duration ))
		log_count=0
		log_count_on=0
		log_count_off=0

		loop_start_datetime=$(date -d @$loop_start '+%Y-%m-%d %H:%M:%S')
		loop_end_datetime=$(date -d @$loop_end '+%Y-%m-%d %H:%M:%S')
		loop_switch_datetime=$(date -d @$loop_switch '+%Y-%m-%d %H:%M:%S')

		echo > $log_file
		echo "$loop_start_datetime | =====Relay Noise ON=====" >> $log_file
		echo "$loop_switch_datetime | =====Relay Noise OFF=====" >> $log_file

		echo "$round,$loop,$loop_start_datetime,$loop_end_datetime,$ip,$log_count,\"" >> $out_csv
		cat $log_file >> $out_csv
		echo "\",0,$log_count_on,$log_count_off"  >> $out_csv
	done
else
	loop=$(( $loop + 1 ))
	loop_start=$loop_end
	loop_end=$(( $loop_start + $duration ))
	loop_switch=$(( $loop_start + $on_duration ))
	log_count=0
	log_count_on=0
	log_count_off=0
	
	loop_start_datetime=$(date -d @$loop_start '+%Y-%m-%d %H:%M:%S')
	loop_end_datetime=$(date -d @$loop_end '+%Y-%m-%d %H:%M:%S')
	loop_switch_datetime=$(date -d @$loop_switch '+%Y-%m-%d %H:%M:%S')
fi

echo > $log_file

while read p; do
	datetime=$(echo $p | awk '{print $1 " " $2}')
	time=$(date -d "$datetime" +%s)
	msg=$(echo $p | awk '{for(i=5;i<=NF;i++) printf $i" "; print ""}' | sed -e 's|"| |g')
	if [ $time -gt $loop_end ]; then
		echo "$round,$loop,$loop_start_datetime,$loop_end_datetime,$ip,$log_count,\"" >> $out_csv
		cat $log_file >> $out_csv
		echo "\",,$log_count_on,$log_count_off"  >> $out_csv
		echo > $log_file
		
		loop=$(( $loop + 1 ))
		loop_start=$loop_end
		loop_end=$(( $loop_start + $duration ))
		loop_switch=$(( $loop_start + $on_duration ))
		log_count=0
		log_count_on=0
		log_count_off=0

		loop_start_datetime=$(date -d @$loop_start '+%Y-%m-%d %H:%M:%S')
		loop_end_datetime=$(date -d @$loop_end '+%Y-%m-%d %H:%M:%S')
		loop_switch_datetime=$(date -d @$loop_switch '+%Y-%m-%d %H:%M:%S')		
	fi

	# loop before first log
	if [ $time -gt $loop_start -a $time -le $loop_end ]; then
		log_count=$(( $log_count + 1 )) 
		
		if [ $time -le $loop_switch ]; then
			if [ $log_count_on -eq 0 ]; then
				echo "$loop_start_datetime | =====Relay Noise ON=====" >> $log_file
			fi
			log_count_on=$(( $log_count_on + 1 )) 
		fi

		if [ $time -gt $loop_switch ]; then
			if [ $log_count_off -eq 0 ]; then
				echo "$loop_switch_datetime | =====Relay Noise OFF=====" >> $log_file
			fi
			log_count_off=$(( $log_count_off + 1 )) 
		fi

		echo "$datetime | $msg" >> $log_file
	fi
done < $filename

while [ $loop_end -le $endtime ]; do
	loop=$(( $loop + 1 ))
	loop_start=$loop_end
	loop_end=$(( $loop_start + $duration ))
	loop_switch=$(( $loop_start + $on_duration ))
	log_count=0
	log_count_on=0
	log_count_off=0

	loop_start_datetime=$(date -d @$loop_start '+%Y-%m-%d %H:%M:%S')
	loop_end_datetime=$(date -d @$loop_end '+%Y-%m-%d %H:%M:%S')
	loop_switch_datetime=$(date -d @$loop_switch '+%Y-%m-%d %H:%M:%S')
	
	echo "" > $log_file
	echo "$loop_start_datetime | =====Relay Noise ON=====" >> $log_file
	echo "$loop_switch_datetime | =====Relay Noise OFF=====" >> $log_file
	
	echo "$round,$loop,$loop_start_datetime,$loop_end_datetime,$ip,$log_count,\"" >> $out_csv
	cat $log_file >> $out_csv
	echo "\",0,$log_count_on,$log_count_off"  >> $out_csv
done

rm $log_file
