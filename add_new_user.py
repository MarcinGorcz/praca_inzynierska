import secrets
import string
import manage_users
import sys
from make_backup_and_create_image import run_command,run_command_shell

man_users = manage_users.manage_users()
users = man_users.json_to_dict()

default_vm = "n1-standard-1"


def generate_passphrase():
    alphabet = string.ascii_letters + string.digits
    passphrase = ''.join(secrets.choice(alphabet) for i in range(8))
    return passphrase


def add_new_user_to_json(newuser):
    for user in users:
        if users[user]["login"] == newuser:
            sys.exit("That user already exists!")

    passphrase = generate_passphrase()
    while passphrase in users:
        passphrase = generate_passphrase()

    config = {
        "login": newuser,
        "password": generate_passphrase(),
        "vm_type": default_vm,
        "image_name": " "}

    users[passphrase] = config
    man_users.dict_to_json(users)
    print("User config created:")
    print("Passphrase: " + passphrase)
    print("login: " + users[passphrase]["login"])
    print("password: " + users[passphrase]["password"])
    print("vm set to default: " + users[passphrase]["vm_type"])
    print("image is not set yet: " + users[passphrase]["image_name"])
    return passphrase

#this is needed
def add_new_user_to_server(user, pass_phrase):
    add_new_user_cmd = "adduser --disabled-password --gecos \"\" " + user
    run_command(add_new_user_cmd)
    #To nizej nie dziala...
    add_password = 'echo -e \"' + users[pass_phrase]["password"] + '\\n' + users[pass_phrase]["password"] + '\" | ' \
                                                                                                           'passwd ' \
                   + user
    run_command_shell(add_password)

#Not needed because directories in gs are abstract
def create_new_directory_in_bucket():
    new_dir_in_bucket_cmd =""
    run_command(new_dir_in_bucket_cmd)


def start_watcher_for_incoming_images(user):
    run_command("/home/marcin_tomasz_stanislaw_gorczyca/Scripts/watcher.sh " + user + " &")

if __name__ == '__main__':
    new_user = sys.argv[1]
    if not new_user:
        sys.exit("User not specified")
    passphrase = add_new_user_to_json(new_user)
    add_new_user_to_server(new_user, passphrase)
    #start_watcher_for_incoming_images(new_user)