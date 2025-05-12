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
        self.login = tk.Button(self, text = "Log In", fg = "black", bg = "light gray", font = ("tahoma",35), borderwidth = 2, relief = "flat", command=lambda: openpage(page1,page2) ) 
        self.login.place(relx = 0.5,y = 400,anchor = "center") 
        self.signup = tk.Button(self, text = "Sign up", fg = "black", bg = "light gray", font = ("tahoma",35), borderwidth = 2, relief = "flat" ,command=lambda:openpage(page1,page3)) 
        self.signup.place(relx = 0.5,y = 600,anchor = "center")
        self.greeting = Greeting(self)
        self.greeting.place(relx=0.5,y=100,anchor="center")

class loginpage(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.configure(bg="white")
        #back button
        self.back_button = tk.Button(self,text="Back",command=lambda: back(self,basepage)) 
        self.back_button.place(relx = 0.05, y=10, anchor="nw") 
        
        #greeting
        self.greeting = Greeting(self)
        self.greeting.place(relx=0.5,y=100,anchor="center")
        #frame
        self.form_frame = tk.Frame(self,bg="grey",padx= 20,pady=20,relief="sunken")
        self.form_frame.place(relx=0.5,rely=0.4,anchor="center")
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

        self.password_form = tk.Entry(self.password_form_frame, font= ("Tahoma",20,"normal"), insertbackground = "grey", highlightcolor = "red", width = 35,fg='black',bg='white' )
        self.password_form.pack()
class signuppage(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.configure(bg="white")
        #back button
        self.back_button = tk.Button(self,text="Back",command=lambda: back(self,basepage)) 
        self.back_button.place(relx = 0.05, y=10, anchor="nw")
        

class app(tk.Tk):
    def __init__(self,parent):
        super().__init__(parent)
        self.state('zoomed')
        self.geometry('1920x1080')
        
        
        self.page = basepage(self)
        basepage.pack(fill="both", expand=True)
        
        
    





root = tk.Tk()
root.geometry('1920x1080')
page1 = basepage(root)
page2 = loginpage(root)
page3 = signuppage(root)
page1.pack(fill="both", expand=True) 
root.mainloop()