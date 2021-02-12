# -*- coding: utf-8 -*-
from flask import Flask, request
from flask import render_template

app = Flask(__name__)
from create_vm import create_vm
from create_vm import validate_user
from create_vm import get_creation_date_from_json
from create_vm import get_selected_vm_type_from_json
from create_vm import set_selected_vm_type_to_json

pass_code =""

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def log_in():
    if request.method == "POST":
        login = request.form['text']
        password = request.form['password']
        global pass_code
        pass_code = password
        if validate_user(password, login):
            #TODO dodaj ustawianie  date_of_creation i current_vm_type_selected podczas przechodzenia
            return render_template('setting_page.html', date_of_creation=get_creation_date_from_json(pass_code), current_vm_type_selected=get_selected_vm_type_from_json(pass_code))
        else:
            return render_template('index.html', invalidcode="Nie ma takiego uzytkownika")
    else:
        return render_template('index.html')


@app.route('/start_vm', methods=['GET', 'POST'])
def start_vm():
    # output0 = pass_code
    try:
        output = create_vm(pass_code)
        output1 = output.split("STATUS", 1)[0]
        output2 = output.split("STATUS", 1)[1]
        output1_splitted = output1.split()
        output2_splitted = output2.split()
        output1_msg = output1_splitted[0] + " " + output1_splitted[1] + " " + output1_splitted[2]
        output2_msg = "VMs IP address is: " +output2_splitted[4]
        return render_template('setting_page.html', output_1=output1_msg, output_2=output2_msg, date_of_creation=get_creation_date_from_json(pass_code), current_vm_type_selected=get_selected_vm_type_from_json(pass_code))
    except:
        return render_template('setting_page.html', output_0="Nastapil problem z wystartowaniem VM. ",date_of_creation=get_creation_date_from_json(pass_code), current_vm_type_selected=get_selected_vm_type_from_json(pass_code))

@app.route('/change_type', methods=['POST'])
def change_type():
    select = request.form.get('vm_type')
    set_selected_vm_type_to_json(pass_code, select)
    return render_template('setting_page.html', date_of_creation=get_creation_date_from_json(pass_code), current_vm_type_selected=get_selected_vm_type_from_json(pass_code))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
