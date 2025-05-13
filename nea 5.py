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
                super().__init__(parent,text="UniPicker",text_color="green",font=("tahoma",70,"bold"))
        class basepage(ctk.CTkFrame):
            def __init__(self,parent):
                super().__init__(parent)
                self.greeting = Greeting(self)
                self.greeting.place(relx=0.5,y=100,anchor="center")
                self.configure(fg_color="white")


                self.login = ctk.CTkButton(self, text = "Log In", fg_color = "green", font = ("tahoma",35))
                self.login.place(relx = 0.5,y = 400,anchor = "center") 
                self.signup = ctk.CTkButton(self, text = "Sign up", fg_color= "green", font = ("tahoma",35),corner_radius=12 )
                self.signup.place(relx = 0.5,y = 600,anchor = "center")


        self.page = basepage(self)
        self.page.pack(fill="both", expand=True) 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
app = NEA()
app.mainloop()