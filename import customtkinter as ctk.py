import customtkinter as ctk

def openpage(current, page):
    current.place_forget()
    page.place(relwidth=1, relheight=1)

class NEA(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Bind Test")

        class LoginPage(ctk.CTkFrame):
            def __init__(self, parent, controller):
                super().__init__(parent)
                self.controller = controller
                self.configure(fg_color="#ffffff")

                label = ctk.CTkLabel(self, text="Login Page", font=("Tahoma", 24))
                label.pack(pady=30)

                # This label should work with bind
                self.link = ctk.CTkLabel(self, text="Join Now", text_color="blue", cursor="hand2", font=("Tahoma", 18, "underline"))
                self.link.pack()

                # BIND: MUST include `event` even if you don't use it
                self.link.bind("<Button-1>", lambda event: openpage(self, self.controller.signuppage))

        class SignupPage(ctk.CTkFrame):
            def __init__(self, parent, controller):
                super().__init__(parent)
                self.controller = controller
                self.configure(fg_color="#e0ffe0")

                label = ctk.CTkLabel(self, text="Signup Page", font=("Tahoma", 24))
                label.pack(pady=30)

        # Pages
        self.loginpage = LoginPage(parent=self, controller=self)
        self.signuppage = SignupPage(parent=self, controller=self)

        # Show login page first
        self.loginpage.place(relwidth=1, relheight=1)

app = NEA()
app.mainloop()