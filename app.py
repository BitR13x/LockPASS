from flask import Flask, render_template, redirect, request
from string import ascii_letters, digits
from base64 import b64decode, b64encode
from json import dump, dumps, load
from random import choice
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
#from Crypto.Random import get_random_bytes
from Crypto import Random
from sys import argv
from os import listdir
from hashlib import md5


app = Flask(__name__)


@app.route("/generator", methods=["GET", "POST"])
def passwordgen():
    punctuation = '''!@#$%&*?:'''
    letters = ascii_letters + digits + punctuation
    password = ''.join(choice(letters) for _ in range(45))
    passwordgen.password = password

    return render_template('password.html', password=password)


@app.route("/save", methods=['POST'])
def save():
    if request.method == "POST":
        soubor = request.form['soubor']

        with open(".masterpass.txt", "r") as pas:
            mpass = pas.readline()

        try:
            Error = False
            contentd = listdir("passwords")
            for item in contentd:
                if item == str(soubor) + ".json":
                    Error = True
                    return render_template("password.html", save="Already existing")

            if not soubor:
                Error = True
                return render_template("password.html", save="You must specify name")

            if not Error:

                mypassdic = {
                    'name': soubor,
                    'password': passwordgen.password
                }

                with open("passwords/%s.json" % (soubor), "w") as file:
                    dump(mypassdic, file)

                with open("passwords/%s.json" % (soubor), "r") as jsonFile:
                    data = load(jsonFile)

                encryptf(data["password"], mpass)
                data["password"] = encryptf.passwd.decode("utf8")

                with open("passwords/%s.json" % (soubor), "w") as jsonFile:
                    jsonFile.write(dumps(data))

        except:
            return render_template("password.html", save="Something went wrong, try reloading page from /")

        try:
            return redirect('/generator')  # text save=SAVED

        except:
            return render_template('password.html', save="Something went wrong, try reloading page from /")


@app.route('/manager', methods=["GET", "POST"])
def pass_manager():
    contentd = [x.split('.')[0] for x in listdir('passwords')]
    return render_template('manager.html', available=contentd)


@app.route('/decode', methods=["POST"])
def file_decode():
    with open(".masterpass.txt", "r") as pas:
        mpass = pas.readline()

    if request.method == "POST":
        field = request.form['master']
        filename = request.form['filename']
        if not filename:
            return render_template("manager.html", error="You must specify filename")

        if not field:
            return render_template("manager.html", error="You must specify enter password")

        try:
            result = md5(field.encode())
            md5pass: str = result.hexdigest()

        except:
            return redirect('/manager')

        if mpass == md5pass:
            try:
                with open("passwords/%s.json" % (filename), "r") as jsonFile:
                    data = load(jsonFile)

                encodedpass = data['password'].encode("utf8")
                decryptf(encodedpass, mpass)
                data["password"] = decryptf.passwd

                name: str = data['name']
                password: str = data['password']

            except:
                name = "file not in options"
                password = ""

        else:
            password = "Bad password"

    return render_template('creds.html', name=name, password=password, mimetype='text/plain')


def get_key(password):
    salt = password.encode("utf8")
    kdf = PBKDF2(password, salt, 64, 1000)
    return kdf[:32]


def encryptf(plain_text, password):
   # encode salt
    BLOCK_SIZE = 32
    def pad(s): return s + (BLOCK_SIZE - len(s) %
                            BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
    key = get_key(password)

    plain_text = pad(plain_text)
    IV = Random.new().read(AES.block_size)
    mode = AES.MODE_CBC
    cipher = AES.new(key, mode, IV=IV)

    passwd = b64encode(IV + cipher.encrypt(plain_text.encode("utf8")))
    encryptf.passwd = passwd


def decryptf(ENCRYPTED, password):
    BLOCK_SIZE = 32
    def unpad(s): return s[:-ord(s[len(s) - 1:])]

    ENCRYPTED = b64decode(ENCRYPTED)
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
        argument = str(argv[1].lower())
        if argument == "--public":
            app.run(host="0.0.0.0", port=5000)
        elif argument == "--debug":
            app.run(host="localhost", debug=True, port=5000)
        elif argument == "--help":
            print("--public \n   Hosted on 0.0.0.0 \n")
            print("--debug \n   Debug mode \n")
            print("\n empty for localhost")
        else:
            app.run(host="localhost", port=5000)
    except IndexError:
        app.run(host="127.0.0.1", port=5000)
