import manage_users
from make_backup_and_create_image import run_command

man_users = manage_users.manage_users()
users = man_users.json_to_dict()

def add_user(users):
    username