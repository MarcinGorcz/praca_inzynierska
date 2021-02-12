#! /bin/bash
adduser --disabled-password --gecos "" user1
echo -e "admin123\nadmin123" | passwd user1
sed -i '/^PasswordAuthentication/s/no/yes/' /etc/ssh/sshd_config
service ssh restart
sudo apt update
sudo apt install tightvncserver
echo -e "admin123\nadmin123" | vncpasswd
vncserver
