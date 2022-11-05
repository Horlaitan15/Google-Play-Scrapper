# importing tkinter module for GUI application
import subprocess
from tkinter import *

# Creating object 'root' of Tk()
root = Tk()

# Providing Geometry to the form
root.geometry("500x500")

# Providing title to the form
root.title('Google Play Scraper')

# this creates 'Label' widget for Registration Form and uses place() method.
label_0 = Label(root, text="Google Play Scraper", width=20, font=("bold", 20))
# place method in tkinter is  geometry manager it is used to organize widgets by placing them in specific position
label_0.place(x=90, y=60)

# this creates 'Label' widget for URL and uses place() method.
label_1 = Label(root, text="Enter Google Play URL:", width=20, font=("bold", 10))
label_1.place(x=80, y=130)

# this will accept the input string text from the user.
entry_1 = Entry(root)
entry_1.place(x=240, y=130)

# this creates 'Label' widget for API Key and uses place() method.
label_2 = Label(root, text="Enter API Key:", width=30, font=("bold", 10))
label_2.place(x=68, y=180)

entry_2 = Entry(root)
entry_2.place(x=240, y=180)

# this creates 'Label' widget for CSV File and uses place() method.
label_3 = Label(root, text="Enter CSV Output:", width=20, font=("bold", 10))
label_3.place(x=70, y=230)

entry_3 = Entry(root)
entry_3.insert(0, "e.g output.csv")
entry_3.place(x=235, y=230)


def submit():
    # To change this to set PATH=%PATH%;C:\Users\tusha\google_play
    # Should also cd into the same directory.
    def stop_run():
        process.stop()

    stop = Button(root, text='Stop Extracting', command=stop_run, width=20, bg="red", fg='white').place(x=180, y=280)
    termi = Text(root, borderwidth=3)
    termi.pack()
    process = subprocess.Popen(
        f"scrapy crawl play -a parameters={{'url':'{entry_1.get()}','key':'{entry_2.get()}'}} -t csv -o {entry_3.get()}",
        shell=True, stdout=subprocess.PIPE,
        bufsize=1, universal_newlines=True)
    for line in process.stdout:
        termi.insert(END, line)
        termi.see(END)
        termi.update_idletasks()


# this creates button for submitting the details provides by the user
start = Button(root, text='Start Extracting', command=submit, width=20, bg="green", fg='white').place(x=180, y=280)

# this will run the mainloop.
root.mainloop()
