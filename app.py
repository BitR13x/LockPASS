from flask import Flask, render_template, redirect, request, url_for
import random
import string
import os
import sys
import base64
import hashlib
import json
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

app = Flask(__name__)

@app.route("/generator", methods=["GET", "POST"])
def passwordgen():
    punctuation = '''!@#$%&*?:''';
    letters = string.ascii_letters + string.digits + punctuation
    password = ''.join(random.choice(letters) for i in range(45))
    passwordgen.password = password

    return render_template('password.html', password=password)

@app.route("/save", methods=['POST'])
def save():
    if request.method == "POST":

        soubor = request.form['soubor']

        with open(".masterpass.txt", "r") as pas:
            mpass = pas.readline()
            pas.close()

        try:
            Error = False
            contentd = os.listdir("passwords")
            for index in range(len(contentd)):
                if contentd[index] == str(soubor) + ".json":
                    Error = True
                    return render_template("password.html", save="Already existing")

            if soubor == "":
                Error = True
                return render_template("password.html", save="You must specify name")

            if Error == False:

                file = open("passwords/%s.json" %(soubor), "w")
                mypassdic = {
                    'name': soubor,
                    'password': passwordgen.password
                }
                json.dump(mypassdic, file)
                file.close()


                jsonFile = open("passwords/%s.json" %(soubor), "r")
                data = json.load(jsonFile)
                jsonFile.close()

                encryptf(data["password"], mpass)
                data["password"] = encryptf.passwd.decode("utf8")

                jsonFile = open("passwords/%s.json" %(soubor), "w")
                jsonFile.write(json.dumps(data))
                jsonFile.close()

        except:
            return render_template("password.html", save="Something went wrong, try reloading page from /")

        try:
            return redirect('/generator') # text save=SAVED
        except:
            return render_template('password.html', save="Something went wrong, try reloading page from /")


@app.route('/manager', methods=["GET", "POST"])
def pass_manager():
    contentd = os.listdir("passwords")
    return render_template('manager.html', available=contentd)

@app.route('/decode', methods=["POST"])
def file_decode():
    #contentd = os.listdir("passwords")
    with open(".masterpass.txt", "r") as pas:
        mpass = pas.readline()
        pas.close()

    if request.method == "POST":
        field = request.form['master']
        filename = request.form['filename']

        if filename == "":
            return render_template("manager.html", error="You must specify filename")

        try:
            result = hashlib.md5(field.encode())
            md5pass = result.hexdigest()
        except:
            return redirect('/manager')
        if mpass == md5pass:
            try:
                jsonFile = open("passwords/%s.json" %(filename), "r")
                data = json.load(jsonFile)
                jsonFile.close()

                encodedpass = data['password'].encode("utf8")
                decryptf(encodedpass, mpass)
                data["password"] = decryptf.passwd

                name = data['name']
                password = data['password']

            except:
                name = "file not in options"
                password = ""
        else:
            password = "Bad password"

    return render_template('creds.html',name=name ,password=password, mimetype='text/plain')

def get_key(password):
    salt = password.encode("utf8")
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key

def encryptf(plain_text, password):
   #encode salt
    BLOCK_SIZE = 32
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
    key = get_key(password)

    plain_text = pad(plain_text)
    IV = Random.new().read(AES.block_size)
    mode = AES.MODE_CBC
    cipher = AES.new(key, mode, IV=IV)

    passwd = base64.b64encode(IV + cipher.encrypt(plain_text.encode("utf8")))
    encryptf.passwd = passwd

def decryptf(ENCRYPTED, password):
    BLOCK_SIZE = 32
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    ENCRYPTED = base64.b64decode(ENCRYPTED)
    iv = ENCRYPTED[:16]
    key = get_key(password)

    mode = AES.MODE_CBC
    cipher = AES.new(key, mode, iv)

    passwd = unpad(cipher.decrypt(ENCRYPTED[16:]))
    decryptf.passwd = passwd.decode("utf8")

@app.route('/')
def render_static():
    return render_template('index.html')

if __name__ == '__main__':
    try:
        argument = sys.argv[1].lower()
        if str(argument) == "--public":
            app.run(host="0.0.0.0", port=5000)
        elif str(argument) == "--debug":
            app.run(host="localhost", debug=True, port=5000)
        elif str(argument) == "--help":
            print("--public \n   Hosted on 0.0.0.0 \n")
            print("--debug \n   Debug mode \n")
            print("\n empty for localhost")
        else:
            app.run(host="localhost", port=5000)
    except IndexError:
        app.run(host="127.0.0.1", port=5000)
