from flask import flash, redirect, url_for, render_template, request, jsonify
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
    def login_host(self,ip,port,username,password):
        try:
            self.tn = telnetlib.Telnet(ip,port)
            self.tn.open(ip,port)
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
def telnet():
    form = TelnetForm()
    tn = TelnetClient()
    command_results = ""
    if form.validate_on_submit():
        if form.submit.data:
            ip = form.ip.data
            port = form.port.data
            username = form.username.data
            password = form.password.data
            config1 = "sys"
            config2 = "int lo20"
            config3 = "ip add 1.1.1.1 255.255.255.255"
            dispiproute = "display ip routing-table"
            #tn = telnetlib.Telnet(ip, port=23, timeout=50)
            result = tn.login_host(ip,port,username, password)
            if result == False:
                print('Connect fail!')
            elif result == True:
                print('Connect!')
                command_results = "Connect Success!"
                print(command_results)
        elif form.submit1.data:
            inputcommand = form.inputcommand.data
            command_results = tn.execute_some_command(inputcommand)
            print(command_results)
        elif form.submit2.data:
            tn.logout_host()
    return render_template('telnet.html',form=form, command_results=command_results)

@app.route('/telnet2',methods=['GET','POST'])
def telnet2():
    form = TelnetForm()
    tn = TelnetClient()
    command_results = ""
    if form.validate_on_submit():
        if form.submit.data:
            ip = form.ip.data
            port = form.port.data
            username = form.username.data
            password = form.password.data
            config1 = "sys"
            config2 = "int lo20"
            config3 = "ip add 1.1.1.1 255.255.255.255"
            dispiproute = "display ip routing-table"
            #tn = telnetlib.Telnet(ip, port=23, timeout=50)
            result = tn.login_host(ip, port,username, password)
            if result == False:
                print('Connect fail!')
            elif result == True:
                print('Connect!')
                command_results = "Connect Success!"
                print(command_results)
        elif form.submit1.data:
            ip = form.ip.data
            port = form.port.data
            username = form.username.data
            password = form.password.data
            result = tn.login_host(ip,port, username, password)
            if result == False:
                print('Connect fail!')
            elif result == True:
                print('Connect!')
                command_results = "Connect Success!"
                print(command_results)
            inputcommand = form.inputcommand.data
            command_results = tn.execute_some_command(inputcommand)
            print(command_results)
        #elif form.submit2.data:
        #    tn.logout_host()
    return render_template('telnet.html',form=form, command_results=command_results)


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/_index_telnet')
def index_telnet():
    a = request.args.get('a', 0, type=str)
    tn = TelnetClient()
    ip = "192.168.1.10"
    port = "23"
    username = "test"
    password ="123"
    tn.login_host(ip, port, username, password)
    print("CONNting")
    result = tn.execute_some_command(a)

    return jsonify(result=result)


@app.route('/index2')
def index2():
    html = render_template('index2.html')
    return html
@app.route('/index3')
def index3():
    html = render_template('index_telnet.html')
    return html


@app.route('/test_post', methods=['GET', 'POST'])
def test_post():
    return '{"name":"zhangsan"}'
