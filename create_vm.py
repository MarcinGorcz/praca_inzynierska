import manage_users
from make_backup_and_create_image import run_command

#TODO: Skrypt ktory odpala VNC, musi odpalac sie po utworzeniu VM ( wejsc tam i wlaczyc przez ssh vncserver )

def validate_user(password, login):
    man_users = manage_users.manage_users()
    users = man_users.json_to_dict()
    if password in users:
        if users[password]["login"] == login:
            return True
        else:
            return False
    else:
        return False

def startup_script(password):
    man_users = manage_users.manage_users()
    users = man_users.json_to_dict()
    username = users[password]["login"]
    passwd = users[password]["password"]
    bash_script = "#! /bin/bash"
    bash_script += "\n"
    #bash_script += "sudo su -"
    bash_script += "adduser --disabled-password --gecos \"\" " + username
    bash_script += "\n"
    bash_script += "echo -e \"" + passwd + "\\n" + passwd +"\" | passwd " + username
    bash_script += "\n"
    bash_script += "sed -i '/^PasswordAuthentication/s/no/yes/' /etc/ssh/sshd_config"
    bash_script += "\n"
    bash_script += "service ssh restart"
    bash_script += "\n"
    bash_script += "sudo apt update"
    bash_script += "\n"
    bash_script += "sudo apt install tightvncserver"
    bash_script += "\n"
    bash_script += "echo -e \"" + passwd + "\\n" + passwd + "\" | vncpasswd"
    bash_script += "\n"
    bash_script += "vncserver"
    bash_script += "\n"

    filename = username + "-startup.sh"
    f = open(filename, "w")
    f.write(bash_script)
    f.close()
    return bash_script

def create_vm(password):
    startup_script(password)
    man_users = manage_users.manage_users()
    users = man_users.json_to_dict()
    gcloud_create_instance = "gcloud compute instances create "
    gcloud_create_instance += users[password]["login"]
    gcloud_create_instance += " --zone=europe-west6-a"
    gcloud_create_instance += " --machine-type=" + users[password]["vm_type"]
    gcloud_create_instance += " --image=" + users[password]["image_name"]
    gcloud_create_instance += " --metadata-from-file startup-script=" + users[password]["login"] + "-startup.sh"

    import subprocess
    process = subprocess.Popen(gcloud_create_instance.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    toReturn = ""
    if output:
        toReturn = "VM creation started:\n"
        toReturn += str(output) + "\n"
    return toReturn


if __name__ == '__main__':
    #startup_script("1nyM2Dmc")
    #create_vm("1nyM2Dmc")
    print(validate_user("1nyM2Dmc", "user3"))