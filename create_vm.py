import manage_users
from make_backup_and_create_image import run_command
man_users = manage_users.manage_users()
users = man_users.json_to_dict()

def validate_user(password):
    if password in users:
        return True
    else:
        return False

def startup_script(password):
    username = users[password]["login"]
    passwd = users[password]["password"]
    bash_script = "\'#! /bin/bash"
    bash_script += "sudo su -"
    bash_script += "adduser --disabled-password --gecos \"\" " + username
    bash_script += "echo -e \"" + passwd + "\\n" + passwd +"\" | passwd user2"
    bash_script += "sed - i '/^PasswordAuthentication/s/no/yes/' / etc / ssh / sshd_config"
    bash_script += "service ssh restart"
    bash_script += "apt update"
    bash_script += "apt install tightvncserver"
    bash_script += "echo -e \"" + passwd + "/n" + passwd + "\" | vncpasswd"
    bash_script += "vncserver\'"
    return bash_script

def create_vm(password):
    gcloud_create_instance = "gcloud compute instances create "
    gcloud_create_instance += users[password]["login"]
    gcloud_create_instance += " --zone=europe-west6-a"
    gcloud_create_instance += " --machine-type=" + users[password]["vm_type"]
    gcloud_create_instance += " --image=" + users[password]["image_name"]

    import subprocess
    process = subprocess.Popen(gcloud_create_instance.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    toReturn = ""
    if output:
        toReturn = "VM creation started:\n"
        toReturn += str(output) + "\n"
    return toReturn


if __name__ == '__main__':
    output = create_vm("passphrase")
    print(output)
    #bash_script = startup_script("passphrase")
    #print(bash_script)
