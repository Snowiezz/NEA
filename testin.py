import customtkinter as ctk
import tkintermapview
root = ctk.CTk()
root.geometry("1000x800")

ctk.CTkLabel(root, text="Hello, World!").pack(pady=20)

map_widget = tkintermapview.TkinterMapView(root, width=800, height=600, corner_radius=0)
map_widget.place(relx=0.5, rely=0.5, anchor="center")
root.mainloop()

