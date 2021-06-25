import socket
import tkinter as tk
from tkinter import filedialog
import time
import threading
import os
import json
from tkinter import font
from tkinter.constants import CENTER
from chat_cli import ChatClient

class GUI:
    def __init__(self) -> None:
        self.chatClient = ChatClient()
        
        self.Window = tk.Tk()
        self.Window.withdraw()

        self.loginScreen = tk.Toplevel()

        self.loginScreen.title('Login')
        self.loginScreen.resizable(width=False, height=False)
        self.loginScreen.config(width=400, height=350)

        self.pls = tk.Label(self.loginScreen,
                            text="Please Login",
                            justify=tk.CENTER,
                            font="Helvetica 12 bold")

        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.userLabelName = tk.Label(self.loginScreen, text="Username: ", font="Helvetica 11")
        self.userLabelName.place(relheight=0.2, relx=0.1, rely=0.25)


        self.userEntryName = tk.Entry(self.loginScreen, font="Helvetica 12")
        self.userEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.30)
        self.userEntryName.focus()

        self.passwordLabelName = tk.Label(self.loginScreen, text="Password: ", font="Helvetica 12")
        self.passwordLabelName.place(relheight=0.2, relx=0.1, rely=0.40)

        self.passwordEntryName = tk.Entry(self.loginScreen, font="Helvetica 11", show="*")
        self.passwordEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.45)

        self.loginButton = tk.Button(self.loginScreen,
                                text="Login",
                                font="Helvetica 12 bold",
                                command = lambda: self.login(self.userEntryName.get(), self.passwordEntryName.get()))
        self.loginButton.place(relx=0.35, rely=0.62)

        self.Window.mainloop()

    def login(self, username, password):
        self.name = username

        response = self.chatClient.login(self.name, password)

        if response['status'] == 'ERROR':
            print("Username atau Password Salah")
        else:
            self.loginScreen.destroy()
            self.option()

            # rcv = threading.Thread(target=self.receive)
            # rcv.start()

    def option(self, fromApp=False, screen=None):
        if fromApp:
            if screen == 'inboxPage':
                self.inboxPage.destroy()
            if screen == 'chatBoxPage':
                self.chatBoxPage.destroy()

        self.Window.withdraw()

        self.optionPage = tk.Toplevel()

        self.optionPage.title("Option")
        self.optionPage.resizable(width=False, height=False)
        self.optionPage.configure(width=400, height=350)
        
        self.chatToLabelName = tk.Label(self.optionPage, text="Chat to: ", font="Helvetica 11")
        self.chatToLabelName.place(relheight=0.1, relx=0.0, rely=0.0)

        self.chatToEntryName = tk.Entry(self.optionPage, font="Helvetica 12")
        self.chatToEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.2, rely=0.0)
        self.chatToEntryName.focus()

        self.chatToButton = tk.Button(self.optionPage, 
                                        text="to CHAT", 
                                        font="Helvetica 12 bold", 
                                        command = lambda: self.chat(self.chatToEntryName.get()))
        self.chatToButton.place(relx=0.65, rely=0.0)

        self.chatGroupLabel = tk.Label(self.optionPage, text="Group to: ", font="Helvetica 11")
        self.chatGroupLabel.place(relheight=0.2, relx=0.0, rely=0.2)

        self.chatGroupEntry = tk.Entry(self.optionPage, font="Helvetica 12")
        self.chatGroupEntry.place(relwidth=0.4 ,relheight=0.1, relx=0.2, rely=0.25)
        self.chatGroupEntry.focus()

        self.chatGroupButton = tk.Button(self.optionPage, 
                                        text="to GROUP", 
                                        font="Helvetica 12 bold", 
                                        command = lambda: self.group())
        self.chatGroupButton.place(relx=0.65, rely=0.25)

        self.inboxButton = tk.Button(self.optionPage, 
                            text="INBOX", 
                            font="Helvetica 12 bold", 
                            command = lambda: self.inbox())
        self.inboxButton.place(relx=0.35, rely=0.62)

    def chat(self, username):
        self.usernameTo = username

        self.optionPage.destroy()
        self.chatBox()

    def chatBox(self):
        self.chatBoxPage = tk.Toplevel()
        self.chatBoxPage.title(self.usernameTo)
        self.chatBoxPage.resizable(width=False, height=False)
        self.chatBoxPage.configure(width=400, height=350)

        self.messageEntryName = tk.Entry(self.chatBoxPage, font="Helvetica 12")
        self.messageEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.2, rely=0.0)
        self.messageEntryName.focus()

        self.sendMessageButton = tk.Button(self.chatBoxPage, 
                                        text="Send", 
                                        font="Helvetica 12 bold", 
                                        command = lambda: self.sendPersonalMessage(self.messageEntryName.get()))
        self.sendMessageButton.place(relx=0.65, rely=0.0)

        self.exitButton = tk.Button(self.chatBoxPage, 
                            text="BACK", 
                            font="Helvetica 12 bold", 
                            command = lambda: self.option(True, 'chatBoxPage'))
        self.exitButton.place(relx=0.35, rely=0.62)

    def sendPersonalMessage(self, msg):
        response = self.chatClient.sendmessage(self.usernameTo, msg)

        if response['status'] == 'OK':
            self.responseLabel = tk.Label(self.chatBoxPage, text="Messagge Sent", font="Helvetica 11")
            self.responseLabel.place(relheight=0.2, relx=0.5, rely=0.5)
        else:
            self.responseLabel = tk.Label(self.chatBoxPage, text="Messagge Failed to Sent", font="Helvetica 11")
            self.responseLabel.place(relheight=0.2, relx=0.5, rely=0.5)

    def inbox(self):
        self.optionPage.destroy()
        
        self.Window.withdraw()

        self.inboxPage = tk.Toplevel()

        self.inboxPage.title("Inbox")
        self.inboxPage.resizable(width=False, height=False)
        self.inboxPage.configure(width=400, height=350)

        self.inboxChatFromTitle = tk.Label(self.inboxPage, text="Msg from", font="Helvetica 11")
        self.inboxChatFromTitle.place(relheight=0.1, relx=0.0, rely=0.0)

        self.inboxChatFromContent = tk.Label(self.inboxPage, text="Content Sender", font="Helvetica 11")
        self.inboxChatFromContent.place(relheight=0.1, relx=0.0, rely=0.15)

        self.getInbox()

        self.exitButton = tk.Button(self.inboxPage, 
                            text="BACK", 
                            font="Helvetica 12 bold", 
                            command = lambda: self.option(True, 'inboxPage'))
        self.exitButton.place(relx=0.35, rely=0.62)

    def getInbox(self):
        response = self.chatClient.inbox()

        self.inboxChatFromContent.configure(text=response)

if __name__ == "__main__":
    g = GUI()
