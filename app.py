# add login
from flask import Flask, render_template, redirect, request, url_for
import random
import string
import sys
import os

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
        #dictionary use for pass and sites
        #encrypt passwords
        text = request.form['text']

        try:
            file = open("passwords/%s" %(text), "w")
            file.write(passwordgen.password + "------" + str(text))
            file.close()
        except:
            return render_template("password.html", save="You must specify name")

        try:
            return redirect('/generator') # text save=SAVED
        except:
            return render_template('password.html', save="Something went wrong, try reloading page from /")


@app.route('/manager')
def pass_manager():
    files = os.listdir("passwords")
    content = []
    for f in files:
        content.append(f)

    #with open("passwords/creds", "r") as file:
    #    content = file.read()

    return render_template('manager.html', content=content, mimetype='text/plain')

@app.route('/')
def render_static():
    return render_template('index.html')

if __name__ == '__main__':
   app.run(debug="true")


# string.ascii_uppercase 	Returns a string with uppercase characters
# string.ascii_lowercase 	Returns a string with lowercase characters
# string.ascii_letters 	    Returns a string with both lowercase and uppercase characters
# string.digits 	        Returns a string with numeric characters
# string.punctuation 	    Returns a string with punctuation characters
