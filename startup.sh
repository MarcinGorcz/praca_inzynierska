#! /bin/bash
sed - i '/^PasswordAuthentication/s/no/yes/' / etc / ssh / sshd_config
service ssh restart