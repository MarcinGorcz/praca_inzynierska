import manage_users
from make_backup_and_create_image import run_command

#run as root


def enable_shh_pass():
    try:
        enable_ssh_password_authentication_sed_cmd = "sed - i '/^PasswordAuthentication/s/no/yes/' / etc / ssh / sshd_config"
        reboot_ssh_service = "sudo service ssh restart"
        run_command(enable_ssh_password_authentication_sed_cmd)
        run_command(reboot_ssh_service)
        print("PasswordAuthentication is enabled")
    except Exception:
        print("PasswordAuthentication enabling failed")


def run_watchers_for_all_users():
    man_users = manage_users.manage_users()
    users = man_users.json_to_dict()
    for user in users:
        run_command("sudo watcher.sh " + users[user]["login"])