from flask import Flask, flash, render_template, request, redirect
import subprocess
import os
import time

app = Flask(__name__)
app.debug = True


@app.route('/', methods = ['GET', 'POST'])
def index():
    with open("/root/filter", "r") as f:
         filter = f.read()
    with open("/root/vol", "r") as f:
         vol = f.read()
    with open("/root/input", "r") as f:
         input = f.read()
    return render_template('app.html', vol=vol, input=input, filter=filter)

@app.route("/volume2", methods = ['GET', 'POST'])
def volume2():
    if request.method == 'POST':
        a = request.form["c"]
        create_file(a)
        os.system('mpc volume $(cat /root/vol)> /dev/null 2>&1')
        with open("/root/vol", "r") as f:
             vol = f.read()
        return redirect('/')
    else:
        with open("/root/vol", "r") as f:
            vol = f.read()
            return vol

@app.route("/volume", methods = ['GET', 'POST'])
def volume():
    if request.method == 'POST':
        a = request.form["a"]
        create_file(a)
        os.system('mpc volume $(cat /root/vol)> /dev/null 2>&1')
        with open("/root/vol", "r") as f:
                vol = f.read()
        return redirect('/')
    else:
        with open("/root/vol", "r") as f:
            vol = f.read()
            return vol

@app.route('/input', methods = ['GET', 'POST'])
def input():
    input = request.form["input"]
    if input == "S1":
         os.system('systemctl stop led')
         os.system('amixer cset numid=2 0 >/dev/nul')
         os.system('echo "(spdif 1)" > /root/input')
    if input == "S2":
         os.system('systemctl stop led')
         os.system('amixer cset numid=2 1 >/dev/nul')
         os.system('echo "(spdif 2)" > /root/input')
    if input == "i2s":
         os.system('systemctl stop led')
         os.system('amixer cset numid=3 1 >/dev/nul')
         os.system('echo "(i2s)" > /root/input')
    if input == "auto":
         os.system('systemctl start led')
         os.system('echo "(auto select)" > /root/input')
    with open("/root/input", "r") as f:
         input = f.read()
    return redirect('/')

@app.route('/test', methods = ['GET', 'POST'])
def test():
    test = request.form["test"]
    if test == "channel":
        os.system('bash /root/channel')
    if test == "phase":
        os.system('bash /root/phase')
    if test == "net":
        os.system('bash /root/net')
    if test == "sysupdate":
        return render_template('update.html')
    return redirect('/')

@app.route('/power')
def power():
    return render_template('power.html')

@app.route('/reboot', methods = ['GET', 'POST'])
def reboot():
    os.system('bash -c "sleep 1; reboot"&')
    return redirect('/')

@app.route('/update', methods = ['GET', 'POST'])
def update():
    os.system('bash -c "sleep 1; updateroot"&')
    return render_template('working.html'), {"Refresh": "4; url='/'"}

@app.route('/no', methods = ['GET', 'POST'])
def no():
    return redirect('/')

@app.route('/poweroff', methods = ['GET', 'POST'])
def poweroff():
    os.system('bash -c "sleep 1; poweroff"&')
    return redirect('/')

@app.route('/prev', methods = ['GET', 'POST'])
def prev():
    os.system('mpc prev')
    return redirect('/')

@app.route('/play', methods = ['GET', 'POST'])
def play():
    os.system('mpc toggle')
    return redirect('/')

@app.route('/stop', methods = ['GET', 'POST'])
def stop():
    os.system('mpc stop')
    return redirect('/')

@app.route('/next', methods = ['GET', 'POST'])
def next():
    os.system('mpc next')
    return redirect('/')

def create_file(a):
    temp_conf_file = open('/root/vol', 'w')
    temp_conf_file.write('' + a + '')
    temp_conf_file.close

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)
