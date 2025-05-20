import customtkinter as ctk
from PIL import Image
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")
import sqlite3
with sqlite3.connect("login.db") as db:
    cursor = db.cursor()
cursor.execute(""" CREATE TABLE OF NOT EXISTS users(id integer PRIMARY
KEY AUTOINCREMENT, username text NOT NULL, passowrd text NOT NULL); """)

class NEA(ctk.CTk):
    def openpage(self,current,page): 
        current.place_forget() 
        page.place(relwidth=1, relheight=1) 
    def __init__(self):
        super().__init__()
        self.state('zoomed')          # standards across all pages
        self.geometry('1920x1080')
        self.title("UniPicker")
        self.configure(fg_color="white")
        

 

        self.after(100, lambda: self.lift())              #opens python file to front in macos
        self.after(100, lambda: self.focus_force())   #macos
        self.after(100, lambda: self.attributes('-topmost', True))  #macos
        self.after(500, lambda: self.attributes('-topmost', False)) #macos
        

        class Greeting(ctk.CTkLabel):
            def __init__(self,parent):
                logo_image = ctk.CTkImage(light_image=Image.open("Untitled-2.png"),size=(350,250))
                super().__init__(parent,image=logo_image,text="")
        class loginpage(ctk.CTkFrame):
            def verifylogin(self):
                emailcheck = self.email_form.get()
                passcheck = self.password_form.get()
            def __init__(self,parent,controller):
                super().__init__(parent)
                self.configure(fg_color="#25995e")
                self.controller = controller
                self.greeting = Greeting(self)
                self.greeting.pack(pady=20)



                self.form_frame = ctk.CTkFrame(self,border_color="#2b2b2b",fg_color="white",corner_radius=12)
                self.form_frame.place(relx=0.5,rely=0.53,anchor="center")
                #log in
                self.logintext_frame = ctk.CTkFrame(self.form_frame,fg_color="white")
                self.logintext_frame.pack(pady=50,padx=20,anchor="w")

                self.logintext = ctk.CTkLabel(self.logintext_frame,text="Login", font=("Tahoma",40,"bold"),text_color="black",fg_color="white")
                self.logintext.pack(anchor="w")
                self.logintext1 = ctk.CTkLabel(self.logintext_frame,text="Sign in to continue.", font=("Tahoma",14),text_color="gray",fg_color="white")
                self.logintext1.pack(anchor="w")
                #email box
                self.email_text = ctk.CTkLabel(self.form_frame, text="Email Address", font=("tahoma",18), text_color="black", fg_color= "white") 
                self.email_text.pack(anchor="w",padx=28)

                self.email_form = ctk.CTkEntry(self.form_frame, font= ("Tahoma",20,"normal"), placeholder_text="Email Address",width=500,height=50,border_width=0,fg_color='lightgrey',corner_radius=10 ) 
                self.email_form.pack(padx=15)
                        #password box


                self.password_form_frame = ctk.CTkFrame(self.form_frame,fg_color="white")
                self.password_form_frame.pack(anchor="w",pady=30,padx=10,fill="x")
                self.innerpassword_frame = ctk.CTkFrame(self.password_form_frame,fg_color="white")
                self.innerpassword_frame.pack(anchor="w",fill = "x")
                self.forgotpassword = ctk.CTkLabel(self.innerpassword_frame,text="Forgot Password?",text_color="green",fg_color="white",font=("Tahoma",15,"underline"),cursor="hand2")
                self.forgotpassword.pack(anchor="e",side="right",padx=20,pady=0)
                self.password_text = ctk.CTkLabel(self.innerpassword_frame,text="Password", font=("tahoma",18),text_color="black",fg_color="white")
                self.password_text.pack(anchor="w",side="left",padx=20)

                self.password_form = ctk.CTkEntry(self.password_form_frame, font= ("Tahoma",20,"normal"), placeholder_text="Password",show="*",text_color='black',fg_color='lightgrey',width=500,height=50,border_width=0,corner_radius=10)
                self.password_form.pack(padx=15,pady=0)
        






                self.signupcheckform = ctk.CTkFrame(self.form_frame, fg_color="white")
                self.signupcheckform.pack(anchor="center",pady=0, padx=10)
                self.loginbtn = ctk.CTkButton(self.form_frame, text="Login",font=("Tahoma",20,"bold"),text_color="white",cursor="hand2",fg_color="#25995e",width=450,height=50,corner_radius=10,command=self.passwordchecker)
                self.loginbtn.pack(pady=20,padx=0)

                self.signupcheck = ctk.CTkLabel(self.signupcheckform, text="New to Unipicker?", text_color="black", fg_color="white", font=("Tahoma",16))
                self.signupcheck1 = ctk.CTkLabel(self.signupcheckform, text="Join Now", text_color="green", fg_color="white", font=("Tahoma",16,"bold"), cursor="hand2")
                self.signupcheck1.bind("<Button-1>",lambda event: self.controller.openpage(self,self.controller.signuppage))
                self.signupcheck.pack(side="left", padx=2, anchor="center")
                self.signupcheck1.pack(side="left", padx=2, anchor="center")
            def passwordchecker(self):
                if self.email_form.get() == "test":
                    self.controller.openpage(self,self.controller.otherpage)
                    print("fix")


                
                
                
                
                
            
        class signuppage(ctk.CTkFrame):
            def __init__(self,parent,controller):
                super().__init__(parent)
                self.controller = controller
                self.configure(fg_color="#25995e")
                self.greeting = Greeting(self)
                self.greeting.pack(pady=20)
                                
                                
                self.form_frame = ctk.CTkFrame(self,border_color="#2b2b2b",fg_color="white",corner_radius=12)
                self.form_frame.place(relx=0.5,rely=0.53,anchor="center")


                self.signuptext = ctk.CTkLabel(self.form_frame,text="Sign Up", font=("Tahoma",40,"bold"),text_color="black",fg_color="white")
                self.signuptext.pack(anchor="w",pady=40,padx=20)

                self.name_text = ctk.CTkLabel(self.form_frame, text="Name", font=("tahoma",18), text_color="black", fg_color= "white") 
                self.name_text.pack(anchor="w",padx=20)
                self.name_form = ctk.CTkEntry(self.form_frame, font= ("Tahoma",20,"normal"), width=500,height=50,border_width=0,fg_color='lightgrey',corner_radius=10 ) 
                self.name_form.pack(padx=15)

                self.email_frame = ctk.CTkFrame(self.form_frame,fg_color="white")
                self.email_frame.pack(anchor="w",pady=10,padx=0,fill="x")
                self.email_text = ctk.CTkLabel(self.email_frame, text="Email Address", font=("tahoma",18), text_color="black", fg_color= "white") 
                self.email_text.pack(anchor="w",padx=20)
                self.email_form = ctk.CTkEntry(self.email_frame, font= ("Tahoma",20,"normal"), width=500,height=50,border_width=0,fg_color='lightgrey',corner_radius=10 ) 
                self.email_form.pack(padx=15)



                self.password_form_frame = ctk.CTkFrame(self.form_frame,fg_color="white")
                self.password_form_frame.pack(anchor="w",pady=0,padx=10,fill="x")
                self.innerpassword_frame = ctk.CTkFrame(self.password_form_frame,fg_color="white")
                self.innerpassword_frame.pack(anchor="w",fill = "x")
                self.password_text = ctk.CTkLabel(self.innerpassword_frame,text="Password", font=("tahoma",18),text_color="black",fg_color="white")
                self.password_text.pack(anchor="w",side="left",padx=20)

                self.password_form = ctk.CTkEntry(self.password_form_frame, font= ("Tahoma",20,"normal"), show="*",text_color='white',fg_color='lightgrey',width=500,height=50,border_width=0,corner_radius=10)
                self.password_form.pack(padx=15,pady=0)






                self.signupcheckform = ctk.CTkFrame(self.form_frame, fg_color="white")
                self.signupcheckform.pack(anchor="center",pady=0, padx=10)
                self.loginbtn = ctk.CTkButton(self.form_frame, text="Login",font=("Tahoma",20,"bold"),text_color="white",cursor="hand2",fg_color="#25995e",width=450,height=50,corner_radius=10)
                self.loginbtn.pack(pady=20,padx=0)

                self.signupcheck = ctk.CTkLabel(self.signupcheckform, text="Already have an account?", text_color="black", fg_color="white", font=("Tahoma",16))
                self.signupcheck1 = ctk.CTkLabel(self.signupcheckform, text="Sign in", text_color="green", fg_color="white", font=("Tahoma",16,"bold"), cursor="hand2")
                self.signupcheck1.bind("<Button-1>",lambda event: self.controller.openpage(self,self.controller.loginpage))
                self.signupcheck.pack(side="left", padx=2, anchor="center")
                self.signupcheck1.pack(side="left", padx=2, anchor="center")
        class otherpage(ctk.CTkFrame):
            def __init__(self,parent,controller):
                super().__init__(parent)
                self.configure(fg_color="#25995e")
                self.controller = controller
        self.otherpage = otherpage(parent=self,controller=self)
        self.loginpage = loginpage(parent=self,controller=self)
        self.signuppage = signuppage(parent=self,controller=self)
        self.loginpage.place(relwidth=1,relheight=1)
                
                
                








        
class loginpage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#25995e")

        self.email_form = ctk.CTkEntry(self, placeholder_text="Email Address", width=500, height=50)
        self.email_form.pack()

        self.password_form = ctk.CTkEntry(self, placeholder_text="Password", width=500, height=50, show="*")
        self.password_form.pack()

        self.login_button = ctk.CTkButton(self, text="Login", command=self.verify_login)
        self.login_button.pack()

    def verify_login(self):
        email = self.email_form.get()
        password = self.password_form.get()

        with sqlite3.connect("login.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            user = cursor.fetchone()

        if user:
            print("Login successful")
            self.controller.openpage(self, SomeOtherPage)  # Navigate to another page
        else:
            print("Invalid credentials")        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
app = NEA()
app.mainloop()