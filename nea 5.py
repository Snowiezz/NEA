import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")
class NEA(ctk.CTk):
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
                super().__init__(parent,text="UniPicker",text_color="white",font=("tahoma",60,"bold"))
        class loginpage(ctk.CTkFrame):
            def __init__(self,parent):
                super().__init__(parent)
                self.greeting = Greeting(self)
                #self.greeting.place(relx=0.1,y=80,anchor="w")
                self.configure(fg_color="#25995e")

                self.form_frame = ctk.CTkFrame(self,border_color="#2b2b2b",fg_color="white",corner_radius=12)
                self.form_frame.place(relx=0.5,rely=0.5,anchor="center")
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

                self.email_form = ctk.CTkEntry(self.form_frame, font= ("Tahoma",20,"normal"), width=500,height=50,border_width=0,fg_color='#99E3C0',corner_radius=10 ) 
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

                self.password_form = ctk.CTkEntry(self.password_form_frame, font= ("Tahoma",20,"normal"), show="*",text_color='black',fg_color='#99E3C0',width=500,height=50,border_width=0,corner_radius=10)
                self.password_form.pack(padx=15,pady=0)




                self.loginbtn = ctk.CTkButton(self.form_frame, text="Login",font=("Tahoma",20,"bold"),text_color="white",cursor="hand2",fg_color="#25995e",width=450,height=50,corner_radius=10,)
                self.loginbtn.pack(pady=20,padx=0)

                self.signupcheckform = ctk.CTkFrame(self.form_frame, fg_color="white")
                self.signupcheckform.pack(anchor="center",pady=0, padx=10)

                self.signupcheck = ctk.CTkLabel(self.signupcheckform, text="New to Unipicker?", text_color="black", fg_color="white", font=("Tahoma",16))
                self.signupcheck1 = ctk.CTkLabel(self.signupcheckform, text="Join Now", text_color="green", fg_color="white", font=("Tahoma",16,"bold"), cursor="hand2")
                self.signupcheck.pack(side="left", padx=2, anchor="center")
                self.signupcheck1.pack(side="left", padx=2, anchor="center")







        self.page = loginpage(self)
        self.page.pack(fill="both", expand=True) 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
app = NEA()
app.mainloop()