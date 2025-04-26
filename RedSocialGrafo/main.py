import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from grafo import Graph
import math

class SocialGraphApp:
    def __init__(self, root):
        self.graph = Graph()
        self.root = root
        self.root.title("Red Social - Grafo de Usuarios")
        self.root.geometry("1000x900")  # Tamaño de la ventana

        self.style = tb.Style("superhero")
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")  # Usamos grid para mayor control

        # Configurar el grid para que ocupe toda la ventana
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Crear Label y Entry para agregar usuario
        ttk.Label(frame, text="Ingrese el nombre del Usuario:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.user_entry = ttk.Entry(frame, width=25)
        self.user_entry.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        # Botón para agregar usuario
        ttk.Button(frame, text="Agregar Usuario", command=self.add_user).grid(row=0, column=2, padx=5, pady=10)

        # Etiquetas para agregar amistad
        ttk.Label(frame, text="Conectar Amigos (Usuario con Usuario):", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.friend1_entry = ttk.Entry(frame, width=20)
        self.friend1_entry.grid(row=1, column=1, padx=5, pady=10)
        self.friend2_entry = ttk.Entry(frame, width=20)
        self.friend2_entry.grid(row=1, column=2, padx=5, pady=10)

        # Botón para conectar usuarios
        ttk.Button(frame, text="Conectar Usuarios", command=self.add_friendship).grid(row=1, column=3, padx=5, pady=10)

        # Selector de usuario para ver amigos y sugerencias
        ttk.Label(frame, text="Usuario que desea análisar:", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=10, sticky="w")
        self.selected_user = ttk.Entry(frame, width=25)
        self.selected_user.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        # Botón para mostrar amigos y sugerencias
        ttk.Button(frame, text="Mostrar Amigos y Sugerencias", command=self.show_friends_and_suggestions).grid(row=2, column=2, padx=5, pady=10)

        # Campo de resultados
        self.result_text = tk.Text(frame, height=10, width=80)
        self.result_text.grid(row=3, column=0, columnspan=4, padx=5, pady=10)

        # Canvas para grafo
        self.canvas = tk.Canvas(frame, width=800, height=500, bg="white")
        self.canvas.grid(row=4, column=0, columnspan=4, pady=20)

    def add_user(self):
        user = self.user_entry.get().strip()
        if user:
            self.graph.add_user(user)
            self.result_text.insert("end", f"Usuario agregado: {user}\n")
            self.user_entry.delete(0, 'end')
            self.draw_graph()

    def add_friendship(self):
        user1 = self.friend1_entry.get().strip()
        user2 = self.friend2_entry.get().strip()
        if user1 and user2:
            self.graph.add_friendship(user1, user2)
            self.result_text.insert("end", f"{user1} y {user2} ahora son amigos\n")
            self.friend1_entry.delete(0, 'end')
            self.friend2_entry.delete(0, 'end')
            self.draw_graph()

    def show_friends_and_suggestions(self):
        user = self.selected_user.get().strip()
        if user:
            friends = self.graph.get_friends(user)
            suggestions = self.graph.suggest_friends_bfs(user)
            self.result_text.insert("end", f"Amigos de {user}: {', '.join(friends)}\n")
            self.result_text.insert("end", f"Sugerencias para {user}: {', '.join(suggestions)}\n")
            self.selected_user.delete(0, 'end')

    def draw_graph(self):
        self.canvas.delete("all")
        users = list(self.graph.adj_list.keys())
        total = len(users)
        radius = 150
        center_x = 400
        center_y = 300
        node_positions = {}

        for i, user in enumerate(users):
            angle = 2 * math.pi * i / total
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            node_positions[user] = (x, y)

        for user, friends in self.graph.adj_list.items():
            x1, y1 = node_positions[user]
            for friend in friends:
                if user < friend:
                    x2, y2 = node_positions[friend]
                    self.canvas.create_line(x1, y1, x2, y2)

        for user, (x, y) in node_positions.items():
            r = 20
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="lightblue")
            self.canvas.create_text(x, y, text=user, font=("Arial", 10))

if __name__ == "__main__":
    root = tb.Window(themename="cosmo")
    app = SocialGraphApp(root)
    root.mainloop()
