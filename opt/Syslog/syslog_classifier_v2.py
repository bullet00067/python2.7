# -*- coding: utf-8 -*-
"""Syslog_classifier_V2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17EjzY5aFOLra0TTN70H7EWuIAOE7X5zf
"""

#with open("T[192.168.1.48].csv") as file:
#    for line in file:
#        print(line)


listed=[]
import sys
filename=sys.argv[1]
#print(filename)
with open("T[192.168.1.48]dbg.csv") as file:
    for line in file:
        line = line.strip()
        if len(line)!=0:
            listed.append(line)

#    print(len(listed))
#    print(listed)
kernel_panic_patterns = ["Backtrace", "kernel panic"]
is_reboot_patterns = ["[PROVISION]", "[BLUETOOTH]", "[SSH]", "[SYSTEM]"]
is_stable_patterns =["btmgmt:"]

def replace_element(listed, out_f, end, logtype, on_is_reboot, on_is_stable, off_is_reboot, off_is_stable):
    str_replaced=""
    #print(list_replaced[end])
    #print(on_is_reboot, on_is_stable, off_is_reboot, off_is_stable)
    #print(logtype)
    if logtype == "ON":
      if on_is_reboot == 1:
        try:
          listed[end].split(",")[4]        
        except IndexError:
          listed[end]=listed[end]+","
        #print(listed[end])
        for x in range(0,len(listed[end].split(","))):
          #print(listed[end].split(",")[x])
          if x ==4 and listed[end].split(",")[4]=="":
            str_replaced+="onis_reboot,"
          else:
            str_replaced+=listed[end].split(",")[x]+","
        listed[end]=str_replaced
        #print("1:"+listed[end])
      if on_is_stable == 1:
        try:
          listed[end].split(",")[4]        
        except IndexError:
          listed[end]=listed[end]+","
        #print(listed[end])
        for x in range(0,len(listed[end].split(","))):
          #print(listed[end].split(",")[x])
          if x ==4 and listed[end].split(",")[4]=="":
            str_replaced+="onis_stable,"
          else:
            str_replaced+=listed[end].split(",")[x]+","
        listed[end]=str_replaced
        #print("2"+listed[end])
    elif logtype == "OFF":
      if off_is_reboot == 1:
        try:
          listed[end].split(",")[4]        
        except IndexError:
          listed[end]=listed[end]+","
        try:
          listed[end].split(",")[5]        
        except IndexError:
          listed[end]=listed[end]+","
        #print(listed[end])
        for x in range(0,len(listed[end].split(","))):
          #print(listed[end].split(",")[x])
          if x ==5 and listed[end].split(",")[5]=="":
            str_replaced+="offis_reboot"
          else:
            str_replaced+=listed[end].split(",")[x]+","
        listed[end]=str_replaced
        #print("3"+listed[end])
      if off_is_stable == 1:
        try:
          listed[end].split(",")[4]        
        except IndexError:
          listed[end]=listed[end]+","
        try:
          listed[end].split(",")[5]        
        except IndexError:
          listed[end]=listed[end]+","
        #print(listed[end])
        for x in range(0,len(listed[end].split(","))):
          #print("@@@"+listed[end].split(",")[x])
          if x ==5 and listed[end].split(",")[5]=="":
            str_replaced+="offis_stable"
          else:
            str_replaced+=listed[end].split(",")[x]+","
        listed[end]=str_replaced
        #print("4"+listed[end])          
#-------------------------------
    elif logtype == "ONOFF":
      #print(on_is_reboot, on_is_stable, off_is_reboot, off_is_stable)
      if on_is_reboot == 1:
        try:
          listed[end].split(",")[4]        
        except IndexError:
          listed[end]=listed[end]+","
        #print(listed[end])
        for x in range(0,len(listed[end].split(","))):
          #print(listed[end].split(",")[x])
          if x ==4 and listed[end].split(",")[4]=="":
            str_replaced+="onis_reboot,"
          else:
            str_replaced+=listed[end].split(",")[x]+","
        listed[end]=str_replaced
        #print("5:"+listed[end])      
      if on_is_stable == 1:
        try:
          listed[end].split(",")[4]        
        except IndexError:
          listed[end]=listed[end]+","
        #print(listed[end])
        for x in range(0,len(listed[end].split(","))):
          #print(listed[end].split(",")[x])
          if x ==4 and listed[end].split(",")[4]=="":
            str_replaced+="onis_stable,"
          else:
            str_replaced+=listed[end].split(",")[x]+","
        listed[end]=str_replaced
        #print("6"+listed[end])
      str_replaced=""
      if off_is_reboot == 1:
        try:
          listed[end].split(",")[4]        
        except IndexError:
          listed[end]=listed[end]+","
        try:
          listed[end].split(",")[5]        
        except IndexError:
          listed[end]=listed[end]+","
        for x in range(0,len(listed[end].split(","))):
          #print(listed[end].split(",")[x])
          if x ==5 and listed[end].split(",")[5]=="":
            str_replaced+="offis_reboot"
          else:
            str_replaced+=listed[end].split(",")[x]+","
        listed[end]=str_replaced
        #print("7"+listed[end])
      if off_is_stable == 1:
        try:
          listed[end].split(",")[4]        
        except IndexError:
          listed[end]=listed[end]+","
        try:
          listed[end].split(",")[5]        
        except IndexError:
          listed[end]=listed[end]+","
        #print("@@@@@@"+listed[end])
        for x in range(0,len(listed[end].split(","))):
          #print("@@@"+listed[end].split(",")[x])
          if x ==5 and listed[end].split(",")[5]=="":
            str_replaced+="offis_stable"
          else:
            str_replaced+=listed[end].split(",")[x]+","
        listed[end]=str_replaced
        #print("8"+listed[end]) 
      else:
        print("nothing match!!")
    else:
      print("logtype mismatch!!")
#-------------------------------    
    out_f.write(listed[end]+"\n")
  
def reducelogs (list_aft_reduced, out_f, logtype, logoffstart, end, logondatacnt, logoffdatacnt):
  if logtype == "ON":
    out_f.write("=====Relay Noise ON====="+"\n")
    for RLON in range(int(logoffstart)-int(logondatacnt),logoffstart):
      print("@@"+"RLON="+str(RLON)+":"+listed[RLON])
      print("##"+str(logoffstart), str(end), str(logondatacnt), str(logoffdatacnt))
      out_f.write(list_aft_reduced[RLON]+"\n")
  elif logtype == "OFF":
    out_f.write("=====Relay Noise OFF====="+"\n")
    for RLOFF in range(int(end)-int(logoffdatacnt),end):
      #print("@@"+listed[x])
      out_f.write(list_aft_reduced[RLOFF]+"\n")        

def check_kernel_panic_onoff (listed, logoncount, logoffcount, list_start, end):
  logonstart=int(list_start)+1
  logoffstart=int(logonstart)+int(logoncount)+1
  for x in range(int(logonstart),int(logoffstart)):
    if any( a in listed[x] for a in kernel_panic_patterns):
      listed[end]=listed[end]+",Kernel panic"
      break
  for y in range(int(logoffstart),int(end)):
    if any( b in listed[y] for b in kernel_panic_patterns):
      listed[end]=listed[end]+",,Kernel panic"
      break

def check_kernel_panic_on (listed, logoncount, logoffcount, list_start, end):
  logonstart=int(list_start)+1
  for v in range(int(logonstart),int(end)):
    if any( a in listed[v] for a in kernel_panic_patterns):
      listed[end]=listed[end]+",Kernel panic,Unknown"
      break
  
def check_kernel_panic_off (listed, logoncount, logoffcount, list_start, end):
  logoffstart=int(list_start)+int(logoncount)+1
  for z in range(int(logoffstart),int(end)):
    if any( a in listed[z] for a in kernel_panic_patterns):    
      listed[end]=listed[end]+",Unknown,Kernel panic"
      break

def check_status_last5logs (listed, out_f, logtype, logoffstart, end, logondatacnt, logoffdatacnt):
    on_is_reboot=0
    on_is_stable=0
    off_is_reboot=0
    off_is_stable=0
    if logtype == "ON":
      for RLON in range(int(logoffstart)-int(logondatacnt),logoffstart):
        if listed[RLON].split(" ")[6] in is_reboot_patterns:
          on_is_reboot=1
          replace_element(listed, out_f, end, logtype, on_is_reboot, on_is_stable, off_is_reboot, off_is_stable)
          break
        elif listed[RLON].split(" ")[6] in is_stable_patterns:
          on_is_stable=1
          replace_element(listed, out_f, end, logtype, on_is_reboot, on_is_stable, off_is_reboot, off_is_stable)
          break
    elif logtype == "OFF":  
      for RLOFF in range(int(end)-int(logoffdatacnt),end):
        if listed[RLOFF].split(" ")[6] in is_reboot_patterns:
          off_is_reboot=1
          replace_element(listed, out_f, end, logtype, on_is_reboot, on_is_stable, off_is_reboot, off_is_stable)
          break
        elif listed[RLOFF].split(" ")[6] in is_stable_patterns:
          off_is_stable=1
          replace_element(listed, out_f, end, logtype, on_is_reboot, on_is_stable, off_is_reboot, off_is_stable)
          break
    elif logtype == "ONOFF":
      for RLON in range(int(logoffstart)-int(logondatacnt),logoffstart):
        if listed[RLON].split(" ")[6] in is_reboot_patterns:
          on_is_reboot=1
          break
        elif listed[RLON].split(" ")[6] in is_stable_patterns:
          on_is_stable=1
          break
      for RLOFF in range(int(end)-int(logoffdatacnt),end):
        if listed[RLOFF].split(" ")[6] in is_reboot_patterns:
          off_is_reboot=1
          break
        elif listed[RLOFF].split(" ")[6] in is_stable_patterns:
          off_is_stable=1
          break
      replace_element(listed, out_f, end, "ONOFF", on_is_reboot, on_is_stable, off_is_reboot, off_is_stable)
      
#main function        
list_start=1
list_aft_reduced=listed
listed[0]=listed[0]+",Onstatus,Offstatus"
with open("T[192.168.1.48]dbg_classified.csv", 'w') as out_f:
    out_f.write(list_aft_reduced[0]+"\n")
    while list_start < len(listed):
        try:
            logcount=listed[list_start].split(",")[5]
        except IndexError:
            logcount=0
        if int(logcount) >0 :
            end=list_start+int(logcount)+3
            op=0
            while op ==0:
                try:
                    listed[end].split(",")
                    if listed[end].split(",")[0]!="\"":
                        end=end-1
                    else:
                        op=1
                except IndexError:
                    end=end-1
            print("end="+str(end))
            logoncount=listed[end].split(",")[2]
            logoffcount=listed[end].split(",")[3]
#-----------------Write first line each round-----------------------------------            
            out_f.write(listed[list_start]+"\n")
            if int(logoncount) < 5:
                logondatacnt=logoncount
            else:
                logondatacnt=5
            if int(logoffcount) < 5:
                logoffdatacnt=logoffcount
            else:
                logoffdatacnt=5
            if int(logoncount)>0 and int(logoffcount)>0:
                logonstart=int(list_start)+1
                logoffstart=int(logonstart)+int(logoncount)+1
                check_kernel_panic_onoff (listed, logoncount, logoffcount, list_start, end)
#-----------------Relay noise On Write last 5 logs------------------------------
                reducelogs (list_aft_reduced, out_f, "ON", logoffstart, end, logondatacnt, logoffdatacnt)
#-----------------Relay noise Off Write last 5 logs-----------------------------
                reducelogs (list_aft_reduced, out_f, "OFF", logoffstart, end, logondatacnt, logoffdatacnt)
                check_status_last5logs (listed, out_f, "ONOFF", logoffstart, end, logondatacnt, logoffdatacnt)
            elif int(logoncount)==0 and int(logoffcount)>0:
                logoffstart=int(list_start)+int(logoncount)+1
                check_kernel_panic_off (listed, logoncount, logoffcount, list_start, end)
#-----------------Relay noise Off Write last 5 logs-----------------------------
                reducelogs (list_aft_reduced, out_f, "OFF", logoffstart, end, logondatacnt, logoffdatacnt)            
                check_status_last5logs (listed, out_f, "OFF", logoffstart, end, logondatacnt, logoffdatacnt)
            elif int(logoncount)>0 and int(logoffcount)==0:
                #logonstart=int(list_start)+1
                logoffstart=end
                check_kernel_panic_on (listed, logoncount, logoffcount, list_start, end)
#-----------------Relay noise On Write last 5 logs------------------------------
                reducelogs (list_aft_reduced, out_f, "ON", logoffstart, end, logondatacnt, logoffdatacnt)            
                check_status_last5logs (listed, out_f, "ON", logoffstart, end, logondatacnt, logoffdatacnt)
#-----------------Write last line each round------------------------------------
            list_start=end+1
        else:
            end=list_start+int(logcount)+1
            check_status_last5logs (listed, out_f, "ON", logoffstart, end, logondatacnt, logoffdatacnt)
#-----------------Write last line each round------------------------------------
            list_start=end+1