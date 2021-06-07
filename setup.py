import hashlib
from getpass import getpass
import os

print("if you not specify your master password encryption not goin to work \nkeep in your mind this is BETA so bugs report is good idea. \n \nif you want help or interest to work with me add me on discord Kiwi501987#4861 \n \n if you don't wanna moving background just delete static/canvas.js")

str2 = getpass("Insert your master password: ")
result = hashlib.md5(str2.encode())
mpass = result.hexdigest()

try:
    os.mkdir("passwords")
except:
    print("Folder already exist")

with open(".masterpass.txt", 'w') as file:
    file.write(mpass)
    file.close()

print("Done")
