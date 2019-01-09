import subprocess
def is_live( ip):
    global result_data
    result_data = []
    CMD = subprocess.Popen("ping -n 1 " + ip, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdin=subprocess.PIPE)

    reply = CMD.stdout.read()
    print(reply)
    if "TTL" in str(reply):
        result = True
    else:
        result = False
    result_data.append(result)
    return result_data
