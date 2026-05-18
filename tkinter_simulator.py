"""
Interface graphique tkinter pour le simulateur de feu de forêt
Permet la visualisation interactive et la simulation en temps réel
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import threading
from forest_fire_simulator import ForestFireSimulator, Position, TerrainType


class ForestFireGUI:
    """Interface graphique pour le simulateur de feu de forêt"""

    # Couleurs pour les terrains
    COLORS = {
        TerrainType.WATER: '#64B5F6',   # Bleu
        TerrainType.BARE: '#D4AF37',    # Or/désert
        TerrainType.TREE: '#2E8B57',    # Vert
        TerrainType.BURNED: '#8B4513',  # Marron
    }

    CELL_SIZE = 20  # Taille d'une cellule en pixels

    def __init__(self, root):
        """Initialise l'interface graphique"""
        self.root = root
        self.root.title("🔥 Simulateur de Feu de Forêt 🔥")
        self.root.geometry("900x750")

        self.simulator = None
        self.current_map = None
        self.burned_positions = set()
        self.best_clearing_pos = None
        self.canvas = None
        self.simulation_running = False

        self._setup_ui()

    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        # Frame de contrôle
        control_frame = tk.Frame(self.root, bg='#f0f0f0', height=100)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        # Paramètres de génération
        params_frame = tk.LabelFrame(control_frame, text="Paramètres de la carte",
                                     bg='#f0f0f0', font=('Arial', 10, 'bold'))
        params_frame.pack(fill=tk.X, padx=5, pady=5)

        # Largeur
        tk.Label(params_frame, text="Largeur:", bg='#f0f0f0').grid(row=0, column=0, sticky=tk.W, padx=5)
        self.width_var = tk.StringVar(value="30")
        tk.Spinbox(params_frame, from_=5, to=50, textvariable=self.width_var, width=5).grid(row=0, column=1, sticky=tk.W, padx=5)

        # Hauteur
        tk.Label(params_frame, text="Hauteur:", bg='#f0f0f0').grid(row=0, column=2, sticky=tk.W, padx=5)
        self.height_var = tk.StringVar(value="30")
        tk.Spinbox(params_frame, from_=5, to=50, textvariable=self.height_var, width=5).grid(row=0, column=3, sticky=tk.W, padx=5)

        # Pourcentage d'arbres
        tk.Label(params_frame, text="% Arbres:", bg='#f0f0f0').grid(row=0, column=4, sticky=tk.W, padx=5)
        self.tree_percent_var = tk.StringVar(value="35")
        tk.Spinbox(params_frame, from_=0, to=100, textvariable=self.tree_percent_var, width=5).grid(row=0, column=5, sticky=tk.W, padx=5)

        # Bouton générer
        tk.Button(params_frame, text="Générer Carte", command=self._generate_map,
                 bg='#4CAF50', fg='white', padx=10, pady=5).grid(row=0, column=6, padx=5)

        # Frame de simulation
        sim_frame = tk.LabelFrame(control_frame, text="Simulation",
                                  bg='#f0f0f0', font=('Arial', 10, 'bold'))
        sim_frame.pack(fill=tk.X, padx=5, pady=5)

        # Position du feu
        tk.Label(sim_frame, text="Position feu (x,y):", bg='#f0f0f0').grid(row=0, column=0, sticky=tk.W, padx=5)
        self.fire_x_var = tk.StringVar(value="15")
        self.fire_y_var = tk.StringVar(value="15")
        tk.Spinbox(sim_frame, from_=0, to=50, textvariable=self.fire_x_var, width=5).grid(row=0, column=1, sticky=tk.W)
        tk.Label(sim_frame, text=",", bg='#f0f0f0').grid(row=0, column=2)
        tk.Spinbox(sim_frame, from_=0, to=50, textvariable=self.fire_y_var, width=5).grid(row=0, column=3, sticky=tk.W, padx=5)

        # Bouton simuler
        tk.Button(sim_frame, text="Simuler Feu", command=self._simulate_fire,
                 bg='#FF6F00', fg='white', padx=10, pady=5).grid(row=0, column=4, padx=5)

        # Bouton trouver meilleur déboisement
        tk.Button(sim_frame, text="Optimiser Déboisement", command=self._find_best_clearing,
                 bg='#2196F3', fg='white', padx=10, pady=5).grid(row=0, column=5, padx=5)

        # Bouton exporter
        tk.Button(sim_frame, text="Exporter HTML", command=self._export_html,
                 bg='#9C27B0', fg='white', padx=10, pady=5).grid(row=0, column=6, padx=5)

        # Frame d'état
        info_frame = tk.Frame(control_frame, bg='#f0f0f0')
        info_frame.pack(fill=tk.X, padx=5, pady=5)

        self.status_label = tk.Label(info_frame, text="Prêt", bg='#f0f0f0', fg='#333')
        self.status_label.pack(anchor=tk.W)

        # Frame du canvas
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas pour afficher la carte
        self.canvas = tk.Canvas(canvas_frame, bg='white', border=2, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self._canvas_click)

        # Frame d'info en bas
        info_bottom_frame = tk.Frame(self.root, bg='#f0f0f0')
        info_bottom_frame.pack(fill=tk.X, padx=10, pady=5)

        self.info_label = tk.Label(info_bottom_frame, text="Cliquez sur 'Générer Carte' pour commencer",
                                   bg='#f0f0f0', fg='#666', font=('Arial', 9))
        self.info_label.pack(anchor=tk.W)

    def _generate_map(self):
        """Génère une nouvelle carte"""
        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            tree_percent = int(self.tree_percent_var.get())

            if width < 5 or height < 5:
                messagebox.showerror("Erreur", "Les dimensions doivent être ≥ 5")
                return

            self.simulator = ForestFireSimulator(width, height, tree_percent)
            self.current_map = [row[:] for row in self.simulator.map]
            self.burned_positions = set()
            self.best_clearing_pos = None

            self._draw_map()
            self.status_label.config(text=f"✅ Carte générée: {width}x{height}")
            self.info_label.config(text=f"Carte: {width}x{height} | Arbres: {tree_percent}%")

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides")

    def _simulate_fire(self):
        """Simule un incendie"""
        if self.simulator is None:
            messagebox.showwarning("Attention", "Veuillez d'abord générer une carte")
            return

        try:
            fire_x = int(self.fire_x_var.get())
            fire_y = int(self.fire_y_var.get())

            if not (0 <= fire_x < self.simulator.width and 0 <= fire_y < self.simulator.height):
                messagebox.showerror("Erreur", f"Position invalide. Doit être entre (0,0) et ({self.simulator.width-1},{self.simulator.height-1})")
                return

            start_pos = Position(fire_x, fire_y)
            
            # Vérifier que la position est un arbre
            terrain = self.simulator.map[fire_y][fire_x]
            if terrain != TerrainType.TREE:
                messagebox.showerror("Erreur", f"❌ Le feu ne peut démarrer que sur un arbre!\nLa position ({fire_x}, {fire_y}) est: {terrain.name}")
                return
            
            self.current_map, self.burned_positions = self.simulator.simulate_fire(start_pos)

            self._draw_map()
            burned_count = len(self.burned_positions)
            total = self.simulator.width * self.simulator.height
            percentage = (burned_count / total) * 100

            self.status_label.config(text=f"🔥 Feu simulé: {burned_count} cases brûlées ({percentage:.1f}%)")
            self.info_label.config(text=f"Cases brûlées: {burned_count} | Pourcentage: {percentage:.2f}%")

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def _find_best_clearing(self):
        """Trouve la meilleure case à déboiser"""
        if self.simulator is None:
            messagebox.showwarning("Attention", "Veuillez d'abord générer une carte")
            return

        if not self.burned_positions:
            messagebox.showinfo("Info", "Veuillez d'abord simuler un incendie")
            return

        try:
            fire_x = int(self.fire_x_var.get())
            fire_y = int(self.fire_y_var.get())

            if not (0 <= fire_x < self.simulator.width and 0 <= fire_y < self.simulator.height):
                messagebox.showerror("Erreur", "Position de feu invalide")
                return
            
            # Vérifier que c'est un arbre
            terrain = self.simulator.map[fire_y][fire_x]
            if terrain != TerrainType.TREE:
                messagebox.showerror("Erreur", f"❌ Le feu doit démarrer sur un arbre!\nLa position ({fire_x}, {fire_y}) est: {terrain.name}")
                return

            self.status_label.config(text="⏳ Recherche en cours (peut prendre du temps)...")
            self.root.update()

            # Exécuter dans un thread pour ne pas bloquer l'UI
            def search_thread():
                start_pos = Position(fire_x, fire_y)
                self.best_clearing_pos, min_burned = self.simulator.find_best_clearing(start_pos)

                original_burned = len(self.burned_positions)
                reduction = original_burned - min_burned

                self.status_label.config(text=f"✅ Déboisement trouvé: ({self.best_clearing_pos.x}, {self.best_clearing_pos.y})")
                self.info_label.config(text=f"Avant: {original_burned} brûlées | Après: {min_burned} brûlées | Réduction: {reduction} (note: la case du feu est exclue)")

                self._draw_map()

            thread = threading.Thread(target=search_thread, daemon=True)
            thread.start()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def _export_html(self):
        """Exporte le résultat en HTML"""
        if self.simulator is None:
            messagebox.showwarning("Attention", "Veuillez d'abord générer une carte")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )

        if file_path:
            self.simulator.export_to_html(
                file_path,
                self.current_map if self.current_map else self.simulator.map,
                self.burned_positions if self.burned_positions else None,
                self.best_clearing_pos
            )
            messagebox.showinfo("Succès", f"Fichier exporté: {file_path}")
            self.status_label.config(text=f"💾 Exported: {file_path}")

    def _draw_map(self):
        """Dessine la carte sur le canvas"""
        if self.simulator is None or self.current_map is None:
            return

        self.canvas.delete("all")

        map_to_draw = self.current_map if self.current_map else self.simulator.map

        for y in range(self.simulator.height):
            for x in range(self.simulator.width):
                terrain = map_to_draw[y][x]
                color = self.COLORS.get(terrain, '#FFFFFF')

                x0 = x * self.CELL_SIZE
                y0 = y * self.CELL_SIZE
                x1 = x0 + self.CELL_SIZE
                y1 = y0 + self.CELL_SIZE

                # Rectangle pour la cellule
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='#999', width=1)

                # Symbole pour meilleure position de déboisement
                if self.best_clearing_pos and Position(x, y) == self.best_clearing_pos:
                    self.canvas.create_rectangle(x0, y0, x1, y1, outline='red', width=3)
                    self.canvas.create_text(x0 + self.CELL_SIZE//2, y0 + self.CELL_SIZE//2,
                                          text='✂', fill='red', font=('Arial', 12, 'bold'))

    def _canvas_click(self, event):
        """Gère les clics sur le canvas pour sélectionner la position du feu"""
        if self.simulator is None:
            return

        x = event.x // self.CELL_SIZE
        y = event.y // self.CELL_SIZE

        if 0 <= x < self.simulator.width and 0 <= y < self.simulator.height:
            self.fire_x_var.set(str(x))
            self.fire_y_var.set(str(y))


def main():
    """Lance l'application graphique"""
    root = tk.Tk()
    gui = ForestFireGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

