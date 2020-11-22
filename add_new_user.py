import secrets
import string
import manage_users

man_users = manage_users.manage_users()
users = man_users.json_to_dict()


def generate_passphrase():
    alphabet = string.ascii_letters + string.digits
    passphrase = ''.join(secrets.choice(alphabet) for i in range(8))
    return passphrase


def add_new_user_to_json():
    passphrase = generate_passphrase()
    while passphrase in users:
        passphrase = generate_passphrase()
    config = {
        "login": "user",
        "password": generate_passphrase(),
        "vm_type": "n1-standard-1",
        "image_name": ""}
    users[passphrase] = config
    man_users.dict_to_json(users)
    print(users[passphrase])


def add_new_user_to_server():
    pass

if __name__ == '__main__':
    pass