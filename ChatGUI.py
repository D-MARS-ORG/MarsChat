import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
# smtp.mail.yahoo.com
import time
from tkinter import *
from tkinter import ttk
import socket
import _thread
import select
import time
import math
import threading
import os.path

from threading import Timer
class Application(Frame):
    """ Gui Application """
    def __init__(self, master):
        """ initialize the Frame """
        ttk.Frame.__init__(self, master)
        curtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        self.ilogo = PhotoImage(file = "logo.gif")
        self.master = master
        self.master.title("Mars Habitat Chat System")
        self.master.geometry("840x640")
        """root.bind("", keydown)
        root.bind("", keyup)"""
        self.master.attributes("-topmost", True)
        self.startTime = time.strftime("%a %d %b %Y %H_%M_%S", time.localtime())
        print(self.startTime)
        self.buffsize = 1024
        Grid.rowconfigure(self, 0, weight=1)  # liam
        Grid.columnconfigure(self, 0, weight=1)  # liam
        Grid.columnconfigure(self, 1, weight=1)  # liam
        Grid.columnconfigure(self, 2, weight=1)  # liam
        Grid.columnconfigure(self, 3, weight=1)  # liam
        Grid.columnconfigure(self, 4, weight=1)  # liam
        self.grid(row=0, column=0, sticky=N + S + E + W)  # liam

        self.grid()
        self.create_widgets()
        self.read_config()

    def addSubject(self, sub, tag):
        sub_log = open ("subject_log.txt", "r")
        f = False
        for line in sub_log.readlines():
            if line.rstrip() == sub.rstrip(): f = True

        sub_log.close()
        if(not f):
            sub_log = open("subject_log.txt", "a")
            sub_log.write(sub)
            sub_log.write('\n')
            sub_log.close()
        sub_log = open("subject_log.txt", "r")
        sublist = list()
        for line in sub_log.readlines():
            sublist.append(line.rstrip())
        self.cbSubject['values'] = sublist
        sub_log.close()

    def read_config(self):
        config = open("config.txt", "r")
        settings = config.readlines()
        status = settings[0].split("=")[1].strip()
        targetIP = settings[1].split("=")[1].strip()
        self.delay = (int)(settings[2].split("=")[1].strip())
        sender = settings[3].split("=")[1].strip()
        to = settings[4].split("=")[1].strip()
        self.FromEmail.insert(END, sender)
        self.ToEmail.insert(END, to)
        self.FromEmail.configure(state = 'disable')
        self.ToEmail.configure(state='disable')
        config.close()
        if (status == 'server'):
            self.handleSetServer()
        else:
            self.handleAddClient(targetIP)
    def log_msg(self):
        filename = ("Log for conversation at " + self.startTime + ".txt")
        log = open(filename, "w")
        log.write(self.msgLog.get("1.0", END))
        log.close()
    def create_widgets(self):
        myfont = ('', 12)

        imageConnect = PhotoImage(file="button_connect.gif")  # liam
        imageLog = PhotoImage(file="button_log.gif")

        # row 0
        # text box
        self.msgLog = Text(self, font=('', 12), height=15)
        self.msgLog.grid(row=0, column=0, columnspan=6, pady=4, sticky=N+S+E+W)
        self.scrollog = Scrollbar(self, command=self.msgLog.yview)
        self.scrollog.grid(row=0, column=6, pady=5, sticky=N+S+E+W)
        self.msgLog['yscrollcommand'] = self.scrollog.set
        self.msgLog.tag_configure("sent", background="#e0e0e0", justify=LEFT)
        self.msgLog.tag_configure("received", background="#ffffff", justify=RIGHT)
        # self.msgLog.config(state=DISABLED)
        # row 1
        # create label for To:
        self.label1 = Label(self, font=myfont, text='To: ').grid(row=1, column=1, pady=5, stick=N+S+E+W)
        # create combo box for the address
        self.ToEmail = Entry(self, font=myfont)
        self.ToEmail.grid(row=1, column=2, pady=5, sticky=N+S+E+W)
        # create label from
        self.label2 = Label(self, font=myfont, text='From: ').grid(row=1, column=3, pady=5, stick=N+S+E+W)
        # create combo box for the address
        self.FromEmail = Entry(self, font=myfont)
        self.FromEmail.grid(row=1, column=4, pady=5, sticky=N+S+E+W)

        self.btnLog = Button(self, command=self.log_msg)
        self.btnLog.config(image=imageLog)
        self.btnLog.image = imageLog
        self.btnLog.grid(row=1, column=5)

        # row 2
        # create label list of email addresses
        self.label3 = Label(self, font=myfont, text='Subject: ').grid(row=2, column=1, pady=5, stick=N+S+E+W)

        # create combo box for the address
        self.cbSubject = ttk.Combobox(self, font=myfont)
        subjects = open("subject_log.txt", "r")
        sublist = list()
        for line in subjects.readlines():
            sublist.append(line.rstrip())
        self.cbSubject['values'] = sublist
        subjects.close()

        self.cbSubject.grid(row=2, column=2, pady=7, columnspan=4, sticky=N+S+E+W)
        # row 3
        self.label4 = Label(self, font=myfont, text='body: ').grid(row=3, column=1, pady=5, stick=N+S+E+W)

        # row 4
        # create text box to hold the text for the letter
        self.text = Text(self, font=('', 12), height=10)
        self.text.grid(row=4, column=0, columnspan=6, pady=5, sticky=N+S+E+W)
        self.scrollb = Scrollbar(self, command=self.text.yview)
        self.scrollb.grid(row=4, column=6, pady=5, sticky=N+S+E+W)
        self.text['yscrollcommand'] = self.scrollb.set

        # row 5
        image2 = PhotoImage(file="button_send.gif")  # liam
        self.btnSend = Button(self, font=myfont,
                                 command=self.handleSendChat)
        self.logo = Label(self, image=self.ilogo).grid(row=1, column=0, rowspan=3, pady=5, stick=N+S+E+W)
        self.btnSend.config(image=image2, compound=RIGHT)  # liam
        self.btnSend.image = image2  # liam
        self.btnSend.grid(row=5, column=5)  # liam

    def handleSetServer(self):
        self.HOST = '0.0.0.0'
        self.PORT = 5005
        self.serverSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #No idea, delete if problem
        self.serverSoc.bind((self.HOST, self.PORT))
        self.serverSoc.listen(5)
        self.soc = self.serverSoc
        print("connected...")
        _thread.start_new_thread(self.listenClients, ())
    def listenClients(self):
        while 1:
            (self.clientSoc, clientaddr) = self.serverSoc.accept()
            print("connected...")
            _thread.start_new_thread(self.handleClientMessages, (self.clientSoc, clientaddr))
        self.serverSoc.close()
    def handleAddClient(self, ip):
        clientaddr = (ip , 5005) #for testing
        self.clientSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSoc.connect(clientaddr)
        _thread.start_new_thread(self.handleClientMessages, (self.clientSoc, clientaddr))
    def handleClientMessages(self, clientsoc, clientaddr):
        while 1:
            try:
                data = clientsoc.recv(self.buffsize)
                if not data:
                    break
                self.text.config(state=NORMAL)
                t = Timer(self.delay, self.addChat, [data, "received"])
                t.start()
            except:
                break
        clientsoc.close()
    def handleSendChat(self):
        curtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        frommsg = self.FromEmail.get()
        msgtext = self.text.get("1.0", END)
        subject = self.cbSubject.get()
        msg = "{} from: {} [{}] {}".format(curtime, frommsg, subject, msgtext)
        if msg == '':
            return

        selfmsg = "{} from: {} ETA: {} [{}] {}".format(curtime, frommsg, time.strftime("%H:%M:%S",
                                                    (time.localtime((int)(time.time())+self.delay))),subject, msgtext)
        self.addChat(selfmsg, "sent")
        self.text.delete("1.0", END)
        self.clientSoc.send(msg.encode('UTF-8'))
    def addChat(self, msg, tag):
        if tag != 'sent':
            msg = msg.decode("UTF-8")

        sub = (msg.split("[")[1]).split("]")[0]
        sub_msg = open("messeges obout " + sub + ".txt", "a")

        self.addSubject(sub, tag)
        sub_msg.write(msg)
        sub_msg.close()

        self.msgLog.config(state=NORMAL)
        self.msgLog.insert(END, msg, tag)
        self.msgLog.insert(END, "")
        self.msgLog.config(state=DISABLED)

def main():
  root = Tk()
  frame = Frame(root)
  Grid.rowconfigure(root, 0, weight=1)
  Grid.columnconfigure(root, 0, weight=1)
  frame.grid(row=0, column=0, sticky=N + S + E + W)
  grid = Frame(frame)
  grid.grid(sticky=N + S + E + W, column=0, row=6, columnspan=5)
  Grid.rowconfigure(frame, 6, weight=1)
  Grid.columnconfigure(frame, 0, weight=1)
  app = Application(root)
  root.mainloop()
if __name__ == '__main__':
  main()
