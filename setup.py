print("if you not specify your master password encryption not goin to work \nkeep in your mind this is BETA so bugs report is good idea. \n \nif you want help or interest to work with me add me on discord Kiwi501987#4861 \n")

mpass = input("Insert your master password: ")

with open(".masterpass.txt", 'w') as file:
    file.write(mpass)
    file.close()

print("Done")
