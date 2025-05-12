import tkinter as tk 
from tkinter import * 
import tkinter.ttk as ttk
#functions
def openpage(current,page): 
    current.place_forget() 
    page.place(relwidth=1, relheight=1) 

def back(current,page): 
    current.place_forget() 
    page.place(relwidth=1,relheight=1) 


 


class Greeting(tk.Label):
    def __init__(self,parent):
        super().__init__(parent,text="UniPicker", fg="green", bg="white", font=("tahoma",70,"bold") )

class basepage(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.configure(bg="white")
        self.login = tk.Button(self, text = "Log In", fg = "black", bg = "light gray", font = ("tahoma",35), borderwidth = 2, relief = "flat", command=lambda: openpage(basepage,loginpage) ) 
        self.login.place(relx = 0.5,y = 400,anchor = "center") 
        self.signup = tk.Button(self, text = "Sign up", fg = "black", bg = "light gray", font = ("tahoma",35), borderwidth = 2, relief = "flat" ,command=lambda:openpage(basepage,signuppage)) 
        self.signup.place(relx = 0.5,y = 600,anchor = "center")
        self.greeting = Greeting(self)
        self.greeting.place(relx=0.5,y=100,anchor="center")

class loginpage(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.configure(bg="white")
        #back button
        self.back_button = tk.Button(self,bg="white",text="Back",command=lambda: back(self,basepage)) 
        self.back_button.place(relx = 0.05, y=10, anchor="nw") 
        
        #greeting
        self.greeting = Greeting(self)
        self.greeting.place(relx=0.5,y=100,anchor="center")
        #frame
        self.form_frame = tk.Frame(self,bg="white",padx= 20,pady=20,relief="sunken",highlightbackground="black",highlightthickness="2")
        self.form_frame.place(relx=0.5,rely=0.45,anchor="center")
        #log in
        self.logintext = tk.Label(self.form_frame,text="Login", font=("Tahoma",47,"bold"),fg="green",bg="white")
        self.logintext.pack(pady=25)
        #email box
        self.email_text = tk.Label(self.form_frame, text="Email Address", font=("tahoma",15), fg = "black", bg= "white", ) 
        self.email_text.pack(anchor="w")
        #self.email_form_frame = tk.Frame(self.form_frame, bd=3, bg="grey", relief = "ridge", ) 
        #self.email_form_frame.pack()
        self.email_form = tk.Entry(self.form_frame, font= ("Tahoma",20,"normal"), insertbackground = "grey", highlightcolor = "red", width = 35,fg='black',bg='white' ) 
        self.email_form.pack()
        #password box
        self.password_form_frame = tk.Frame(self.form_frame,bg="white",relief="ridge")
        self.password_form_frame.pack(anchor="w",pady=20)
        self.password_text = tk.Label(self.password_form_frame,text="Password", font=("tahoma",15),fg="black",bg="white")
        self.password_text.pack(anchor="w")

        self.password_form = tk.Entry(self.password_form_frame, font= ("Tahoma",20,"normal"), show="*",insertbackground = "grey", highlightcolor = "red", width = 35,fg='black',bg='white' )
        self.password_form.pack(padx=0,pady=0)
        #forgotpassword
        self.forgotpassword = tk.Label(self.password_form_frame,text="Forgot Password?",fg="gray",bg="white",font=("Tahoma",15,"underline"),cursor="hand1")
        self.forgotpassword.pack(anchor="nw",padx=0,pady=0)

        self.loginbtn = tk.Button(self.form_frame, text="Login",font=("Tahoma",12,"bold"),fg="white",bd=0,relief="flat",cursor="hand2",highlightbackground="Green",bg="white",width=30,height=2)
        self.loginbtn.pack()
        #signupchecker
        self.signupcheck = tk.Label(self,text="New to Unipicker?",fg="black",bg="white",font=("Tahoma",15))
        self.signupcheck.place(rely=0.7,relx=0.47,anchor="center")
        
        self.signupcheck1 = tk.Label(self,text="Join Now",fg="Blue",bg="White",font=("Tahoma",15,"underline"))
        self.signupcheck1.place(rely=0.7,anchor="center",relx=0.53)
        self.signupcheck1.bind("<Button-1>",lambda event:openpage(self,signuppage))

class signuppage(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.configure(bg="white")
        #back button
        self.back_button = tk.Button(self,text="Back",command=lambda: back(self,basepage)) 
        self.back_button.place(relx = 0.05, y=10, anchor="nw")

        self.greeting = Greeting(self)
        self.greeting.place(relx=0.5,y=100,anchor="center")


class app(tk.Tk):
    def __init__(self,parent):
        super().__init__(parent)
        self.state('zoomed')
        self.geometry('1920x1080')
        
        
        self.page = basepage(self)
        basepage.pack(fill="both", expand=True)
        
        
    





root = tk.Tk()
root.geometry('1920x1080')
basepage = basepage(root)
loginpage = loginpage(root)
signuppage = signuppage(root)
basepage.pack(fill="both", expand=True) 
root.mainloop()