#!/usr/bin/env python3
import os
import re
import sys
import subprocess
from datetime import datetime
#import searchCVE
#from searchCVE import searchCVE 
#from Scenario.searchCVE import searchCVE

# ipaddr = "192.168.22.137"
ipaddr = sys.argv[1]
nowdate = datetime.now()
nowdate_f = nowdate.strftime("%Y%m%d_%H%M")


### nmap nse
def run_nmap_scripts(ip):
    print("### Start Nmap NSE. ###")
    port1 = "80"
    port2 = "81"
    port3 = "443"
    ports = [port1,port2,port3]
    script1 = "http-apache-server-status"
    script2 = "http-auth-finder"
    nse1 = f'nmap --script "{script1}" -p "{port1}","{port2}","{port3}" "{ip}"| egrep "\"{port1}\"|\"{port2}\"|\"{port3}\"|^\|" | tee nse1_"{ nowdate_f }".txt'
    nse2 = f'nmap --script "{script2}" -p "{port1}","{port2}","{port3}" "{ip}"| egrep "\"{port1}\"|\"{port2}\"|\"{port3}\"|^\|" | tee nse2_"{ nowdate_f }".txt'
    print(f"# Start Nmap NSE: {script1}")
    os.system(nse1)
    print(f"# Finish NSE: {script1}")
    print()
    print(f"# Start Nmap NSE: {script2}")
    os.system(nse2)
    print(f"# Finish NSE: {script2}")
    print("### Nmap NES Done. ###")



### whatweb ( stealethy mode )
def run_whatweb(ip):
    print("### Start Whatweb. ###")
    whatweb1 = f'whatweb -a 1 "{ip}" | sed "s/, /\\n  /g" | tee whatweb-a1_"{ nowdate_f }".txt'
    print("# Start Whatweb stealthy mode")
    os.system(whatweb1)
    print("# Finish Whatweb stealthy mode")
    print()
    whatweb2 = f'whatweb -a 3 "{ip}" | sed "s/, /\\n  /g" | tee whatweb-a3_"{ nowdate_f }".txt'
    print("# Start whatweb aggresive mode")
    os.system(whatweb2)
    print("# Finish whatweb aggressive mode")
    print("### Whatweb Done.")

### Nikto
def run_nikto(ip):
    print("### Start Nikto. ###")

    print("# Start nikto : 80/http")
    nc80  = f'nc -z -w2 "{ip}" 80 && nikto -h http://"{ip}" | egrep "^\+" | tee nikto-80_"{ nowdate_f }".txt'
    os.system(nc80)
    print()

    print("# Start nikto : 81/http")
    nc81  = f'nc -z -w2 "{ip}" 81 && nikto -h http://"{ip}":81 | egrep "^\+" | tee nikto-81_"{ nowdate_f }".txt'
    os.system(nc81)
    print()

    print("# Start nikto : 443/https")
    nc443  = f'nc -z -w2 "{ip}" 443 && nikto -h https://"{ip}" | egrep "^\+" | tee nikto-443_"{ nowdate_f }".txt'
    os.system(nc443)
    print()
    print("### Nikto Done.")

###Nuclei
def run_nuclei(ip):
    print("### Start Nuclei.###")
    cmd = 'nuclei -ut  >/dev/null 2>&1'
    cmd1 =  f'nc -z -w2 "{ip}" 80  && nuclei -target  http://"{ip}"    2> /dev/null | egrep -i "cve-20|cve-19|high|medium|criticalwarn|detect" | tee nuclei-80_"{ nowdate_f }".txt'
    cmd2 =  f'nc -z -w2 "{ip}" 81  && nuclei -target  http://"{ip}":81 2> /dev/null | egrep -i "cve-20|cve-19|high|medium|criticalwarn|detect" | tee nuclei-81_"{ nowdate_f }".txt'
    cmd3 =  f'nc -z -w2 "{ip}" 443 && nuclei -target  https://"{ip}"   2> /dev/null | egrep -i "cve-20|cve-19|high|medium|criticalwarn|detect" | tee nuclei-443_"{ nowdate_f }".txt'
    os.system(cmd)
    print("# Start nuclei: 80/http")
    os.system(cmd1)
    print("# Start nuclei: 81/http")
    os.system(cmd2)
    print("# Start nuclei: 443/https")
    os.system(cmd3)
    print("### Nuclei Done.")
    print()


###Dirsearch
# dirsearch -u http://$ip
def run_dirsearch(ip):
    print("### Start Dirsearch.###")
    cmd1 =  f'dirsearch.py -u  http://"{ip}"    '#| tee dirsearch-80_"{ nowdate_f }".txt'
    cmd2 =  f'dirsearch.py -u  http://"{ip}":81 '#| tee dirsearch-81_"{ nowdate_f }".txt'
    cmd3 =  f'dirsearch.py -u  https://"{ip}"   '#| tee dirsearch-443_"{ nowdate_f }".txt'
    print("# Start dirsearch: 80/http")
    os.system(cmd1)
    print("# Start dirsearch: 81/http")
    os.system(cmd2)
    print("# Start dirsearch: 443/https")
    os.system(cmd3)
    print("### Dirsearch Done.")
    print()

### find cve
def run_findcve():
    nikto_command = f'grep -i cve- nikto-80_"{ nowdate_f }".txt'
    #nikto_command = f'grep -i cve- nikto-80_20231003_1939.txt'
    nuclei_command  = f'grep -i cve- nuclei-80_"{ nowdate_f }".txt'
    #nuclei_command  = f'grep -i cve- nuclei-80_20231003_1939.txt'
    nikto_output = subprocess.check_output(nikto_command, shell=True, text=True)
    nuclei_output = subprocess.check_output(nuclei_command, shell=True, text=True)
    outputs = nikto_output + nuclei_output
    pattern = r"CVE-\d{4}-\d{4,5}"
    matches = re.findall(pattern, outputs)
    if matches:
        #print( matches )
        cve = matches
        #searchCVE(cve)
        return cve

    else:
        print("CVE ID not found.")
        return 1


def httpScenario():
    print("""
    #########################################################
      This script will do follows;
        1. Nmap NSE
          1-1. http-apache-server-status [ few seconds ]
          1-2. http-auth-finder          [ few seconds ]
        2. Whatweb 
          2-1. whatweb stealthy mode     [ few seconds ]
          2-2. whatweb aggressive mode   [ few seconds ]
        3. Nikto                         [ 1~2 minutes ]
        4. Nuclei                        [ few minutes ]
        5. Dirsearch                     [ few minutes ]  
    ########################################################
        """)

    run_nmap_scripts(ipaddr)
    print()
    run_whatweb(ipaddr)
    print()
    run_nikto(ipaddr)
    print()
    run_nuclei(ipaddr)
    print()
    run_dirsearch(ipaddr)
    print()
    run_findcve()
