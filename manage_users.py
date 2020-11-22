import os
import json

class manage_users:
    path = "./users_config.json"
    test_users = {
        "LINUXUSER1120": [
            "linuxuser1",
            "europe-west6-a",
            "n1-standard-1",
            "ubuntufromraw2"
        ],
        "LINUXUSER0001": [
            "linuxuser1",
            "europe-west6-a",
            "n1-standard-1",
            "linuxuser1"
        ],
        "LINUXUSER2077": [
            "linuxuser2",
            "europe-west6-a",
            "n1-standard-1",
            "ubuntufromraw2"
        ]
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



