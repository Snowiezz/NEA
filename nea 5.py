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

        self.after(100, lambda: self.lift())              #macos
        self.after(100, lambda: self.focus_force())   #macos
        self.after(100, lambda: self.attributes('-topmost', True))  #macos
        self.after(500, lambda: self.attributes('-topmost', False)) #macos
        

        class Greeting(ctk.CTkLabel):
            def __init__(self,parent):
                super().__init__(parent,text="UniPicker",text_color="green",font=("tahoma",90,"bold"))
        class loginpage(ctk.CTkFrame):
            def __init__(self,parent):
                super().__init__(parent)
                self.greeting = Greeting(self)
                self.greeting.place(relx=0.5,y=100,anchor="center")
                self.configure(fg_color="white")

                self.bglabel = Image.open("")

                self.form_frame = ctk.CTkFrame(self,border_color="gray",fg_color="white",border_width=1)
                self.form_frame.place(relx=0.5,rely=0.45,anchor="center")
                #log in
                self.logintext = ctk.CTkLabel(self.form_frame,text="Login", font=("Tahoma",80,"bold"),text_color="black",fg_color="white")
                self.logintext.pack(pady=50,padx=50)
                #email box
                self.email_text = ctk.CTkLabel(self.form_frame, text="Email Address", font=("tahoma",15), text_color="black", fg_color= "white") 
                self.email_text.pack(anchor="w",padx=5)

                self.email_form = ctk.CTkEntry(self.form_frame, font= ("Tahoma",20,"normal"), width=550,height=50 ) 
                self.email_form.pack(padx=5)





        self.page = loginpage(self)
        self.page.pack(fill="both", expand=True) 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
app = NEA()
app.mainloop()