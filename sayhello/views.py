from flask import flash, redirect, url_for, render_template
import telnetlib
from threading import Thread
import json
import time
import traceback
import datetime
import logging
from sayhello.forms import HelloForm, TelnetForm
from sayhello.models import Message
from sayhello import db
from sayhello import app


@app.route('/', methods=['GET', 'POST'])
def index():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(name=name, body=body)
        db.session.add(message)
        db.session.commit()
        flash('You leave the message success!')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, messages=messages)

class Telnet():
    def connect(self,ip,username,password,port,timeout=30):

    def close(self):



@app.route('/telnet',methods=['GET','POST'])
def telnet():
    form = TelnetForm()
    telnet = Telnet()
    if form.validate_on_submit():
        ip = form.ip.data
        port = form.port.data
        username = form.username.data
        password = form.password.data
        tn = telnetlib.Telnet(ip, port=23, timeout=50)
        tn.write(password + '\n')
        print(tn.read_very_eager())
        telnet.close()
    return render_template('telnet.html',form=form)




