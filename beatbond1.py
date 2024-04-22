#libreria 
import customtkinter as ctk
from PIL import Image

# tema
#mainpage
mainpage = ctk.CTk()
mainpage.title("BeatBond")
mainpage.geometry("700x700")

mainpage.config(background='#FBEBC7')

# logo
logo = ctk.CTkImage(light_image=Image.open('images/beatbond_logo.png'), 
                    dark_image=Image.open('images/beatbond_logo.png'),
                    size=(500,500)) # width x height
logo_label = ctk.CTkLabel(mainpage, text="", image=logo)
logo_label.pack(pady=50, padx=20) 

# boton de iniciar
boton_iniciar = ctk.CTkButton(mainpage, text="⭐Empezar⭐", corner_radius=32, fg_color="#D03561", hover_color="#EA516D", border_color='#FFCC70', font=("Helvetica", 50))


boton_iniciar.pack(pady=60)
mainpage.mainloop()