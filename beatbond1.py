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
    frame_botones = ctk.CTkFrame(option_page, bg_color="#FBEBC7")
    frame_botones.pack(pady=20)

    # Posicionar los botones en la misma fila con un espacio entre ellos dentro del contenedor
    boton1 = ctk.CTkButton(frame_botones, text="BROWSE", command=browse_page, corner_radius=32, fg_color="#5A2B71", hover_color="#9350b4", border_color='#5A2B71', font=boton_font,  bg_color="#FBEBC7")
    boton2 = ctk.CTkButton(frame_botones, text="GENRES", command=genres_page, corner_radius=32, fg_color="#5A2B71", hover_color="#9350b4", border_color='#5A2B71', font=boton_font,  bg_color="#FBEBC7")

    boton1.pack(side="left", padx=10)  # Espaciado horizontal desde el centro
    boton2.pack(side="left", padx=10)  # Espaciado horizontal desde el centro

    # Mostrar la nueva ventana
    option_page.mainloop()

def browse_page():
    option_page.destroy()
    browse_page = ctk.CTk()
    browse_page.title("Browse Songs")
    browse_page.geometry("700x700")
    browse_page.config(background='#FBEBC7')

def genres_page():
    option_page.destroy()
    genres = ctk.CTk()
    genres.title("Browse Songs")
    genres.geometry("700x700")
    genres_page.config(background='#FBEBC7')

    #Logo
    logo_image = Image.open('images/beatbond_logo.png')
    logo = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(600, 600))  # width x height
    logo_label = ctk.CTkLabel(option_page, text="", image=logo, bg_color="#FFD700")  # Color de fondo amarillo para el logo
    logo_label.pack(pady=20, padx=150)

    # Mostrar la nueva ventana
    option_page.mainloop()
    browse_page.mainloop()
    genres_page.mainloop()

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