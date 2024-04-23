import customtkinter as ctk
from PIL import Image, ImageTk

def option_page():
    mainpage.destroy()
    option_page = ctk.CTk()
    option_page.title("BeatBond")
    option_page.geometry("700x700")
    option_page.config(background='#FBEBC7')

    

    #Logo
    logo_image = Image.open('images/beatbond_logo.png')
    logo = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(600, 600))  # width x height
    logo_label = ctk.CTkLabel(option_page, text="", image=logo, bg_color="#FFD700")  # Color de fondo amarillo para el logo
    logo_label.pack(pady=20, padx=150)

    def funcion_boton1():
        print("Botón 1 presionado")

    def funcion_boton2():
        print("Botón 2 presionado")

        # Crear los botones y asignarles las funciones
    boton1 = ctk.CTkButton(option_page, text="Botón 1", command=funcion_boton1)
    boton2 = ctk.CTkButton(option_page, text="Botón 2", command=funcion_boton2)

    # Posicionar los botones en la misma fila
    boton1.place(relx=0.5, rely=0.8, anchor="e", relwidth=0.2)
    boton2.place(relx=0.5, rely=0.8, anchor="w", relwidth=0.2)
    boton1.pack(padx=10)
    boton2.pack(padx=10)
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
slogan_font = ctk.CTkFont(family="Consolas", size=35, 
    weight="bold", slant="italic")

slogan = ctk.CTkLabel(mainpage, text="Revolutionize your sound", font=slogan_font, bg_color="#FBEBC7", text_color="#5A2B71")  # Color de fondo beige para el slogan
slogan.pack(pady=2)

#label sin nada para centrar el slogan
empty_label = ctk.CTkLabel(mainpage, text="", text_color="#FBEBC7", bg_color="#FBEBC7")
empty_label.pack(pady = 10)
empty_label2 = ctk.CTkLabel(mainpage, text="", text_color="#FBEBC7", bg_color="#FBEBC7")

##Botón de iniciar
boton_iniciar = ctk.CTkButton(mainpage, text="⭐ EMPEZAR ⭐", corner_radius=32, fg_color="#5A2B71", hover_color="#9350b4", border_color='#5A2B71', font=boton_font,  bg_color="#FBEBC7", command=option_page)
boton_iniciar.pack()
empty_label2.pack(pady = 10)

mainpage.mainloop()

#Asegúrate de cerrar las imágenes después de que la ventana principal se cierre
logo_image.close()