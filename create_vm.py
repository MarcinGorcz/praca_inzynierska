import manage_users

man_users = manage_users.manage_users()
users = man_users.json_to_dict()

def validate_user(password):
    if password in users:
        return True
    else:
        return False


def create_vm(password):
    gcloud_create_instance = "gcloud compute instances create "
    gcloud_create_instance += users[password][0]
    gcloud_create_instance += " --zone=" + users[password][1]
    gcloud_create_instance += " --machine-type=" + users[password][2]
    gcloud_create_instance += " --image=" + users[password][3]

    import subprocess
    process = subprocess.Popen(gcloud_create_instance.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    toReturn = ""
    if output:
        toReturn = "VM creation started:\n"
        toReturn += str(output) + "\n"
    return toReturn


if __name__ == '__main__':
    output = create_vm("LINUXUSER0001")
    print(output)
