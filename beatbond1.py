import customtkinter as ctk
from PIL import Image, ImageTk

def option_page():
    option_page = ctk.CTk()
    option_page.title("BeatBond")
    option_page.geometry("700x700")
    option_page.config(background='#FBEBC7')

    etiqueta = ctk.CTkLabel(option_page, text="¡Bienvenido a la nueva ventana!")
    etiqueta.pack()

    # Mostrar la nueva ventana
    option_page.mainloop()

#Tema
#MainPage
mainpage = ctk.CTk()
mainpage.title("BeatBond")
mainpage.geometry("700x700")
mainpage.config(background='#FBEBC7')

#Logo
logo_image = Image.open('images/beatbond_logo.png')
logo = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(600, 600))  # width x height
logo_label = ctk.CTkLabel(mainpage, text="", image=logo, bg_color="#FFD700")  # Color de fondo amarillo para el logo
logo_label.pack(pady=20, padx=150)

#fontita
boton_font = ctk.CTkFont(family="Impact", size=40, 
     slant="italic")
slogan_font = ctk.CTkFont(family="Consolas", size=20, 
    weight="bold", slant="italic")

slogan = ctk.CTkLabel(mainpage, text="Revolutionize your sound", font=slogan_font, bg_color="#FBEBC7", text_color="#5A2B71")  # Color de fondo beige para el slogan
slogan.pack(pady=1)

#Botón de iniciar
boton_iniciar = ctk.CTkButton(mainpage, text="⭐ EMPEZAR ⭐", corner_radius=32, fg_color="#5A2B71", hover_color="#9350b4", border_color='#5A2B71', font=boton_font,  bg_color="#FBEBC7", command=option_page)
boton_iniciar.pack()

mainpage.mainloop()

#Asegúrate de cerrar las imágenes después de que la ventana principal se cierre
logo_image.close()