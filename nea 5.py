import customtkinter as ctk
class Greeting(ctk.CTkLabel):
    def __init__(self,parent):
        super().__init__(parent,text="UniPicker",fg="green",bg="white",font=("tahoma",70,"bold"))
class basepage(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.configure(bg="white")
        self.greeting = Greeting(self)
        self.greeting.place(relx=0.5,y=100,anchor="center")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
root = ctk.CTk()
root.geometry("1920x1080")
root.mainloop()