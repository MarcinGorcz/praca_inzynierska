import manage_users
from pathlib import Path
import sys

man_users = manage_users.manage_users()
users = man_users.json_to_dict()
day = ""
format = "vmdk"


#TODO: Przetestowac tworzenie dla user4 ( fizyczny laptop z Ubuntu )
#TODO: Przetestowac usuwanie plikow
#TODO: Przetestowac na innym uzytkowniku niz Ubuntu 16.04 !!!
#TODO: Czy watcher.sh nie loopuje sie po wypadkowaniu pliku image? Bo w sumie tworzy sie wtedy nowy plik? nowy folder potrzebny?
#TODO: WYDAJE MI SIE ZE WATCHER PRZY PRZERWANIU PRZESYLANIA WYKRYWA ZE PLIK JEST DO ROZPAKOWANIA I PROBUJE ODPALIC SKRYPT ALE MU SIE NIE UDAJE
def cleanup_files(path):
    remove_cmd = "rm " + path
    print(remove_cmd)
    run_command(remove_cmd)


def run_command_shell(command):
    import subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE,shell=True)
    output, error = process.communicate()
    if output:
        print(output)
    if error:
        print(error)
        raise Exception("Sorry, no numbers below zero")


def run_command(command):
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if output:
        print(output)
    if error:
        print(error)


#Done locally on client:
#ssh ubuntu@pseudofizycznyuzytkownik "sudo dd if=/dev/sda | gzip -1 -" | dd of=image.gz
#def create_dd_copy(password):
#    create_dd_image = "ssh marcin_tomasz_stanislaw_gorczyca@34.65.5.171 "
#    create_dd_image += "\"sudo dd if=/dev/sda\" | dd of=/home/marcin_tomasz_stanislaw_gorczyca/" + users[password][0] + "/" + users[password][0] +".img"
#    print(create_dd_image)
#    run_command_shell(create_dd_image)


# qemu-img convert -f raw -O vmdk sda.img sda.vmdk
def create_vmdk(password):
    img_path_string = "/home/" + users[password]["login"] + "/image/unziped_image"
    img_path = Path(img_path_string)
    if img_path.is_file():
        create_vmdk_cmd = "qemu-img convert -f raw -O " + format + " "
        create_vmdk_cmd += img_path_string + " "
        create_vmdk_cmd += "/home/" + users[password]["login"] + "/" + format + "/"
        create_vmdk_cmd += users[password]["login"] + "." + format
        print(create_vmdk_cmd)
        run_command(create_vmdk_cmd)
        cleanup_files(img_path_string)
    else:
        print("VMDK creation failed\n")
        print("No img file \n")


#gsutil cp imagefrompseudo.tar.gz  gs://linux-image-bucket/frompseudouser/compressed-image.tar.gz
def move_to_storage(password):
    vmdk_path_string = "/home/" + users[password]["login"] + "/" + format + "/" + users[password]["login"]  + "." + format
    vmdk_path = Path(vmdk_path_string)
    print(vmdk_path_string)
    if vmdk_path.is_file():
        import datetime
        x = datetime.datetime.now()
        day = x.strftime("%d") + x.strftime("%m") + x.strftime("%y")
        move_to_bucket = "gsutil cp /home/" + users[password]["login"]
        move_to_bucket += "/" + format + "/" + users[password]["login"] + "." + format
        move_to_bucket += " gs://linux-image-bucket/" + users[password]["login"] + "/" + users[password]["login"] + "-" + day + "." + format
        print(move_to_bucket)
        run_command(move_to_bucket)
        cleanup_files(vmdk_path_string)
        return day
    else:
        print("Image creation failed\n")
        print("No vmdk file \n")


def update_users(password, image_name):
    users[password]["image_name"] = image_name
    man_users.dict_to_json(users)


#gcloud compute images import image-name \
#--source-file source-file \
#--os os
def create_image(password,creationday):
    image_name = users[password]["login"] + "-" + creationday
    create_image_cmd = "gcloud compute images import " + image_name + " --source-file "
    create_image_cmd += "gs://linux-image-bucket/" + users[password]["login"] + "/" + users[password]["login"] + "-" + creationday + "." + format
    create_image_cmd += " --os ubuntu-1604"
    print(create_image_cmd)
    run_command(create_image_cmd)
    update_users(password, image_name)



def get_passphrase_from_username(login):
    for user in users:
        if users[user]["login"] == login:
            return user


if __name__ == '__main__':
    login = sys.argv[1]
    if not login:
        sys.exit("User not specified")
    passphrase = get_passphrase_from_username(login)
    create_vmdk(passphrase)
    day = move_to_storage(passphrase)
    create_image(passphrase, day)
