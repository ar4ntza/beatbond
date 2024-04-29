import pandas as pd
import networkx as nx
import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk

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
        
        df = pd.read_excel('AH.xlsx')  # Suponiendo que tienes una columna para género, canción y artista en tu archivo Excel
        G = nx.Graph()

        # Agrupar canciones por género
        generos = df['genero'].unique()
        for genero in generos:
            canciones_genero = df[df['genero'] == genero]['cancion'].tolist()
            G.add_nodes_from(canciones_genero)

            # Conectar las aristas / canciones que comparten el mismo género
            for i in range(len(canciones_genero)):
                for j in range(i+1, len(canciones_genero)):
                    G.add_edge(canciones_genero[i], canciones_genero[j])

        # Referencia al canvas de matplotlib y a la lista de relaciones
        canvas = None
        relations_listbox = None

        # Dividir la ventana en dos frames
        frame_left = ctk.CTkFrame(genres_window, fg_color="#FBEBC7")
        frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        frame_right = ctk.CTkFrame(genres_window, fg_color="#FBEBC7")
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        # Función para actualizar el grafo y la lista de relaciones
        def update_graph_and_relations(search_query):
            nonlocal canvas, relations_listbox
            
            # Limpiar el área de dibujo anterior y la lista de relaciones si existen
            if canvas:
                canvas.get_tk_widget().destroy()
            if relations_listbox:
                relations_listbox.destroy()
            
            # Filtrar las canciones por el género buscado
            canciones_genero = df[df['genero'].str.lower() == search_query.lower()]
            subgraph = G.subgraph(canciones_genero['cancion'].tolist()) if not canciones_genero.empty else None
            boton_fonty = ("Impact", 20)
            # Actualizar la lista de relaciones
            relations_listbox = ctk.CTkTextbox(frame_right, fg_color="#FBEBC7", text_color="#000000", font=boton_fonty )
            relations_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            if subgraph:
                relations_listbox.insert(tk.END, f"Las canciones del género '{search_query}' son: \n")
                for cancion in canciones_genero.itertuples():
                    relations_listbox.insert(tk.END, f"\n- {cancion.cancion} - {cancion.artista}\n")
            else:
                relations_listbox.insert(tk.END, f"No se encontraron canciones para el género '{search_query}' ")
            
            # Crear una figura de matplotlib para el grafo
            fig, ax = plt.subplots(figsize=(5, 4))
            # Dibujar el subgrafo del género buscado
            if subgraph:
                pos = nx.spring_layout(subgraph)  # Calcular la posición de los nodos
                nx.draw(subgraph, ax=ax, pos=pos, with_labels=True, node_color='skyblue', edge_color='black')
            else:
                ax.text(0.5, 0.5, 'Género no encontrado', transform=ax.transAxes, ha='center', va='center')
            
            # Crear el canvas de matplotlib y añadirlo al frame izquierdo
            canvas = FigureCanvasTkAgg(fig, master=frame_left)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        # Crear la barra de búsqueda y el botón fuera de la función update_graph_and_relations
        search_bar = ctk.CTkEntry(genres_window, placeholder_text="Buscar canciones del genero...", fg_color="#FBEBC7", text_color="black", bg_color="#FBEBC7")
        search_bar.pack(pady=10)

        search_button = ctk.CTkButton(genres_window, text="Buscar", command=lambda: update_graph_and_relations(search_bar.get()), fg_color="#5A2B71", bg_color="#FBEBC7", hover_color="#9350b4" )
        search_button.pack()

        genres_window.mainloop()

# Asegúrate de llamar a genres_page() para iniciar la interfaz


    # Botones para navegar a las páginas de exploración y géneros
    frame_botones = ctk.CTkFrame(option_window, bg_color="#FBEBC7", fg_color="#FBEBC7")
    frame_botones.pack(pady=20)
    boton_font = ("Impact", 50)
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