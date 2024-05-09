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
class BeatBondApp:
    def __init__(self):
        self.mainpage = ctk.CTk()
        self.mainpage.title("BeatBond")
        self.width = self.mainpage.winfo_screenwidth()
        self.height = self.mainpage.winfo_screenheight()
        self.mainpage.geometry(f"{self.width}x{self.height}")
        
        # Create a single frame for all pages
        self.main_frame = ctk.CTkFrame(self.mainpage)
        self.main_frame.pack(fill="both", expand=True)
        
        self.create_main_page()

    def create_main_page(self):
        # Create elements for the main page
        self.mainpage_background_label = ctk.CTkLabel(self.main_frame, text=" ")
        self.mainpage_background_label.pack(fill="both", expand=True)
        
        # Load background image
        background_image = ImageTk.PhotoImage(Image.open("images/ondas.jpg"))
        
        # Create background label and pack it into main_frame
        background_label = ctk.CTkLabel(self.mainpage_background_label, image=background_image, text="")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create elements for the main page
        mainpage_background_label = ctk.CTkLabel(self.mainpage_background_label, text="Main Page")
        
        button_frame = ctk.CTkFrame(self.mainpage_background_label, bg_color="transparent", fg_color="transparent")
        button_frame.place(relx=0.2, rely=0.9, anchor="center")

        start_button = ctk.CTkButton(button_frame, text="Get Started", corner_radius=32, 
                                        fg_color="#7118C0", hover_color="#8A3DCF", 
                                        border_color='#7118C0', font = ('<Century Gothic>', 40, "bold"),
                                        bg_color="transparent", command=lambda: self.option_page())
        start_button.pack()

    def option_page(self):
        # Clear the main frame
        self.clear_main_frame()
        
        # Create elements for the option page
        self.option_background_label = ctk.CTkLabel(self.main_frame, text=" ")
        self.option_background_label.pack(fill="both", expand=True)
        
        # Load background image
        background_image = ImageTk.PhotoImage(Image.open("images/discos.jpg"))
        
        # Create background label and pack it into main_frame
        background_label = ctk.CTkLabel(self.option_background_label, image=background_image, text="")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create buttons
        button_font = ("Impact", 50)
        browse_button = ctk.CTkButton(self.main_frame, text="EXPLORAR", command=self.browse_page,
                                    corner_radius=50, fg_color="#7118C0", hover_color="#8A3DCF", 
                                    border_color='#7118C0', font=button_font, bg_color="transparent")
        browse_button.place(relx=0.4, rely=0.5, anchor="center")

        genres_button = ctk.CTkButton(self.main_frame, text="GÉNEROS", command=self.genres_page,
                                    corner_radius=50, fg_color="#7118C0", hover_color="#8A3DCF", 
                                    border_color='#7118C0', font=button_font, bg_color="transparent")
        genres_button.place(relx=0.6, rely=0.5, anchor="center")

    def browse_page(self):
        self.browse_window = ctk.CTk()
        self.browse_window.title("Explorar Canciones")
        self.browse_window.geometry(f"{self.width}x{self.height}")
        self.browse_window.config(background='#41397D')

        def cargar_datos(archivo_excel):
            return pd.read_excel(archivo_excel)

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

        archivo_excel = 'AH.xlsx'
        datos_canciones = cargar_datos(archivo_excel)
        grafo_canciones = crear_grafo(datos_canciones)

        def buscar_canciones():
            cancion_buscada = search_bar.get()  # Convertir a minúsculas

            if not cancion_buscada:
                return
            try:
                genero_cancion_buscada = nx.get_node_attributes(grafo_canciones, 'genero')[cancion_buscada]
            except KeyError:
                results_list.insert(ctk.END, f"Canción '{cancion_buscada}' no encontrada.\n")
                return

            results_list.delete("1.0", "end")

            generator = (node for node, attr in grafo_canciones.nodes(data=True) if attr['genero'] == genero_cancion_buscada and node != cancion_buscada)

            for cancion in generator:
                yield cancion

        def find_related_genres_and_songs(grafo_canciones, cancion_buscada):
            genero_cancion_buscada = nx.get_node_attributes(grafo_canciones, 'genero')[cancion_buscada]

            print(f"Genre of searched song: {genero_cancion_buscada}")

            related_genres = []
            for relacion in relaciones:
                if genero_cancion_buscada in relacion:
                    related_genres.append(relacion[0 if relacion[0] != genero_cancion_buscada else 1])

            print(f"Related genres: {related_genres}")

            related_songs = []
            for node, attr in grafo_canciones.nodes(data=True):
                if attr['genero'] in related_genres:
                    related_songs.append(node)

            print(f"Related songs: {related_songs}")

            return related_genres, related_songs

        def create_related_frames(browse_window):
            related_genres_frame = ctk.CTkFrame(browse_window, width=300, height=300, fg_color="#BB5538", bg_color="#41397D")
            related_genres_frame.place(relx=0.25, rely=0.70, anchor="center")

            related_genres_label = ctk.CTkLabel(related_genres_frame, text="Géneros relacionados:", font=('<Century Gothic>', 22, "bold"), text_color="#FFFFFF")
            related_genres_label.pack(pady=10)

            global related_genres_textbox
            related_genres_textbox = ctk.CTkTextbox(related_genres_frame, width=280, height=250, bg_color="#C26E60", font=('Century Gothic', 15))
            related_genres_textbox.pack(pady=10)

            related_songs_frame = ctk.CTkFrame(browse_window, width=500, height=500, fg_color="#BB5538", bg_color="#41397D")
            related_songs_frame.place(relx=0.75, rely=0.70, anchor="center")

            related_songs_label = ctk.CTkLabel(related_songs_frame, text="Canciones relacionadas:", font=('<Century Gothic>', 22, "bold"), text_color="#FFFFFF")
            related_songs_label.pack(pady=10)

            global related_songs_textbox
            related_songs_textbox = ctk.CTkTextbox(related_songs_frame, width=280, height=250, bg_color="#C26E60",  font=('Century Gothic', 15))
            related_songs_textbox.pack(pady=10)

        def buscar_mostrar():
            results_list.delete("1.0", "end")
            related_genres_textbox.delete("1.0", "end")
            related_songs_textbox.delete("1.0", "end")

            for cancion in buscar_canciones():
                results_list.insert(ctk.END, cancion + "\n")


            related_genres, related_songs = find_related_genres_and_songs(grafo_canciones, search_bar.get())
            for genero in related_genres:
                related_genres_textbox.insert("end", f"{genero}\n")
            for cancion in related_songs:
                related_songs_textbox.insert("end", f"{cancion}\n")

            print("memoria usada con yields: ", sys.getsizeof(buscar_canciones), "bytes")

        search_bar = ctk.CTkEntry(self.browse_window, placeholder_text="Ingrese una canción", width=500, height=35, bg_color="#41397D", font=('<Century Gothic>', 18, "bold"), text_color="#545454")
        search_bar.pack(pady=40)

        search_button = ctk.CTkButton(self.browse_window, text="Buscar", command=buscar_mostrar, bg_color="#41397D", hover_color="#CBA052", fg_color="#AFA96E", font=('<Century Gothic>', 15, "bold"))
        search_button.pack(pady=10)

        results_frame = ctk.CTkFrame(self.browse_window)
        results_frame.pack(pady=10)

        results_list = ctk.CTkTextbox(results_frame, bg_color="#41397D", fg_color="#2D2F4E", border_width=0, font=('Century Gothic', 15), text_color="#FFFFFF", width=350, height=150)
        results_list.pack(expand=True, fill=ctk.BOTH)

        credit_button = ctk.CTkButton(self.browse_window, text="👽", command=self.creditos, fg_color="#FBEBC7", bg_color="#41397D", hover_color="#F8C546")
        credit_button.pack(pady=10)

        create_related_frames(self.browse_window)
        self.browse_window.mainloop()


    def genres_page(self):
        # Clear the main frame
        self.genres_window = ctk.CTk()
        self.genres_window.title("Página de Géneros")
        self.genres_window.geometry("700x700")
        self.genres_window.config(background='#FBEBC7')
        search_frame = ctk.CTkFrame(self.genres_window, fg_color="#FBEBC7", bg_color="#FBEBC7")
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
        frame_left = ctk.CTkFrame(self.genres_window, fg_color="#FBEBC7", bg_color="#FBEBC7", corner_radius=32)
        frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=(20, 20), pady=(20, 20))  # add 20px padding to the left, 20px padding to the right, 20px padding to the top, and 20px padding to the bottom

        frame_right = ctk.CTkFrame(self.genres_window, fg_color="#EAD3E2", bg_color="#FBEBC7",corner_radius=32)
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
        credit_button = ctk.CTkButton(self.genres_window, text="👽", command=self.creditos, fg_color="#FBEBC7", bg_color="#FBEBC7", hover_color="#F8C546")
        credit_button.pack(pady=10)
        browse_button = ctk.CTkButton(self.genres_window, text="Explorar Canciones", command=self.browse_page,
                            corner_radius=50, fg_color="#7118C0", hover_color="#8A3DCF", 
                            border_color='#7118C0', font = ('<Century Gothic>', 40, "bold"), bg_color="transparent")
        browse_button.pack(side=tk.BOTTOM, pady=20)
        self.genres_window.mainloop()

    def creditos(self):
        self.credit_page = ctk.CTk()
        self.credit_page.title("Página Personalizada")
        self.credit_page.geometry("400x300")
        self.credit_page.config(bg="#060515")  # Change the background color of the page

        frame = ctk.CTkFrame(self.credit_page, bg_color="#060515")
        frame.pack(pady=20)

        label = ctk.CTkLabel(frame, text="(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧\n\nElaborado por:\nArantza García y Samantha Cortés", font=('<Arial>', 22, "bold", "italic"), text_color="#FFFFFF", bg_color="#060515")
        label.pack()       
        cred_image = Image.open('images/zinkys.png')
        cred = ctk.CTkImage(light_image=cred_image, dark_image=cred_image, size=(600, 600))
        logo_label = ctk.CTkLabel(self.credit_page, text="", image=cred, bg_color='transparent')
        logo_label.pack(pady=20, padx=150)
        cred_image.close()
        self.credit_page.mainloop()

    def clear_main_frame(self):
        # Clear all widgets in the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = BeatBondApp()
    app.mainpage.mainloop()