login = "user1"
password = ""
ip = "34.65.196.190"


#Please install sshpass!
#sudo apt-get install sshpass

def run_command_shell(command):
    import subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE,shell=True)
    output, error = process.communicate()
    if output:
        print(output)
    if error:
        print(error)

def dd_to_server():
    dd_cmd = "dd if=/dev/sda | gzip -1 - | sshpass -p "+password+" ssh "+login+"@"+ip+"34.65.196.190"" dd of=image.gz"


