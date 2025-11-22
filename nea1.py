import customtkinter as ctk
from tkinter import messagebox #confirmation 
import re # for valid email pattern
import sqlite3 #db
import hashlib #hashes

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Modern Color Palette
COLORS = {
    "primary": "#6366f1",        # Indigo
    "primary_hover": "#4f46e5",  # Darker indigo
    "secondary": "#10b981",      # Emerald
    "background": "#f8fafc",     # Light gray
    "surface": "#ffffff",        # White
    "text_dark": "#1e293b",      # Slate
    "text_gray": "#64748b",      # Gray
    "border": "#e2e8f0",         # Light border
    "success": "#10b981",        # Green
    "error": "#ef4444"            # Red
}



class NEA(ctk.CTk):
    def openpage(self,current,page): 
        current.place_forget() 
        page.place(relwidth=1, relheight=1)
    def quiztaken(self,user_id,currentpage): # checks if user has taken quiz
        self.current_user_id = user_id  # stores current user id
        self.cursor.execute("SELECT quiz_taken FROM users WHERE id = ?",(user_id,)) #Checks database for it quiz has been taken
        result = self.cursor.fetchone() # fetches result
        if result and result[0] == 0: # if quiz not taken
            self.openpage(currentpage, self.quizpage)
        else: # if quiz taken
            self.openpage(currentpage, self.mainpage)
    def save_quiz_answers(self,quiz_answers):
        for question_num, answer in quiz_answers.items():
            if isinstance(answer, list):
                answer = ', '.join(answer)
            self.cursor.execute("INSERT INTO quiz_answers (user_id, question_num, answer) VALUES (?, ?, ?)", (self.current_user_id, question_num, answer))
        self.db.commit()
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
        self.current_user_id = None  # stores current user id

        
        self.mainpage = mainpage(parent=self,controller=self)
        self.quizpage = quizpage(parent=self,controller=self)
        self.loginpage = loginpage(self.db,self.cursor,parent=self,controller=self)
        self.signuppage = signuppage(self.db,self.cursor,parent=self,controller=self)
        self.loginpage.place(relwidth=1,relheight=1)
class loginpage(ctk.CTkFrame):
    def __init__(self,db,cursor,parent,controller):
        super().__init__(parent)
        self.configure(fg_color=COLORS["background"])
        self.controller = controller
        self.db = db
        self.cursor = cursor

        # Centered container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Logo with emoji and modern styling
        self.unipicker = ctk.CTkLabel(container,text="🎓 UniPicker",text_color=COLORS["primary"],font=("Inter",80,"bold"))
        self.unipicker.pack(pady=(0, 10))
        
        # Tagline
        tagline = ctk.CTkLabel(container, text="Find your perfect university match", 
                              text_color=COLORS["text_gray"], font=("Inter", 16))
        tagline.pack(pady=(0, 40))
        
        # Form card with subtle shadow effect
        self.form_frame = ctk.CTkFrame(container, fg_color=COLORS["surface"], 
                                      corner_radius=24, border_width=1, border_color=COLORS["border"])
        self.form_frame.pack()
        
        # Header section
        self.logintext_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.logintext_frame.pack(pady=(50, 10), padx=50, anchor="w")

        self.logintext = ctk.CTkLabel(self.logintext_frame, text="Welcome back", 
                                     font=("Inter", 36, "bold"), text_color=COLORS["text_dark"])
        self.logintext.pack(anchor="w")
        self.logintext1 = ctk.CTkLabel(self.logintext_frame, text="Sign in to continue your journey", 
                                      font=("Inter", 15), text_color=COLORS["text_gray"])
        self.logintext1.pack(anchor="w", pady=(5, 0))
        
        # Email input with label
        email_container = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        email_container.pack(pady=(30, 0), padx=50)
        
        email_label = ctk.CTkLabel(email_container, text="Email address", 
                                  font=("Inter", 14, "bold"), text_color=COLORS["text_dark"])
        email_label.pack(anchor="w", pady=(0, 8))
        
        self.email_form = ctk.CTkEntry(email_container, font=("Inter", 16), 
                                      placeholder_text="you@example.com", 
                                      width=550, height=56, border_width=2,
                                      fg_color=COLORS["background"], 
                                      border_color=COLORS["border"],
                                      corner_radius=12)
        self.email_form.pack()
        
        # Password input with label
        pass_container = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        pass_container.pack(pady=(20, 0), padx=50)
        
        pass_label = ctk.CTkLabel(pass_container, text="Password", 
                                 font=("Inter", 14, "bold"), text_color=COLORS["text_dark"])
        pass_label.pack(anchor="w", pady=(0, 8))
        
        self.password_form = ctk.CTkEntry(pass_container, font=("Inter", 16), 
                                         placeholder_text="Enter your password", show="●",
                                         width=550, height=56, border_width=2,
                                         fg_color=COLORS["background"],
                                         border_color=COLORS["border"],
                                         corner_radius=12)
        self.password_form.pack()
        
        # Forgot password link
        self.forgotpassword = ctk.CTkLabel(pass_container, text="Forgot password?", 
                                          text_color=COLORS["primary"], 
                                          font=("Inter", 13, "bold"), cursor="hand2")
        self.forgotpassword.pack(anchor="e", pady=(8, 0))
        self.forgotpassword.bind("<Enter>", lambda e: self.forgotpassword.configure(text_color=COLORS["primary_hover"]))
        self.forgotpassword.bind("<Leave>", lambda e: self.forgotpassword.configure(text_color=COLORS["primary"]))

        # Login button with hover effect
        self.loginbtn = ctk.CTkButton(self.form_frame, text="Sign in →", 
                                     font=("Inter", 18, "bold"), text_color="white", 
                                     cursor="hand2", fg_color=COLORS["primary"], 
                                     hover_color=COLORS["primary_hover"],
                                     width=550, height=56, corner_radius=12, 
                                     command=self.accountchecker)
        self.loginbtn.pack(pady=(35, 0), padx=50)
        
        # Sign up section
        self.signupcheckform = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.signupcheckform.pack(pady=(25, 50), padx=50)

        self.signupcheck = ctk.CTkLabel(self.signupcheckform, text="New to UniPicker?  ", 
                                       text_color=COLORS["text_gray"], font=("Inter", 15))
        self.signupcheck1 = ctk.CTkLabel(self.signupcheckform, text="Create account", 
                                        text_color=COLORS["primary"], 
                                        font=("Inter", 15, "bold"), cursor="hand2")
        self.signupcheck1.bind("<Button-1>", lambda event: self.controller.openpage(self, self.controller.signuppage))
        self.signupcheck1.bind("<Enter>", lambda e: self.signupcheck1.configure(text_color=COLORS["primary_hover"]))
        self.signupcheck1.bind("<Leave>", lambda e: self.signupcheck1.configure(text_color=COLORS["primary"]))
        
        self.signupcheck.pack(side="left")
        self.signupcheck1.pack(side="left")
        
    def accountchecker(self):
        emailcheck = self.email_form.get()
        passcheck = self.password_form.get()
        self.cursor.execute("SELECT Password FROM users WHERE Email = ?", (emailcheck, )) # finds email
        result = self.cursor.fetchone() # stores results
        if passcheck == "" or emailcheck == "": # checks fields arent empty
            messagebox.showinfo("Error", "Email/Password cannot be blank")
            return
        if result: # if a result is found
            stored_password = result[0]
            hashed_password = hashlib.sha256(passcheck.encode()).hexdigest()
            if hashed_password == stored_password:
                print("Success")
                self.cursor.execute("SELECT id FROM users WHERE Email = ?", (emailcheck, )) # finds email
                result1 = self.cursor.fetchone() # stores results
                messagebox.showinfo("Login", "Login successful")
                self.controller.quiztaken(result1[0],self) 
                print(result1[0]) # prints user id
            else:
                print("fail")
                messagebox.showinfo("Error", "Incorrect email or password")
        if not result: # if no result is found
            messagebox.showinfo("Error", "Incorrect email or password")
    
    
class signuppage(ctk.CTkFrame):
    def __init__(self,db,cursor,parent,controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=COLORS["background"])
        self.db = db 
        self.cursor = cursor
        
        # Centered container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo and tagline
        self.unipicker = ctk.CTkLabel(container, text="🎓 UniPicker", 
                                     text_color=COLORS["primary"], font=("Inter", 70, "bold"))
        self.unipicker.pack(pady=(0, 8))
        
        tagline = ctk.CTkLabel(container, text="Join thousands finding their perfect university", 
                              text_color=COLORS["text_gray"], font=("Inter", 15))
        tagline.pack(pady=(0, 35))
        
        # Form card
        self.form_frame = ctk.CTkFrame(container, fg_color=COLORS["surface"], 
                                      corner_radius=24, border_width=1, border_color=COLORS["border"])
        self.form_frame.pack()
        
        # Header
        self.signuptext_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.signuptext_frame.pack(pady=(45, 10), padx=50, anchor="w")

        self.signuptext = ctk.CTkLabel(self.signuptext_frame, text="Create your account", 
                                      font=("Inter", 36, "bold"), text_color=COLORS["text_dark"])
        self.signuptext.pack(anchor="w")
        self.signuptext1 = ctk.CTkLabel(self.signuptext_frame, text="Start your university journey today", 
                                       font=("Inter", 15), text_color=COLORS["text_gray"])
        self.signuptext1.pack(anchor="w", pady=(5, 0))

        # Name input
        name_container = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        name_container.pack(pady=(25, 0), padx=50)
        
        name_label = ctk.CTkLabel(name_container, text="Full name", 
                                 font=("Inter", 14, "bold"), text_color=COLORS["text_dark"])
        name_label.pack(anchor="w", pady=(0, 8))
        
        self.name_form = ctk.CTkEntry(name_container, font=("Inter", 16), 
                                     placeholder_text="John Smith",
                                     width=550, height=56, border_width=2,
                                     fg_color=COLORS["background"],
                                     border_color=COLORS["border"],
                                     corner_radius=12)
        self.name_form.pack()

        # Email input
        email_container = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        email_container.pack(pady=(18, 0), padx=50)
        
        email_label = ctk.CTkLabel(email_container, text="Email address", 
                                  font=("Inter", 14, "bold"), text_color=COLORS["text_dark"])
        email_label.pack(anchor="w", pady=(0, 8))
        
        self.email_form = ctk.CTkEntry(email_container, font=("Inter", 16), 
                                      placeholder_text="you@example.com",
                                      width=550, height=56, border_width=2,
                                      fg_color=COLORS["background"],
                                      border_color=COLORS["border"],
                                      corner_radius=12)
        self.email_form.pack()

        # Password input
        pass_container = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        pass_container.pack(pady=(18, 0), padx=50)
        
        pass_label = ctk.CTkLabel(pass_container, text="Password", 
                                 font=("Inter", 14, "bold"), text_color=COLORS["text_dark"])
        pass_label.pack(anchor="w", pady=(0, 8))
        
        self.password_form = ctk.CTkEntry(pass_container, font=("Inter", 16), 
                                         placeholder_text="Minimum 10 characters", show="●",
                                         width=550, height=56, border_width=2,
                                         fg_color=COLORS["background"],
                                         border_color=COLORS["border"],
                                         corner_radius=12)
        self.password_form.pack()
        
        # Password requirements
        pass_hint = ctk.CTkLabel(pass_container, 
                                text="Must include uppercase, lowercase, and number", 
                                font=("Inter", 12), text_color=COLORS["text_gray"])
        pass_hint.pack(anchor="w", pady=(8, 0))

        # Sign up button
        self.loginbtn = ctk.CTkButton(self.form_frame, text="Create account →", 
                                     font=("Inter", 18, "bold"), text_color="white",
                                     cursor="hand2", fg_color=COLORS["primary"],
                                     hover_color=COLORS["primary_hover"],
                                     width=550, height=56, corner_radius=12, 
                                     command=self.signup_user)
        self.loginbtn.pack(pady=(30, 0), padx=50)
        
        # Sign in link
        self.signupcheckform = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.signupcheckform.pack(pady=(20, 45), padx=50)

        self.signupcheck = ctk.CTkLabel(self.signupcheckform, text="Already have an account?  ", 
                                       text_color=COLORS["text_gray"], font=("Inter", 15))
        self.signupcheckbutton = ctk.CTkLabel(self.signupcheckform, text="Sign in", 
                                             text_color=COLORS["primary"], 
                                             font=("Inter", 15, "bold"), cursor="hand2")
        self.signupcheckbutton.bind("<Button-1>", lambda event: self.controller.openpage(self, self.controller.loginpage))
        self.signupcheckbutton.bind("<Enter>", lambda e: self.signupcheckbutton.configure(text_color=COLORS["primary_hover"]))
        self.signupcheckbutton.bind("<Leave>", lambda e: self.signupcheckbutton.configure(text_color=COLORS["primary"]))
        
        self.signupcheck.pack(side="left")
        self.signupcheckbutton.pack(side="left")

    # Validation functions
    def validname(self,name): 
        if len(name) < 2 or len(name) > 15: # checks name length
            messagebox.showinfo("Error", "Name must be between 2 and 15 characters long")
            return False
        if not name.isalpha(): # can only contain letter and spaces
            messagebox.showinfo("Error", "Name must contain only letters and spaces!")
            return False
        else:
            return True
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
            messagebox.showinfo("Error", "Name/Username/Password cannot be blank")
            return
        if not self.validname(newname):
            return
        if not self.validemail(newuser):
            messagebox.showinfo("Error", "Invalid email format")
        else: 
            self.cursor.execute("SELECT Email FROM users WHERE Email = ?", (newuser, )) # finds email
            result = self.cursor.fetchone() # stores results
            if result: # if a result is found
                messagebox.showinfo("Error", "Email already exists")
                return
            if self.validpass(newpass) is False: # checks if password is valid via validpass function
                print("Password not valid!")
            else:
                self.hashedpass = self.passwordhasher(newpass)
                self.cursor.execute("INSERT INTO users (Name,Email,Password) VALUES (?, ?, ?)", (newname,newuser, self.hashedpass)) # inserts new user
                self.db.commit()
                messagebox.showinfo("Success!","user registered success!")
                self.cursor.execute("SELECT id FROM users WHERE email = ?", (newuser,))
                result1 = self.cursor.fetchone() # fetch user id

                if result1:
                    user_id = result1[0] # get user id
                    self.controller.quiztaken(user_id, self)

                    
class quizpage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color=COLORS["background"])
        self.controller = controller
        
        # Modern header
        self.header = ctk.CTkFrame(self, fg_color=COLORS["primary"], height=0.2)
        self.header.place(relx=0, rely=0, relwidth=1, relheight=0.13)
        
        # Logo and badge
        logo_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        logo_frame.place(anchor="w", rely=0.5, relx=0.04)
        
        self.logintext = ctk.CTkLabel(logo_frame, text="🎓 UniPicker", 
                                     font=("Inter", 45, "bold"), text_color="white")
        self.logintext.pack(side="left")
        
        badge = ctk.CTkLabel(logo_frame, text="Quiz", 
                            font=("Inter", 14, "bold"), text_color=COLORS["primary"],
                            fg_color="white", corner_radius=8, padx=12, pady=4)
        badge.pack(side="left", padx=15)
        
        # Modern sign out button
        signoutbutton = ctk.CTkButton(self.header, text="Sign out", 
                                     font=("Inter", 16, "bold"), 
                                     text_color=COLORS["primary"],
                                     fg_color="white",
                                     hover_color=COLORS["background"],
                                     cursor="hand2", corner_radius=10,
                                     width=110, height=42,
                                     command=lambda: self.controller.openpage(self, self.controller.loginpage))
        signoutbutton.place(anchor="e", rely=0.5, relx=0.96)
        
        # Body with subtle background
        self.scrollableframe = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        self.scrollableframe.place(relx=0, rely=0.13, relwidth=1, relheight=0.87)

        self.quiz_answers = {}
        self.current_question_index = 0
        self.universitylist = [
            "University of Oxford", "University of Cambridge", "Imperial College London",
            "London School of Economics and Political Science", "University College London (UCL)", "University of Edinburgh",
            "University of Manchester", "Kings College London", "University of Bristol", "University of Glasgow",
        ]
        self.questions = [
            {
                "text": "Are you interested in any potential universities?",
                "type": "multi",
                "questionnumber": 1,
                "options": self.universitylist,
                "handler": self.multi_selected
            },
            {
                "text": "Do you plan on staying at home or moving away for university?",
                "type": "single",
                "questionnumber": 2,
                "options": ["Staying at home", "Moving away", "Not sure"],
                "handler": self.single_selected
            },
            {
                "text": "What is your postcode? (For location-based recommendations)",
                "type": "text",
                "questionnumber": 3,
                "handler": self.postcode_selected,
            },
            {
                "text": "Do you require financial information?",
                "type": "single",
                "questionnumber": 4,
                "options": ["Yes", "No"],
                "handler": self.single_selected
            },
            {
                "text": "Do you prefer a city or campus university?",
                "type": "single",
                "questionnumber": 5,
                "options": ["City", "Campus", "No preference"],
                "handler": self.single_selected
            },
            {
                "text": "What is your preferred study duration?",
                "type": "single",
                "questionnumber": 6,
                "options": ["3 Years", "4 Years(masters/industry/scotland)", "No preference"],
                "handler": self.single_selected
            },
            {
                "text": "Are you interested in any of the following?",
                "type": "multi",
                "questionnumber": 7,
                "options": ["Masters Degree", "Placement Year", "Study Abroad", "Scotland degree(4 years)"],
                "handler": self.multi_selected
            },
        ]
        # Progress indicator
        progress_frame = ctk.CTkFrame(self.scrollableframe, fg_color="transparent")
        progress_frame.pack(pady=(30, 15))
        
        self.progress_label = ctk.CTkLabel(progress_frame, text="Question 1 of 7", 
                                          font=("Inter", 15, "bold"), 
                                          text_color=COLORS["text_gray"])
        self.progress_label.pack()
        
        # Question card
        question_card = ctk.CTkFrame(self.scrollableframe, fg_color=COLORS["surface"],
                                    corner_radius=20, border_width=1, border_color=COLORS["border"])
        question_card.pack(pady=20, padx=60, fill="both")
        
        self.question_label = ctk.CTkLabel(question_card, font=("Inter", 28, "bold"), 
                                          text_color=COLORS["text_dark"], wraplength=900)
        self.question_label.pack(pady=(45, 40), padx=50)
        
        # Answer widgets
        self.answer_menu = ctk.CTkOptionMenu(self.scrollableframe, height=60, width=700, 
                                            font=("Inter", 17), values=[],
                                            fg_color=COLORS["primary"],
                                            button_color=COLORS["primary_hover"],
                                            button_hover_color=COLORS["primary"])
        
        self.single_choice_frame = ctk.CTkFrame(self.scrollableframe, fg_color="transparent")
        
        self.postcode_entry = ctk.CTkEntry(self.scrollableframe, font=("Inter", 17), 
                                          placeholder_text="e.g., SW1A 1AA", 
                                          width=700, height=56, border_width=2,
                                          fg_color=COLORS["background"],
                                          border_color=COLORS["border"],
                                          corner_radius=12)
        
        self.continue_button = ctk.CTkButton(self.scrollableframe, text="Continue →", 
                                            font=("Inter", 19, "bold"), 
                                            command=self.next_question, 
                                            width=700, height=56,
                                            fg_color=COLORS["primary"],
                                            hover_color=COLORS["primary_hover"],
                                            corner_radius=12)
        
        self.selected_answers = {}
        self.display_question()

    def display_question(self):
        question = self.questions[self.current_question_index]
        
        # Update progress
        self.progress_label.configure(text=f"Question {self.current_question_index + 1} of {len(self.questions)}")
        
        # Hide/destroy all widgets
        self.answer_menu.pack_forget()
        self.single_choice_frame.pack_forget()
        self.continue_button.pack_forget()
        self.postcode_entry.pack_forget()
        for widget in self.single_choice_frame.winfo_children():
            widget.destroy()

        self.question_label.configure(text=question["text"])

        if question["type"] == "multi":
            # Create modern checkbox cards
            for option in question["options"]:
                var = ctk.IntVar()
                
                option_card = ctk.CTkFrame(self.single_choice_frame, fg_color=COLORS["surface"],
                                          corner_radius=12, border_width=2, border_color=COLORS["border"])
                option_card.pack(fill="x", pady=8, padx=20)
                
                check = ctk.CTkCheckBox(option_card, text=option, 
                                       font=("Inter", 17), variable=var,
                                       fg_color=COLORS["primary"],
                                       hover_color=COLORS["primary_hover"],
                                       border_color=COLORS["border"],
                                       command=lambda choice=option, v=var: self.multi_selected(choice, v))
                check.pack(anchor="w", pady=16, padx=20)
                
            self.single_choice_frame.pack(pady=(20, 30), padx=60, fill="both")
            self.continue_button.pack(pady=(10, 50))

        elif question["type"] == "single":
            # Create modern button grid
            button_grid = ctk.CTkFrame(self.single_choice_frame, fg_color="transparent")
            button_grid.pack(pady=20)
            
            for i, option in enumerate(question["options"]):
                btn = ctk.CTkButton(button_grid, text=option, 
                                   font=("Inter", 17, "bold"),
                                   command=lambda choice=option: question["handler"](choice), 
                                   width=320, height=65,
                                   fg_color=COLORS["surface"],
                                   hover_color=COLORS["primary_hover"],
                                   text_color=COLORS["text_dark"],
                                   border_width=2,
                                   border_color=COLORS["border"],
                                   corner_radius=12)
                
                row = i // 2
                col = i % 2
                btn.grid(row=row, column=col, padx=15, pady=12)
                
            self.single_choice_frame.pack(pady=(20, 50), anchor="center")

        elif question["type"] == "text":
            hint = ctk.CTkLabel(self.scrollableframe, 
                               text="Please enter your full UK postcode", 
                               font=("Inter", 15), text_color=COLORS["text_gray"])
            hint.pack(pady=(20, 10))
            
            self.postcode_entry.pack(pady=(10, 20), anchor="center")
            self.postcode_entry.bind("<Return>", lambda event: question["handler"]())
            self.continue_button.configure(text="Submit →", command=question["handler"])
            self.continue_button.pack(pady=(10, 50))

    def next_question(self):
        current_q = self.questions[self.current_question_index]["questionnumber"] # holds current q number
        current_selection = self.selected_answers.get(self.current_question_index)  # gets current selection
        self.quiz_answers[current_q] = current_selection
        if self.current_question_index < len(self.questions) - 1: # if more questions
            self.current_question_index += 1
            self.display_question()
        else:
            messagebox.showinfo("Quiz Completed", "Please continue to the main page.") # no more questions
            self.controller.save_quiz_answers(self.quiz_answers) # saves quiz answers to db
            print(self.quiz_answers)

    # Handlers for different question types
    def multi_selected(self, choice,var):
        if var.get() == 1: # if selected
            if self.current_question_index not in self.selected_answers: # checks there isnt already a list
                self.selected_answers[self.current_question_index] = [] # assigns empty list
            self.selected_answers[self.current_question_index].append(choice) # adds choice to the answers
        else: # if unselected
            self.selected_answers[self.current_question_index].remove(choice)


    def single_selected(self, choice):
        self.selected_answers[self.current_question_index] = choice
        self.next_question()

    def postcode_selected(self):
        postcode = self.postcode_entry.get().strip()
        if not postcode:
            messagebox.showinfo("Error", "Postcode cannot be blank")
            return
        if not re.match(r'^[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}$', postcode, re.IGNORECASE):
            messagebox.showinfo("Error", "Invalid postcode format")
            return
        self.selected_answers[self.current_question_index] = postcode
        self.next_question()

class mainpage(ctk.CTkFrame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.configure(fg_color=COLORS["background"])
        self.controller = controller
        
        # Header
        header = ctk.CTkFrame(self, fg_color=COLORS["primary"], height=100)
        header.pack(fill="x", side="top")
        
        logo = ctk.CTkLabel(header, text="🎓 UniPicker", 
                           font=("Inter", 45, "bold"), text_color="white")
        logo.place(anchor="w", rely=0.5, relx=0.04)
        
        # Content area
        content = ctk.CTkScrollableFrame(self, fg_color=COLORS["background"])
        content.pack(fill="both", expand=True, padx=50, pady=40)
        
        # Welcome card
        welcome_card = ctk.CTkFrame(content, fg_color=COLORS["surface"],
                                   corner_radius=20, border_width=1, border_color=COLORS["border"])
        welcome_card.pack(fill="x", pady=(0, 30))
        
        welcome_title = ctk.CTkLabel(welcome_card, text="Welcome to Your Dashboard! 🎉", 
                                     font=("Inter", 32, "bold"), 
                                     text_color=COLORS["text_dark"])
        welcome_title.pack(pady=(40, 15), padx=40)
        
        welcome_text = ctk.CTkLabel(welcome_card, 
                                    text="Based on your quiz responses, we've curated personalized university recommendations.", 
                                    font=("Inter", 16), 
                                    text_color=COLORS["text_gray"],
                                    wraplength=900)
        welcome_text.pack(pady=(0, 40), padx=40)

            
                
                



  
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
app = NEA()
app.mainloop()