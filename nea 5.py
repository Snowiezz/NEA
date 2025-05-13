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

                self.form_frame = ctk.CTkFrame(self,fg_color="white",padx= 20,pady=20,relief="sunken",highlightbackground="dark gray",highlightthickness="2")
                self.form_frame.place(relx=0.5,rely=0.45,anchor="center")
                #log in
                self.logintext = ctk.CTkLabel(self.form_frame,text="Login", font=("Tahoma",47,"bold"),fg="black",bg="white")
                self.logintext.pack(pady=25)





        self.page = loginpage(self)
        self.page.pack(fill="both", expand=True) 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
app = NEA()
app.mainloop()