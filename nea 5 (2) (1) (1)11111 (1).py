import customtkinter as ctk
from tkinter import messagebox #confirmation 
from PIL import Image #logo
import re # for valid email pattern
import sqlite3 #db
import hashlib #hashes

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")



class NEA(ctk.CTk):
    def openpage(self,current,page): 
        current.place_forget() 
        page.place(relwidth=1, relheight=1)
    def quiztaken(self,user_id,currentpage):
        self.cursor.execute("SELECT quiz_taken FROM users WHERE id = ?",(user_id,))
        result = self.cursor.fetchone()
        if result and result[0] == 0:
            self.openpage(currentpage, self.controller.quizpage)
        else:
            self.openpage(currentpage, self.controller.mainpage)
            


    def __init__(self):
        super().__init__()
        self.state('zoomed')          # standards across all pages
        self.geometry('1920x1080')
        self.title("UniPicker")
        self.configure(fg_color="white")

        #connect to db
        self.db = sqlite3.connect("login.db")
        self.cursor = self.db.cursor()

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
                        self.cursor.execute("SELECT id FROM users WHERE Email = ?", (emailcheck, )) # finds email
                        result1 = self.cursor.fetchone() # stores results
                        messagebox.showinfo("Login", "Login successful")
                        self.controller.quiztaken(self,result1[0]) 
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
            def validpass(self,password):
                if len(password) < 10:
                    messagebox.showinfo("Error", "Password must be above 10 characters!")
                    return False
                if not re.search(r'[A-Z]', password):
                    messagebox.showinfo("Error", "Password must contain at least one uppercase letter!") # checks for uppercase
                    return False
                if not re.search(r'[a-z]', password):
                    messagebox.showinfo("Error", "Password must contain at least one lowercase letter!") # checks for lowercase
                    return False
                if not re.search(r'\d', password):
                    messagebox.showinfo("Error", "Password must contain at least one digit!") # checks for digit
                    return False
                else:
                    return True
                
                
                
                
            
            def passwordhasher(self,password):
                return hashlib.sha256(password.encode()).hexdigest()
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
                    if self.validpass(newpass) is False:
                        print("Password not valid!")
                    else:
                        self.hashedpass = self.passwordhasher(newpass)
                        self.cursor.execute("INSERT INTO users (Name,Email,Password) VALUES (?, ?, ?)", (newname,newuser, self.hashedpass))
                        self.db.commit()
                        messagebox.showinfo("Success!","user registered success!")
                        self.cursor.execute("SELECT id FROM users WHERE email = ?", (newuser,))
                        result1 = self.cursor.fetchone()

                        if result1:
                            user_id = result1[0]
                            self.controller.quiztaken(user_id, self)#
        class quizpage(ctk.CTkFrame):
            def __init__(self,parent,controller):

                super().__init__(parent)
                self.configure(fg_color="white")
                self.controller = controller
                self.header = ctk.CTkFrame(self,fg_color="#25995e",height=0.2)
                self.header.place(relx=0,rely=0,relwidth=1,relheight=0.12)
                self.logintext = ctk.CTkLabel(self.header,text="UniPicker", font=("Tahoma",55,"bold"),text_color="white",fg_color="#25995e")
                self.logintext.place(anchor="w",rely=0.5,relx=0.04)
                self.scrollableframe = ctk.CTkScrollableFrame(self,fg_color="white")
                self.scrollableframe.place(relx=0,rely=0.12,relwidth=1,relheight=0.88)

                self.quiztext = ctk.CTkLabel(self.scrollableframe,text="Quiz",font=("Tahoma",95,"bold"),fg_color="white",text_color="#25995e")
                self.quiztext.pack(anchor="center")
                self.quizquestion1 = ctk.CTkLabel(self.scrollableframe,text="1: What Subjects are you taking?",text_color="#25995e",font=("Tahoma",35,"bold")) #######FINISH
                self.quizquestion1.pack(padx=200, pady=10, anchor="center")

                # Row hold lift of selected subjects
                self.selection_row = ctk.CTkFrame(self.scrollableframe, fg_color="white")
                self.selection_row.pack(pady=(5,2), anchor="center")
                self.selectedsubjectlist = ctk.CTkLabel(
                    self.selection_row,
                    text="You have selected:",
                    text_color="#a3a3a3",
                    font=("Tahoma", 20)
                )
                self.selectedsubjectlist.pack(side="left", padx=(0, 10))
                self.selectedsubjects_frame = ctk.CTkFrame(self.selection_row, fg_color="white")



                self.selectedsubjects = []
                self.update_selected_subjects()


                self.subjectlist = ["Arabic","Art & Design","Biology","Business Studies","Chemistry","Computer Science","Economics","English Language","English Literature","French","Geography",'German',"History","Law","Mathematics","Mathematics-Further","Music","Physics","Psychology","Religious Studies","Sociology","Travel & Tourism"] # list of subjects
                self.quizquestion1ans = ctk.CTkOptionMenu(self.scrollableframe,values=self.subjectlist,height=80,width=500,font=("Tahoma",20),command=self.subject_selected)
                self.quizquestion1ans.set("Choose a subject")
                self.quizquestion1ans.pack(pady=(2,10))
            def remove_subject(self,subject): # removes subject, allows user to click x and cancel subject
                self.selectedsubjects.remove(subject) # removes
                self.update_selected_subjects()# updates list again
            def update_selected_subjects(self):
                for widget in self.selectedsubjects_frame.winfo_children(): # deletes widgets so they dont stack
                    widget.destroy() # destroys widgets
                if not self.selectedsubjects: #if theres no elements
                    self.selectedsubjects_frame.pack_forget() # hides frame when theres no elements
                    self.selectedsubjectlist.configure(text="You have selected: None",font=("Tahoma",20,"bold"))
                else:
                    self.selectedsubjects_frame.pack(side="left")
                    self.selectedsubjectlist.configure(text="You have selected:", font=("Tahoma", 20, "bold"))
                    for subject in self.selectedsubjects:
                        self.container  = ctk.CTkFrame(self.selectedsubjects_frame, fg_color="white") # container allows x to be next to subject
                        self.container.pack(side="left", padx=0, pady=0) # packs container
                        subject_label = ctk.CTkLabel(self.container, text=subject, font=("Tahoma", 20), text_color="grey")
                        subject_label.pack(side="left", padx=5, pady=5) # packs button
                        x_label = ctk.CTkLabel(self.container, text="x", font=("Tahoma", 18,"bold"), text_color="#7C7C7C", cursor="hand2")
                        x_label.pack(side="right", padx=0) # packs x
                        x_label.bind("<Button-1>", lambda event, s=subject: self.remove_subject(s)) # binds click to remove subject
            def subject_selected(self,choice):
                if choice not in self.selectedsubjects:
                    self.selectedsubjects.append(choice) # adds subject to list
                    self.update_selected_subjects()
                else:
                    messagebox.showinfo("Error", "You have already selected this subject")
                self.quizquestion1ans.set("Choose a subject")


        

        class mainpage(ctk.CTkFrame):
            def __init__(self,parent,controller):
                super().__init__(parent)
                self.configure(fg_color="#25995e")
                self.controller = controller

        self.mainpage = mainpage(parent=self,controller=self)
        self.quizpage = quizpage(parent=self,controller=self)
        self.loginpage = loginpage(self.db,self.cursor,parent=self,controller=self)
        self.signuppage = signuppage(self.db,self.cursor,parent=self,controller=self)
        self.quizpage.place(relwidth=1,relheight=1)
                
                
                



  
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
app = NEA()
app.mainloop()

