import subprocess ,re
def get_mac(ip):
    # this function for get mac using specific ip , by arp table
    mac = ""
    # ping ths ip to store it into arp table
    p=subprocess.Popen("ping "+ip,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    # extract arp table using command line for windows , arp -a
    s=subprocess.Popen("arp -a",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    arp = str(s.stdout.read())
    # split data using expression \\r\\n to get it line by line
    arp2 =  arp.split("\\r\\n")
    for i in arp2 :
        if str(ip) in str(i) and "Interface" not in str(i):
            # now using regular expression to get mac address for ip
            mac=re.findall(r"([\da-f]{2}(?:[-:][\da-f]{2}){5})", str(i))

            break
    return mac    # finally return man
