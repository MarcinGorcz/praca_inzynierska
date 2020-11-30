# -*- coding: utf-8 -*-

from flask import Flask, request
from flask import render_template

app = Flask(__name__)
from create_vm import create_vm
from create_vm import validate_user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    login = request.form['text']
    password = request.form['password']
    if (validate_user(password, login)):
        output = create_vm(password)
        output1 = output.split("STATUS", 1)[0]
        output2 = output.split("STATUS", 1)[1]
        return render_template('index.html', output_1=output1, output_2=output2)
    else:
        return render_template('index.html', invalidcode = "Nie ma takiego uzytkownika")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
