import manage_users
from pathlib import Path

def get_tl_type():
    #TODO
    #Script from pycharm
    pass

man_users = manage_users.manage_users()
users = man_users.json_to_dict()

def cleanup_files(path):
    remove_cmd = "rm " + path
    run_command(remove_cmd)

def run_command_shell(command):
    import subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE,shell=True)
    output, error = process.communicate()
    if output:
        print(output)
    if error:
        print(error)

def run_command(command):
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if output:
        print(output)
    if error:
        print(error)

#ssh ubuntu@pseudofizycznyuzytkownik "sudo dd if=/dev/sda | gzip -1 -" | dd of=image.gz
def create_dd_copy(password):
    create_dd_image = "ssh marcin_tomasz_stanislaw_gorczyca@34.65.5.171 "
    create_dd_image += "\"sudo dd if=/dev/sda\" | dd of=/home/marcin_tomasz_stanislaw_gorczyca/" + users[password][0] + "/" + users[password][0] +".img"
    print(create_dd_image)
    run_command_shell(create_dd_image)

# qemu-img convert -f raw -O vmdk sda.img sda.vmdk
def create_vmdk(password):
    img_path = Path("/home/marcin_tomasz_stanislaw_gorczyca/" + users[password][0] + "/" + users[password][0] + ".img")
    if img_path.is_file():
        create_vmdk =  "qemu-img convert -f raw -O vmdk "
        create_vmdk += "/home/marcin_tomasz_stanislaw_gorczyca/" + users[password][0] + "/"
        create_vmdk +=  users[password][0] + ".img "
        create_vmdk += "/home/marcin_tomasz_stanislaw_gorczyca/" + users[password][0] + "/"
        create_vmdk += users[password][0] + ".vdmk"
        print(create_vmdk)
        run_command(create_vmdk)
        cleanup_files(img_path)
    else:
        print("VMDK creation failed\n")
        print("No img file \n")

#gsutil cp imagefrompseudo.tar.gz  gs://linux-image-bucket/frompseudouser/compressed-image.tar.gz
def move_to_storage(password):
    vdmk_path = Path("/home/marcin_tomasz_stanislaw_gorczyca/" + users[password][0] + "/" + users[password][0] + ".vdmk")
    if vdmk_path.is_file():
        import subprocess
        move_to_bucket = "gsutil cp /home/marcin_tomasz_stanislaw_gorczyca/" + users[password][0]
        move_to_bucket += "/" + users[password][0] + ".vdmk "
        move_to_bucket += "gs://linux-image-bucket/" + users[password][0] + "/" + users[password][0] + ".vdmk"
        print(move_to_bucket)
        run_command(move_to_bucket)
        cleanup_files(vdmk_path)
    else:
        print("Image creation failed\n")
        print("No vmdk file \n")

#gcloud compute images import image-name \
#--source-file source-file \
#--os os
def create_image(password):
    create_image_cmd = "gcloud compute images import " + users[password][0]+ " --source-file "
    create_image_cmd += "gs://linux-image-bucket/" + users[password][0] + "/" + users[password][0] + ".vdmk "
    create_image_cmd += "--os ubuntu-1604"
    print(create_image_cmd)
    run_command(create_image_cmd)

def update_users():
    #users -> add img
    pass


passw = "LINUXUSER0001"
#create_dd_copy(passw)
#create_vmdk(passw)
#move_to_storage(passw)
create_image(passw)

from create_vm import create_vm
create_vm(passw)
