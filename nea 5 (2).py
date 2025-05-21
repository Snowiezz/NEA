import customtkinter as ctk
from tkinter import messagebox #confirmation 
from PIL import Image #logo
import re # for valid email pattern
import sqlite3 #db

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")



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

        #connect to db
        self.db = sqlite3.connect("login.db")
        self.cursor = self.db.cursor()

        self.cursor.execute(""" CREATE TABLE iF NOT EXISTS users(id integer PRIMARY
KEY AUTOINCREMENT,Name text NOT NULL, Email text NOT NULL, Password text NOT NULL); """) #creates table, autoincrements every time new data added
        self.db.commit()

 

        self.after(100, lambda: self.lift())              #opens python file to front in macos
        self.after(100, lambda: self.focus_force())   #macos
        self.after(100, lambda: self.attributes('-topmost', True))  #macos
        self.after(500, lambda: self.attributes('-topmost', False)) #macos
        

        #class Greeting(ctk.CTkLabel):
        #    def __init__(self,parent):
        #        logo_image = ctk.CTkImage(light_image=Image.open("Untitled-2.png"),size=(350,250))
        #        super().__init__(parent,image=logo_image,text="")
        class loginpage(ctk.CTkFrame):
            def __init__(self,db,cursor,parent,controller):
                super().__init__(parent)
                self.configure(fg_color="#25995e")
                self.controller = controller
          #     self.greeting = Greeting(self)
        #       self.greeting.pack(pady=20)
                self.db = db
                self.cursor = cursor




                self.form_frame = ctk.CTkFrame(self,border_color="#2b2b2b",fg_color="white",corner_radius=12)
                self.form_frame.place(relx=0.5,rely=0.53,anchor="center")
                #log in
                self.logintext_frame = ctk.CTkFrame(self.form_frame,fg_color="white")
                self.logintext_frame.pack(pady=30,padx=20,anchor="w")

                self.logintext = ctk.CTkLabel(self.logintext_frame,text="Login", font=("Tahoma",40,"bold"),text_color="black",fg_color="white")
                self.logintext.pack(anchor="w")
                self.logintext1 = ctk.CTkLabel(self.logintext_frame,text="Sign in to continue.", font=("Tahoma",14),text_color="gray",fg_color="white")
                self.logintext1.pack(anchor="w")
                #email box

                self.email_form = ctk.CTkEntry(self.form_frame, font= ("Tahoma",20,"normal"), placeholder_text="Email Address",width=500,height=70,border_width=0,fg_color='lightgrey',corner_radius=10 ) 
                self.email_form.pack(padx=15)
                        #password box


                self.password_form_frame = ctk.CTkFrame(self.form_frame,fg_color="white")
                self.password_form_frame.pack(anchor="w",pady=20,padx=10,fill="x")



                self.password_form = ctk.CTkEntry(self.password_form_frame, font= ("Tahoma",20,"normal"), placeholder_text="Password",show="*",text_color='black',fg_color='lightgrey',width=500,height=70,border_width=0,corner_radius=10)
                self.password_form.pack(padx=15,pady=0)
                self.forgotpassword = ctk.CTkLabel(self.password_form_frame,text="Forgot Password?",text_color="green",fg_color="white",font=("Tahoma",15,"underline"),cursor="hand2")
                self.forgotpassword.pack(anchor="e",side="right",padx=20,pady=0)
        







                self.loginbtn = ctk.CTkButton(self.form_frame, text="Login",font=("Tahoma",20,"bold"),text_color="white",cursor="hand2",fg_color="#25995e",width=500,height=70,corner_radius=10,command=self.accountchecker)
                self.loginbtn.pack(pady=0,padx=0)
                self.signupcheckform = ctk.CTkFrame(self.form_frame, fg_color="white")
                self.signupcheckform.pack(anchor="center",pady=15, padx=10)

                self.signupcheck = ctk.CTkLabel(self.signupcheckform, text="New to Unipicker?", text_color="black", fg_color="white", font=("Tahoma",16))
                self.signupcheck1 = ctk.CTkLabel(self.signupcheckform, text="Join Now", text_color="green", fg_color="white", font=("Tahoma",16,"bold"), cursor="hand2")
                self.signupcheck1.bind("<Button-1>",lambda event: self.controller.openpage(self,self.controller.signuppage))
                self.signupcheck.pack(side="left", padx=2, anchor="center")
                self.signupcheck1.pack(side="left", padx=2, anchor="center")
                
            def accountchecker(self):
                emailcheck = self.email_form.get()
                passcheck = self.password_form.get()
                self.cursor.execute("SELECT Password FROM users WHERE Email = ?", (emailcheck, )) # finds email
                result = self.cursor.fetchone() # stores results
                if result: # if a result is found
                    stored_password = result[0]
                    if stored_password == passcheck:
                        messagebox.showinfo("Login", "Login successful")
                        self.controller.openpage(self,self.controller.otherpage)
                    else:
                        print("fail")
                        messagebox.showinfo("Error", "Incorrect email or password")
                if not result: # if no result is found
                    messagebox.showinfo("Error", "Incorrect email or password")
            


                


                
                
                
                
                
            
        class signuppage(ctk.CTkFrame):
            def __init__(self,db,cursor,parent,controller):
                super().__init__(parent)
                self.controller = controller
                self.configure(fg_color="#25995e")
                #self.greeting = Greeting(self)
                #self.greeting.pack(pady=20)
                self.db = db 
                self.cursor = cursor
                                
                                
                self.form_frame = ctk.CTkFrame(self,border_color="#2b2b2b",fg_color="white",corner_radius=12)
                self.form_frame.place(relx=0.5,rely=0.53,anchor="center")
 
                self.entryform_frame = ctk.CTkFrame(self.form_frame,fg_color="white")
                self.entryform_frame.pack(pady=20,padx=0)
                self.signuptext_frame = ctk.CTkFrame(self.entryform_frame,fg_color="white") #signuptext is in entry form so padding of entryform doesnt affect signuptext
                self.signuptext_frame.pack(pady=15,padx=20,anchor="w")

                self.signuptext = ctk.CTkLabel(self.signuptext_frame,text="Sign Up", font=("Tahoma",40,"bold"),text_color="black",fg_color="white")
                self.signuptext.pack(anchor="w")
                self.signuptext1 = ctk.CTkLabel(self.signuptext_frame,text="Sign Up to continue.", font=("Tahoma",14),text_color="gray",fg_color="white")
                self.signuptext1.pack(anchor="w")


                self.name_form = ctk.CTkEntry(self.entryform_frame, font= ("Tahoma",20,"normal"),placeholder_text="Name" ,width=500,height=70,border_width=0,fg_color='lightgrey',corner_radius=10 ) 
                self.name_form.pack(padx=15,pady=10)


                self.email_form = ctk.CTkEntry(self.entryform_frame, font= ("Tahoma",20,"normal"),placeholder_text="Email Address" ,width=500,height=70,border_width=0,fg_color='lightgrey',corner_radius=10 ) 
                self.email_form.pack(padx=15,pady=10)



                self.password_form_frame = ctk.CTkFrame(self.entryform_frame,fg_color="white")
                self.password_form_frame.pack(anchor="w",pady=0,padx=10,fill="x")

                self.password_form = ctk.CTkEntry(self.password_form_frame, font= ("Tahoma",20,"normal"), placeholder_text="Password",show="*",text_color='white',fg_color='lightgrey',width=500,height=70,border_width=0,corner_radius=10)
                self.password_form.pack(padx=15,pady=10)







                self.loginbtn = ctk.CTkButton(self.form_frame, text="Sign Up",font=("Tahoma",20,"bold"),text_color="white",cursor="hand2",fg_color="#25995e",width=500,height=70,corner_radius=10,command=self.signup_user)
                self.loginbtn.pack(pady=10,padx=0)
                self.signupcheckform = ctk.CTkFrame(self.form_frame, fg_color="white")
                self.signupcheckform.pack(anchor="center",pady=15, padx=10)

                self.signupcheck = ctk.CTkLabel(self.signupcheckform, text="Already have an account?", text_color="black", fg_color="white", font=("Tahoma",16))
                self.signupcheck1 = ctk.CTkLabel(self.signupcheckform, text="Sign in", text_color="green", fg_color="white", font=("Tahoma",16,"bold"), cursor="hand2")
                self.signupcheck1.bind("<Button-1>",lambda event: self.controller.openpage(self,self.controller.loginpage))
                self.signupcheck.pack(side="left", padx=2, anchor="center")
                self.signupcheck1.pack(side="left", padx=2, anchor="center")
            def validemail(self, email):
                pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # checks if valid email follows email format
                return re.match(pattern, email) is not None # returns true if email is valid
            def signup_user(self):
                newname = self.name_form.get()
                newuser = self.email_form.get()
                newpass = self.password_form.get()
                if not newuser or not newpass or not newname: # checks fields arent empty
                    print("Name/Username/Password cannot be blank")
                    return
                if not self.validemail(newuser):
                    messagebox.showinfo("Error", "Invalid email format")
                else:
                    self.cursor.execute("SELECT Email FROM users WHERE Email = ?", (newuser, )) # finds email
                    result = self.cursor.fetchone() # stores results
                    if result: # if a result is found
                        messagebox.showinfo("Error", "Email already exists")
                        return
                    else:
                        self.cursor.execute("INSERT INTO users (Name,Email,Password) VALUES (?, ?, ?)", (newname,newuser, newpass))
                        self.db.commit()
                        messagebox.showinfo("Success!","user registered success!")

        class otherpage(ctk.CTkFrame):
            def __init__(self,parent,controller):
                super().__init__(parent)
                self.configure(fg_color="#25995e")
                self.controller = controller
        self.otherpage = otherpage(parent=self,controller=self)
        self.loginpage = loginpage(self.db,self.cursor,parent=self,controller=self)
        self.signuppage = signuppage(self.db,self.cursor,parent=self,controller=self)
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
  
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
app = NEA()
app.mainloop()