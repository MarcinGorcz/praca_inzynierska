import os
import json

class manage_users:
    path = "./users_config.json"
    test_users = {
    "passphrase": {
        "login": "user1",
        "password": "admin123",
        "vm_type": "n1-standard-1",
        "imagename": "user1-22112020"
    }
    }

    def json_init(self):
        with open(manage_users.path, "w") as outfile:
            json.dump(manage_users.test_users, outfile)

    def json_to_dict(self):
        with open(manage_users.path) as json_file:
            data = json.load(json_file)
            return data

    def dict_to_json(self,users_dict):
        with open(manage_users.path, "w") as outfile:
            json.dump(users_dict, outfile)

if __name__ == '__main__':
    a = manage_users()
    a.json_init()
    dic = a.json_to_dict()
    #print(dic)
    #print(dic["LINUXUSER1120"][0])
    a.dict_to_json(dic)



