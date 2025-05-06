from sqlalchemy import MetaData, Table, Column, Row, Integer, String, create_engine
import customtkinter as ctk
import tkinter.messagebox as tkm
from tkinter import StringVar
import smtplib
from email.mime.text import MIMEText  

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.engine = create_engine('sqlite:///members.db')
        self.meta = MetaData()
        self.conn = self.engine.connect()
        self.user = Table('users', self.meta, Column('code', Integer, primary_key= True),
                          Column('username', String),
                          Column('password', String))
        
        self.meta.create_all(self.engine)
        self.geometry('800x500')
        self.title('Sign in/up')
        self.pane = ctk.CTkFrame(self, corner_radius=20)
        self.pane.pack(pady=20, padx=10)
        self.button_log = ctk.CTkButton(self.pane, fg_color='darkblue', hover_color='blue', border_spacing=5,font=('Calibri', 19), text='Login', command=self.login)
        self.button_log.pack(pady=10, padx=10, expand=True, side= 'left')
        self.button_reg = ctk.CTkButton(self.pane, fg_color='darkblue', hover_color='blue', border_spacing=5,font=('Calibri', 19), text='Register', command=self.regester)
        self.button_reg.pack(pady=10, padx=10, expand=True, side= 'left')
        self.button_email = ctk.CTkButton(self.pane, fg_color='darkblue', hover_color='blue', border_spacing=5,font=('Calibri', 19), text='Email', command=self.email)
        self.button_email.pack(pady=10, padx=10, expand=True, side= 'left')
        self.pane_login = ctk.CTkFrame(self, corner_radius=10, width=300, height=400)
        self.pane_register = ctk.CTkFrame(self, corner_radius=10, width=300, height=400)
        self.pane_email = ctk.CTkFrame(self, corner_radius=10, width=300, height=400) 

        self.button_log.configure(fg_color='black')
        self.newtext = ctk.CTkLabel(self.pane_login, text='Login account', font=('Calibri', 18))
        self.newtext.pack(pady=12, padx=10)
        self.user_entry1 = ctk.CTkEntry(self.pane_login, placeholder_text="Username")
        self.user_entry1.pack(pady=12, padx=10)
        self.user_pass1 = ctk.CTkEntry(self.pane_login, placeholder_text="Password", show="*")
        self.user_pass1.pack(pady=12, padx=10)
        self.checkbox1 = ctk.CTkCheckBox(self.pane_login, text='Show passowrd', command=self.show_pass)
        self.checkbox1.pack(pady=12, padx=10)
        self.button = ctk.CTkButton(self.pane_login, text='Login', command=self.select)
        self.button.pack(pady=12, padx=10)

        self.button_reg.configure(fg_color= 'black')
        self.newtext = ctk.CTkLabel(self.pane_register, text='Regester account', font=('Calibri', 18))
        self.newtext.pack(pady=12, padx=10)
        self.user_entry = ctk.CTkEntry(self.pane_register, placeholder_text="Username")
        self.user_entry.pack(pady=12, padx=10)
        self.user_pass = ctk.CTkEntry(self.pane_register, placeholder_text="Password", show="*")
        self.user_pass.pack(pady=12, padx=10)
        self.checkbox = ctk.CTkCheckBox(self.pane_register, text='Show passowrd', command=self.show_pass)
        self.checkbox.pack(pady=12, padx=10)
        self.button = ctk.CTkButton(self.pane_register, text='Regester', command=self.insert)
        self.button.pack(pady=12, padx=10)

        self.button_email.configure(fg_color='black')
        self.newtext.pack(pady=12, padx=10)
        self.sender_entry = ctk.CTkEntry(self.pane_email, placeholder_text='Sender')
        self.sender_entry.pack(pady=6, padx=100, fill='both')
        self.sender_pass = ctk.CTkEntry(self.pane_email, placeholder_text='Sender password', show='*')
        self.sender_pass.pack(pady=6, padx=100, fill='both')
        self.checkbox2 = ctk.CTkCheckBox(self.pane_email, text='Show passowrd', command=self.show_pass)
        self.checkbox2.pack(pady=12, padx=10)
        self.reciever_entry = ctk.CTkEntry(self.pane_email, placeholder_text='Reciever')
        self.reciever_entry.pack(pady=6, padx=100, fill='both')
        self.text_entry = ctk.CTkEntry(self.pane_email, placeholder_text='text', width=400, height=100)
        self.text_entry.pack(pady=15, padx=50)
        self.s_button = ctk.CTkButton(self.pane_email, text='Send', command=self.send_button)
        self.s_button.pack(pady=12, padx=10)
        
    def login(self):
        self.pane_register.pack_forget()
        self.pane_email.pack_forget()
        self.pane_login.pack(pady=0, padx=30, fill=ctk.BOTH, expand=ctk.TRUE)
        self.button_reg.configure(fg_color= 'black')
        self.button_email.configure(fg_color= 'black')
        self.button_log.configure(fg_color= 'navyblue')
        
    def regester(self):
        self.pane_login.pack_forget()
        self.pane_email.pack_forget()
        self.pane_register.pack(pady=0, padx=30, fill=ctk.BOTH, expand=ctk.TRUE)
        self.button_reg.configure(fg_color= 'navyblue')
        self.button_log.configure(fg_color= 'black')
        self.button_email.configure(fg_color= 'black')
        
    def email(self):
        self.pane_register.pack_forget()
        self.pane_login.pack_forget()
        self.pane_email.pack(pady=0, padx=30, fill=ctk.BOTH, expand=ctk.TRUE)
        self.button_email.configure(fg_color= 'navyblue')
        self.button_log.configure(fg_color= 'black')
        self.button_reg.configure(fg_color= 'black')
        
    def send_button(self):
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=self.sender_entry.get(), password=self.sender_pass.get())
        try:
            connection.sendmail(
                from_addr=self.sender_entry.get(),
                to_addrs= self.reciever_entry.get(),
                msg= self.text_entry.get()
            )
            connection.close()
            tkm.showinfo(title= "Sent successful", message="Your message sent successfully.")
        except:
            tkm.showerror(title= "Not sent", message="Something went wrong! Try again.")

    def show_pass(self):
        if self.checkbox.get():
            self.user_pass.configure(show='')
        else:
            self.user_pass.configure(show='*')

        if self.checkbox1.get():
            self.user_pass1.configure(show='')
        else:
            self.user_pass1.configure(show='*')

        if self.checkbox2.get():
            self.sender_pass.configure(show='')
        else:
            self.sender_pass.configure(show='*')

    def insert(self):
        stmt = self.user.insert().values(username= self.user_entry.get(), password= self.user_pass.get())
        with self.engine.begin() as conn:
            conn.execute(stmt)
        tkm.showinfo(title='Register successful', message='You have regestered successfully.')

    def select(self):
        try:
            for i in range(1,21):
                stmt = self.user.select().where(self.user.c.code == i)
                with self.engine.begin() as conn:
                    for row in conn.execute(stmt):
                        row = list(row)
                        if row[1] == self.user_entry1.get() and row[2] == self.user_pass1.get():
                            tkm.showinfo(title='Login successful', message='You have loged in successfully.')
                            t = False
            if t:
                raise TypeError
                        
        except:
            tkm.showerror(title='Login unsuccessful', message='Your username or password is wrong.')


root = App()
root.mainloop()
