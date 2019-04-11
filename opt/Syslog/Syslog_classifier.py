
# coding: utf-8

# In[244]:


#with open("[192.168.1.129].csv") as file:
#    for line in file:
#        print(line)


# In[245]:


listed=[]
import sys
filename=sys.argv[1]
#print(filename)
with open(filename+".csv") as file:
    for line in file:
        line = line.strip()
        if len(line)!=0:
            listed.append(line)
        
#    print(len(listed))
#    print(listed)


# In[246]:


list_start=1
listed[0]=listed[0]+",Onstatus,Offstatus"
with open(filename+"_classified.csv", 'w') as out_f:
    while list_start < len(listed):
        try:
            logcount=listed[list_start].split(",")[5]
        except IndexError:
            logcount=0
        if int(logcount) > 0:
            end=list_start+int(logcount)+3
            op=0
            while op !=1:
                try:
                    listed[end].split(",")
                    if listed[end].split(",")[0]!="\"":
                        end=end-1
                except IndexError:
                    end=end-1
                else:
                    op=1
            logoncount=listed[end].split(",")[2]
            logoffcount=listed[end].split(",")[3]
            kernel_panic=0
            if int(logoncount)>0 and int(logoffcount)>0:
                logonstart=int(list_start)+1
                logoffstart=int(logonstart)+int(logoncount)+1
                for x in range(int(logonstart),int(logoffstart)):
                    if "Backtrace" in listed[x]:
                        listed[end]=listed[end]+",Kernel panic"
                        break
                for y in range(int(logoffstart),int(end)):
                    if "Backtrace" in listed[y]:
                        listed[end]=listed[end]+",,Kernel panic"
                        break
                    elif any(c in listed[y] for c in ("[SYSTEM] add user: manager", "network: Set SYSLOG server to 192.168.1.55 by DHCP option 7","[SYSTEM] Scanning Log ... Done (OK)"," [NETWROK] wan (929): udhcpc: lease of 192.168.1.129 obtained, lease time 120")):
                        listed[end]=listed[end]+",,Recovered"
                        break
            elif int(logoncount)==0 and int(logoffcount)>0:
                logoffstart=int(list_start)+int(logoncount)+1
                for z in range(int(logoffstart),int(end)):
                    if "Backtrace" in listed[z]:
                        listed[end]=listed[end]+",Unknown,Kernel panic"
                        break
                    elif any(c in listed[z] for c in ("[SYSTEM] add user: manager", "network: Set SYSLOG server to 192.168.1.55 by DHCP option 7","[SYSTEM] Scanning Log ... Done (OK)"," [NETWROK] wan (929): udhcpc: lease of 192.168.1.129 obtained, lease time 120")):
                        listed[end]=listed[end]+",Unknown,Recovered"
                        break
            elif int(logoncount)>0 and int(logoffcount)==0: 
                logonstart=int(list_start)+1
                for v in range(int(logonstart),int(end)):
                    if "Backtrace" in listed[v]:
                        listed[end]=listed[end]+",Kernel panic,Unknown"
            list_start=end+1
        else:
            end=list_start+int(logcount)+1
            listed[end]=listed[end]+",Unknown,Unknown"
            list_start=end+1
    for cnt in range(0,len(listed)-1):
        out_f.write(listed[cnt]+"\n")
    

    


# In[247]:


#print(listed)

