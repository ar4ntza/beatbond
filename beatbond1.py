import pandas as pd
import networkx as nx
import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import numpy as np
import sys

mainpage = ctk.CTk()
mainpage.title("BeatBond")
width = mainpage.winfo_screenwidth()
height = mainpage.winfo_screenheight()
mainpage.geometry(f"{width}x{height}")
image = Image.open("images/ondas.jpg")
background_image = ImageTk.PhotoImage(image)
background_label = ctk.CTkLabel(mainpage, image=background_image, text="")
background_label.pack(fill="both", expand=True)  # Usar relwidth y relheight para cubrir toda la ventana

# Función para la página de opciones
def option_page():
    mainpage.destroy()
    option_window = ctk.CTk()
    option_window.title("Página de Opciones")
    option_window.geometry("700x700")
    option_window.config(background='#FBEBC7')
    

    # Función para la página de exploración
    def browse_page():
        option_window.destroy()
        browse_window = ctk.CTk()
        browse_window.title("Explorar Canciones")
        browse_window.geometry("700x700")
        browse_window.config(background='#FBEBC7')
        
        # Función para cargar datos de canciones desde el archivo de Excel
        def cargar_datos(archivo_excel):
            return pd.read_excel(archivo_excel)

        # Función para crear un grafo de canciones a partir de los datos cargados
        def crear_grafo(datos_canciones):
            grafo = nx.Graph()

            for index, cancion in datos_canciones.iterrows():
                grafo.add_node(cancion['cancion'], genero=cancion['genero'])

                for cancion_relacionada in datos_canciones.loc[datos_canciones['cancion'] != cancion['cancion'], 'cancion']:
                    grafo.add_edge(cancion['cancion'], cancion_relacionada)

            return grafo

        relaciones = [
            ('Rock', 'Metal', 0.7),
            ('Rock', 'Heavy metal', 0.6),
            ('Rock', 'Heavy metal', 0.6),
            ('Rock', 'Jazz', 0.4),
            ('Metal', 'Heavy metal', 0.3),
            ('Cumbia', 'Salsa', 0.7),
            ('Bachata', 'Boleros', 0.6),
            ('Reggaeton', 'Old Reggeton', 0.4),
            ('Jazz', 'R&B', 0.3),
            ('Electronica', 'Hiphop', 0.3),
            ('rap', 'Trap', 0.3),
            ('R&B', 'pop', 0.3),
        ]

        # Cargar datos de la base de datos (Excel)
        archivo_excel = 'AH.xlsx'
        datos_canciones = cargar_datos(archivo_excel)

        # Crear el grafo de canciones
        grafo_canciones = crear_grafo(datos_canciones)

        def buscar_canciones():
            # Obtener la canción buscada desde la barra de búsqueda
            cancion_buscada = search_bar.get()

            if not cancion_buscada:
                return
            try:
                genero_cancion_buscada = nx.get_node_attributes(grafo_canciones, 'genero')[cancion_buscada]
            except KeyError:
                # Mostrar mensaje de error si la canción no se encuentra
                results_list.insert(ctk.END, f"Canción '{cancion_buscada}' no encontrada.\n")
                return
            
            # Limpiar la lista de resultados
            results_list.delete("1.0", "end")

            # Generar las canciones del mismo género
            generator = (node for node, attr in grafo_canciones.nodes(data=True) if attr['genero'] == genero_cancion_buscada and node!= cancion_buscada)

            # Yield the songs
            for cancion in generator:
                yield cancion

        def song_label():
            # Eliminar cualquier etiqueta de resultado previa si existe
            for widget in results_frame.winfo_children():
                if widget!= results_list:
                    widget.destroy()

            # Verificar si se encontró la canción
            if results_list.get("1.0", "end-1c") == "":
                not_found_label = ctk.CTkLabel(results_frame, text="¡Canción no encontrada!", font=('<Arial>', 22, "bold", "italic"), text_color="#5A2B71", fg_color="#FBEBC7")
                not_found_label.pack(anchor=tk.CENTER, pady=0)
            else:
                found_label = ctk.CTkLabel(results_frame, text="¡Canción encontrada!", font=('<Arial>', 22, "bold", "italic"), text_color="#5A2B71", fg_color="#FBEBC7")
                found_label.pack(anchor=tk.CENTER, pady=0)

        def find_related_genres_and_songs(grafo_canciones, cancion_buscada):
            # Get the genre of the searched song
            genero_cancion_buscada = nx.get_node_attributes(grafo_canciones, 'genero')[cancion_buscada]

            print(f"Genre of searched song: {genero_cancion_buscada}")

            # Find related genres
            related_genres = []
            for relacion in relaciones:
                if genero_cancion_buscada in relacion:
                    related_genres.append(relacion[0 if relacion[0] != genero_cancion_buscada else 1])

            print(f"Related genres: {related_genres}")

            # Find related songs
            related_songs = []
            for node, attr in grafo_canciones.nodes(data=True):
                if attr['genero'] in related_genres:
                    related_songs.append(node)

            print(f"Related songs: {related_songs}")

            return related_genres, related_songs

        def create_related_frames(browse_window):
            # Frame para géneros relacionados
            related_genres_frame = ctk.CTkFrame(browse_window, width=300, height=300, fg_color="#FFA3B5")
            related_genres_frame.pack(side=tk.LEFT, padx=10, pady=10)

            # Título para géneros relacionados
            related_genres_label = ctk.CTkLabel(related_genres_frame, text="Géneros relacionados:")
            related_genres_label.pack(pady=10)

            # Cuadro de texto para géneros relacionados
            global related_genres_textbox
            related_genres_textbox = ctk.CTkTextbox(related_genres_frame, width=280, height=250)
            related_genres_textbox.pack(pady=10)

            # Frame para canciones relacionadas
            related_songs_frame = ctk.CTkFrame(browse_window, width=300, height=300, fg_color="#FFA3B5")
            related_songs_frame.pack(side=tk.LEFT, padx=10, pady=10)

            # Título para canciones relacionadas
            related_songs_label = ctk.CTkLabel(related_songs_frame, text="Canciones relacionadas:")
            related_songs_label.pack(pady=10)

            # Cuadro de texto para canciones relacionadas
            global related_songs_textbox
            related_songs_textbox = ctk.CTkTextbox(related_songs_frame, width=280, height=250)
            related_songs_textbox.pack(pady=10)


        def buscar_mostrar():
            # Buscar canción
            for cancion in buscar_canciones():
                results_list.insert(ctk.END, cancion + "\n")
            song_label()
            # Encontrar géneros y canciones relacionadas
            related_genres, related_songs = find_related_genres_and_songs(grafo_canciones, search_bar.get())

            # Mostrar géneros relacionados
            related_genres_textbox.delete("1.0", "end")
            for genero in related_genres:
                related_genres_textbox.insert("end", f"{genero}\n")

            # Mostrar canciones relacionadas
            related_songs_textbox.delete("1.0", "end")
            for cancion in related_songs:
                related_songs_textbox.insert("end", f"{cancion}\n")

            print("memoria usada con yields: ", sys.getsizeof(buscar_canciones), "bytes")

        # Barra de búsqueda
        search_bar = ctk.CTkEntry(browse_window, placeholder_text="Ingrese una canción")
        search_bar.pack(pady=10)

        search_button = ctk.CTkButton(browse_window, text="Buscar", command=buscar_mostrar, bg_color="#FBEBC7", hover_color="#EF3340", fg_color="#EA516D")
        search_button.pack(pady=10)

        # Frame para contener los resultados
        results_frame = ctk.CTkFrame(browse_window)
        results_frame.pack(pady=10)

        # Lista para mostrar resultados
        results_list = ctk.CTkTextbox(results_frame, bg_color="#FBEBC7", fg_color="#FF808B", border_width=0)
        results_list.pack(expand=True, fill=ctk.BOTH)

        create_related_frames(browse_window)
        browse_window.mainloop()

    # Función para la página de géneros
    def genres_page():
        option_window.destroy()
        genres_window = ctk.CTk()
        genres_window.title("Página de Géneros")
        genres_window.geometry("700x700")
        genres_window.config(background='#FBEBC7')
        search_frame = ctk.CTkFrame(genres_window, fg_color="#FBEBC7", bg_color="#FBEBC7")
        search_frame.pack(side=tk.TOP, fill=tk.X)
        
         # Asumiendo que tienes una columna 'genero' en tu archivo Excel 'AH.xlsx'
        df = pd.read_excel('AH.xlsx')
        G = nx.Graph()
        # Añadir géneros como nodos al grafo
        generos = df['genero'].unique()
        G.add_nodes_from(generos)

        # Asumiendo que queremos crear subgrafos para cada género
        for genero in generos:
            sub_nodes = [genero]  # Nodos que queremos en el subgrafo
            for _, vecino in G.edges(genero):
                sub_nodes.append(vecino)  # Agregar los vecinos del genero seleccionado
            subgraph = G.subgraph(sub_nodes).copy()  # Hacer una copia del subgrafo para poder modificarlo

            # Agregar las canciones asociadas al género seleccionado al subgrafo
            for _, row in df[df['genero'] == genero].iterrows():
                cancion = row['cancion']
                subgraph.add_node(cancion)
                subgraph.add_edge(genero, cancion)

        # Referencia al canvas de matplotlib y a la lista de relaciones
        canvas = None
        relations_listbox = None

        # Dividir la ventana en dos frames
        frame_left = ctk.CTkFrame(genres_window, fg_color="#FBEBC7", bg_color="#FBEBC7", corner_radius=32)
        frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=(20, 20), pady=(20, 20))  # add 20px padding to the left, 20px padding to the right, 20px padding to the top, and 20px padding to the bottom

        frame_right = ctk.CTkFrame(genres_window, fg_color="#EAD3E2", bg_color="#FBEBC7",corner_radius=32)
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1, padx=(20, 20), pady=(20, 20))  # add 20px padding to the left, 20px padding to the right, 20px padding to the top, and 20px padding to the bottom
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
            subgraph = nx.Graph()  # Crear un nuevo grafo vacío
            if not canciones_genero.empty:
                subgraph.add_node(search_query)  # Añadir el nodo del género al grafo
                for cancion in canciones_genero['cancion']:
                    subgraph.add_node(cancion)  # Añadir los nodos de las canciones al grafo
                    subgraph.add_edge(search_query, cancion)  # Conectar cada canción con el género
            boton_fonty = ("Impact", 20)
            # Actualizar la lista de relaciones
            relations_listbox = ctk.CTkTextbox(frame_right, fg_color="#EAD3E2", text_color="#000000", font=boton_fonty, corner_radius=32)
            relations_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            if not canciones_genero.empty:
                relations_listbox.insert(tk.END, f"Las canciones del género '{search_query}' son: \n")
                for cancion in canciones_genero.itertuples():
                    relations_listbox.insert(tk.END, f"\n- {cancion.cancion} - {cancion.artista}\n")
            else:
                relations_listbox.insert(tk.END, f"No se encontraron canciones para el género '{search_query}' ")
            
            # Crear una figura de matplotlib para el grafo
            fig, ax = plt.subplots(figsize=(5, 4))
            # Dibujar el subgrafo del género buscado
            if not canciones_genero.empty:
                pos = nx.spring_layout(subgraph)  # Calcular la posición de los nodos
                ax.set_facecolor('#f2f2f2')  # set background color to light gray
                nx.draw(subgraph, ax=ax, pos=pos, with_labels=True, node_color='#DFA0C9', edge_color='black', node_size=1500)
                pos[search_query] = np.array([0, 0])  # Colocar el nodo del género en el centro
                nx.draw_networkx_nodes(subgraph, pos, nodelist=[search_query], node_size=1500, node_color='#C6579A')
            else:
                ax.text(0.6, 0.5, 'El genero no se ha encontrado...\n Revise que esté escrito correctamente', transform=ax.transAxes, ha='center', va='center')
            
            # Crear el canvas de matplotlib y añadirlo al frame izquierdo
            canvas = FigureCanvasTkAgg(fig, master=frame_left)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        
        search_bar = ctk.CTkEntry(search_frame, placeholder_text="Buscar genero...", fg_color="#FBEBC7", text_color="black", bg_color="#FBEBC7", font=('Impact', 25), width=450)
        search_bar.pack(padx=5, pady=2)

        search_button = ctk.CTkButton(search_frame, text="🔍", command=lambda: update_graph_and_relations(search_bar.get()), fg_color="#5A2B71", bg_color="#FBEBC7", hover_color="#9350b4", font=('Impact', 25), width=10)
        search_button.pack(padx=15)
        genres_window.mainloop()

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
button_font = ctk.CTkFont(family="Impact", size=40, slant="italic")

button_frame = ctk.CTkFrame(mainpage, bg_color="transparent", fg_color="transparent")
button_frame.place(relx=0.2, rely=0.9, anchor="center")  # Centra el marco de botón en la ventana

start_button = ctk.CTkButton(button_frame, text="⭐ EMPEZAR ⭐", corner_radius=32, 
                              fg_color="#460A75", hover_color="#621C99", 
                              border_color='#9F54DB', font=button_font, 
                              bg_color="transparent", command=option_page)
start_button.pack()

mainpage.mainloop()