# -*- coding: utf-8 -*-
"""Copy of Syslog.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k_HLE6EigXjc_GcvTv1LSuQmmj9ZHzij
"""

raw_list=[]
import sys
filename=sys.argv[1]
#print(filename)
with open(filename+"_classified.csv") as file:
    for line in file:
        line = line.strip()
        if len(line)!=0:
            raw_list.append(line)

logcount=raw_list[1].split(",")[5]
#print(logcount)

item_line = 0
start_line = 1
end_line = 0
recov_cnt = 0
normal_cnt = 0
unknown_cnt = 0
data_cnt = 0
raw_list[item_line]=raw_list[item_line]+",Recovered,Normal,Unknown,Total_Count"
with open(filename+"_statistics.csv", 'w') as out_f:
    while start_line < len(raw_list):
        #print(start_line)
        try:
            logcount=raw_list[start_line].split(",")[5]
        except IndexError:
            logcount=0
        if int(logcount) > 0:
            end_line=start_line+int(logcount)+3
            op=0
            while op !=1:
                try:
                    raw_list[end_line].split(",")
                    if raw_list[end_line].split(",")[0]!="\"":
                        end_line=end_line-1
                except IndexError:
                    end_line=end_line-1
                    break
                else:
                    op=1
        #print("@@"+"end_line="+str(end_line)+raw_list[end_line])
        try:
            onstatus=raw_list[end_line].split(",")[4]
        except IndexError:
            print(raw_list[end_line])
            raw_list[end_line]=raw_list[end_line]+",normal,"
            print(raw_list[end_line])
        try:
            offstatus=raw_list[end_line].split(",")[5]
        except IndexError:
            print(raw_list[end_line])
            raw_list[end_line]=raw_list[end_line]+",normal,"
            print(raw_list[end_line])
        #print("@@"+str(raw_list[end_line].split(",")))
        #print("@@"+str(len(raw_list[end_line].split(","))))
#---------------------------------------------------------------------------------
        if not onstatus:
            raw_list_replaced_flag=0
            for idx in range(0,6):
                if raw_list_replaced_flag==0:
                    raw_list_replaced=""
                    raw_list_replaced_flag=1
                if idx == 4:
                    raw_list_replaced=raw_list_replaced+"normal"+","
                else:
                    raw_list_replaced=raw_list_replaced+raw_list[end_line].split(",")[idx]+","
            raw_list[end_line]=raw_list_replaced
#----------------------------------------------------------------------------------

        if not offstatus:
            normal_cnt+=1
            raw_list_replaced_flag=0
            for idx in range(0,6):
                  #print(raw_list[end_line])
                  #print("idx="+str(idx)+","+raw_list[end_line].split(",")[idx])
                  #print(raw_list[end_line].split(",")[5])
                  if raw_list_replaced_flag==0:
                      raw_list_replaced=""
                      raw_list_replaced_flag=1
                  #print("@@"+raw_list[end_line])
                  if idx == 5:
                      raw_list_replaced=raw_list_replaced+"normal"+","
                  else:
                      raw_list_replaced=raw_list_replaced+raw_list[end_line].split(",")[idx]+","
            raw_list[end_line]=raw_list_replaced
        if offstatus == "Unknown":
            unknown_cnt+=1
        if offstatus == "Recovered":
            recov_cnt+=1
        print(end_line)    
        start_line = end_line +1

    #print(normal_cnt)
    #print(unknown_cnt)
    #print(recov_cnt)
    #print(data_cnt)
    #print(raw_list[1])
    data_cnt=normal_cnt+unknown_cnt+recov_cnt
    item_list_replaced_flag=0
    for idx in range(0,7):
        if item_list_replaced_flag==0:
            item_list_replaced=""
            item_list_replaced_flag=1
        if idx == 6:
            item_list_replaced=item_list_replaced+'\"'
            #print("idx = "+str(idx))
            #print("@@"+raw_list[1])
        else:
            item_list_replaced=item_list_replaced+raw_list[1].split(",")[idx]+","
    raw_list[1]=item_list_replaced
    log_cnt=raw_list[1].split(",")[5]
    end_line_first=1+int(log_cnt)+3
    raw_list[end_line_first]=raw_list[end_line_first]+str(recov_cnt)+","+str(normal_cnt)+","+str(unknown_cnt)+","+str(data_cnt)
    print("@@"+raw_list[end_line_first])
    for cnt in range(0,len(raw_list)-1):
        out_f.write(raw_list[cnt]+"\n")
