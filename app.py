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
        soubor = request.form['soubor']

        try:
            file = open("passwords/%s" %(soubor), "w")
            file.write(str(soubor) + "------" + passwordgen.password)
            file.close()
        except:
            contentd = os.listdir("passwords")

            for index in range(len(contentd)):
                if contentd[index] == soubor:
                    return render_template("password.html", save="Already existing")
                elif soubor == "":
                    return render_template("password.html", save="You must specify name")

        try:
            return redirect('/generator') # text save=SAVED
        except:
            return render_template('password.html', save="Something went wrong, try reloading page from /")


@app.route('/manager')
def pass_manager():
    contentd = os.listdir("passwords")
    filecontentd = []
#    try:
#        buttons = "<input type='submit'> \n" * len(contentd)
#    except:
#        return render_template('manager.html', credsfile="first add some passwords")
    for i in range(len(contentd)):
        file = open("passwords/%s" %(contentd[i]), "r")
        readf = file.read()
        filecontentd.append(readf)
        file.close()
    return render_template('creds.html', contentd=filecontentd, mimetype='text/plain')
    #except:
    #    return render_template('creds.html', contentd="Something went wrong")

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
