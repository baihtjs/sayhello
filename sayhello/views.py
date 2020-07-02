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
        print('connect')

    def close(self):
        print('close')

class TelnetClient():
    def __init__(self,):
        self.tn = telnetlib.Telnet()

    # 此函数实现telnet登录主机
    def login_host(self,ip,username,password):
        try:
            self.tn = telnetlib.Telnet(ip,port=23)
            self.tn.open(ip,port=23)
        except:
            logging.warning('%s网络连接失败'%ip)
            return False
        # 等待login出现后输入用户名，最多等待10秒
        self.tn.read_until(b'Username:',timeout=10)
        self.tn.write(username.encode('ascii') + b'\n')
        # 等待Password出现后输入用户名，最多等待10秒
        time.sleep(2)
        self.tn.read_until(b'Password:',timeout=10)
        self.tn.write(password.encode('ascii') + b'\n')
        # 延时两秒再收取返回结果，给服务端足够响应时间
        time.sleep(2)
        # 获取登录结果
        # read_very_eager()获取到的是的是上次获取之后本次获取之前的所有输出
        command_result = self.tn.read_very_eager().decode('ascii')
        if 'Login incorrect' not in command_result:
            logging.warning('%s登录成功'%ip)
            return True
        else:
            logging.warning('%s登录失败，用户名或密码错误'%ip)
            return False

    # 此函数实现执行传过来的命令，并输出其执行结果
    def execute_some_command(self,command):
        # 执行命令
        self.tn.write(command.encode('ascii')+b'\n')
        time.sleep(2)
        # 获取命令结果
        command_result = self.tn.read_very_eager().decode('ascii')
        logging.warning('命令执行结果：\n%s' % command_result)
        return command_result

    # 退出telnet
    def logout_host(self):
        self.tn.write(b"quit\n")

@app.route('/telnet',methods=['GET','POST'])
def telnet(command_result=None):
    form = TelnetForm()
    command_results = ""
    if form.validate_on_submit():
        ip = form.ip.data
        port = form.port.data
        username = form.username.data
        password = form.password.data
        config1 = "sys"
        config2 = "int lo1"
        config3 = "ip add 1.1.1.1 255.255.255.255"
        #tn = telnetlib.Telnet(ip, port=23, timeout=50)
        tn = TelnetClient()
        tn.login_host(ip,username,password)
        time.sleep(2)
        tn.execute_some_command(config1)
        time.sleep(2)
        tn.execute_some_command(config2)
        command_results = command_result
        #print(tn.read_very_eager())
       # tn.write(username.encode('ascii') + b'\n')
        #print(tn.read_very_eager())
        time.sleep(2)
      #  tn.write(password.encode('ascii') + b'\n')
       # print(tn.read_very_eager())
       # time.sleep(2)
      #  tn.write(config1.encode('ascii') + b'\n')
      #  time.sleep(2)
       # tn.write(config2.encode('ascii') + b'\n')
       # time.sleep(2)
       # tn.write(config3.encode('ascii') + b'\n')
        #tn.write("sys\n")
      #  print(tn.read_very_eager())
        time.sleep(2)
        tn.logout_host()
    return render_template('telnet.html',form=form)




