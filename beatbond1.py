import customtkinter as ctk
from PIL import Image

# Función para crear el logo
def create_logo(window, bg_color):
    logo_image = Image.open('images/beatbond_logo.png')
    logo = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(600, 600))
    logo_label = ctk.CTkLabel(window, text="", image=logo, bg_color=bg_color)
    logo_label.pack(pady=20, padx=150)
    logo_image.close()  # Cerrar el archivo de imagen después de crear la etiqueta

# Página principal
mainpage = ctk.CTk()
mainpage.title("BeatBond")
mainpage.geometry("700x700")
mainpage.config(background='#FBEBC7')
create_logo(mainpage, "#FFD700")  # Crear logo en la página principal

# Estilos de fuente y otros elementos de la página principal...
# ...

# Función para la página de opciones
def option_page():
    mainpage.destroy()
    option_window = ctk.CTk()
    option_window.title("Página de Opciones")
    option_window.geometry("700x700")
    option_window.config(background='#FBEBC7')
    create_logo(option_window, "#FBEBC7")  # Crear logo en la página de opciones

    # Función para la página de exploración
    def browse_page():
        option_window.destroy()
        browse_window = ctk.CTk()
        browse_window.title("Explorar Canciones")
        browse_window.geometry("700x700")
        browse_window.config(background='#FBEBC7')
        create_logo(browse_window, "#FFD700")  # Crear logo en la página de exploración
        # Configuración adicional para browse_window...
        browse_window.mainloop()

    # Función para la página de géneros
    def genres_page():
        option_window.destroy()
        genres_window = ctk.CTk()
        genres_window.title("Página de Géneros")
        genres_window.geometry("700x700")
        genres_window.config(background='#FBEBC7')
        create_logo(genres_window, "#FFD700")  # Crear logo en la página de géneros
        # Configuración adicional para genres_window...
        genres_window.mainloop()

    # Botones para navegar a las páginas de exploración y géneros
    frame_botones = ctk.CTkFrame(option_window, bg_color="#FBEBC7", fg_color="#FBEBC7")
    frame_botones.pack(pady=20)
    boton_font = ("Arial", 50)
    boton1 = ctk.CTkButton(frame_botones, text="EXPLORAR", command=browse_page,
                           corner_radius=32, fg_color="#5A2B71", hover_color="#9350b4",
                           border_color='#5A2B71', font=boton_font, bg_color="#FBEBC7")
    boton1.pack(side="left", padx=10)

    boton2 = ctk.CTkButton(frame_botones, text="GÉNEROS", command=genres_page,
                           corner_radius=32, fg_color="#5A2B71", hover_color="#9350b4",
                           border_color='#5A2B71', font=boton_font, bg_color="#FBEBC7")
    boton2.pack(side="left", padx=10)

    option_window.mainloop()

# Font Styles
boton_font = ctk.CTkFont(family="Impact", size=40, slant="italic")
slogan_font = ctk.CTkFont(family="Consolas", size=35, weight="bold", slant="italic")
# Botón para empezar en la página principal
boton_iniciar = ctk.CTkButton(mainpage, text="⭐ EMPEZAR ⭐", corner_radius=32, fg_color="#5A2B71", hover_color="#9350b4",
                              border_color='#5A2B71', font=boton_font, bg_color="#FBEBC7", command=option_page)
boton_iniciar.pack()

mainpage.mainloop()
