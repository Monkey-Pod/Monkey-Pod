import subprocess

def telnetScenario(ip):
    try:
        args = ['nmap','--script','telnet-encryption',ip,'-p','23']
        res = subprocess.check_output(args)
    except:
        print("Error")

    res = res.decode('utf-8')
    
    nextGet = 0
    for i in res.splitlines():
        if(nextGet ==1):
            print(i)
            nextGet = 0
        if ("telnet-encryption" in i):
            print(i)
            nextGet = 1    

    try:
        args = ['nmap','-sV','-sC',ip,'-p','22']
        res = subprocess.check_output(args)
    except:
        print("Error")

    res = res.decode('utf-8')
    
    for i in res.splitlines():
        if ("Server supports SSHv1" in i):
            print("|_ssh supports version 1.0")
    else:
        print("|_ssh dose not support version 1.x")

#telnetSenario()
