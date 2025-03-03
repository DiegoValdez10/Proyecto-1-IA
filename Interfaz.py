import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import time
import threading
import os
from Laberinto import Laberinto
from Busqueda import busqueda_amplitud, busqueda_profundidad, busqueda_voraz, busqueda_a_estrella
from Heuristica import distancia_euclidiana, distancia_manhattan

def generar_laberinto_aleatorio(laberinto_original, ruta_salida):
    import random
    import copy

    matriz_nueva = copy.deepcopy(laberinto_original.matriz)
    posiciones_validas = []
    for i in range(len(matriz_nueva)):
        for j in range(len(matriz_nueva[0])):
            if matriz_nueva[i][j] == '0':
                posiciones_validas.append((i, j))
    fila_salida, col_salida = laberinto_original.salida
    matriz_nueva[fila_salida][col_salida] = '0'
    

    if posiciones_validas:
        nueva_salida = random.choice(posiciones_validas)
        fila_nueva, col_nueva = nueva_salida
        matriz_nueva[fila_nueva][col_nueva] = '3'
    else:
        matriz_nueva[fila_salida][col_salida] = '3'
        nueva_salida = (fila_salida, col_salida)
    

    with open(ruta_salida, 'w') as archivo:
        for fila in matriz_nueva:
            archivo.write(','.join(fila) + '\n')
    
    return nueva_salida

class AplicacionLaberinto:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de Laberintos")
        self.root.geometry("1200x700")
        
        self.laberinto = None
        self.camino_solucion = None
        self.algoritmo_seleccionado = tk.StringVar()
        self.heuristica_seleccionada = tk.StringVar()
        self.ruta_archivo_actual = None
        
        self.crear_widgets()
    
    def crear_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        control_frame = ttk.LabelFrame(main_frame, text="Controles", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Button(control_frame, text="Cargar Laberinto", command=self.cargar_laberinto).pack(fill=tk.X, pady=5)
        ttk.Button(control_frame, text="Generar Laberinto Aleatorio", command=self.generar_aleatorio).pack(fill=tk.X, pady=5)

        ttk.Label(control_frame, text="Algoritmo:").pack(anchor=tk.W, pady=(10, 5))
        algoritmos = ["BFS", "DFS", "Greedy", "A*"]
        self.algoritmo_seleccionado.set(algoritmos[0])
        ttk.Combobox(control_frame, textvariable=self.algoritmo_seleccionado, values=algoritmos, state="readonly").pack(fill=tk.X, pady=5)

        ttk.Label(control_frame, text="Heurística:").pack(anchor=tk.W, pady=(10, 5))
        heuristicas = ["Euclidiana", "Manhattan"]
        self.heuristica_seleccionada.set(heuristicas[0])
        ttk.Combobox(control_frame, textvariable=self.heuristica_seleccionada, values=heuristicas, state="readonly").pack(fill=tk.X, pady=5)

        ttk.Button(control_frame, text="Resolver", command=self.resolver_laberinto).pack(fill=tk.X, pady=(20, 5))

        self.resultados_frame = ttk.LabelFrame(control_frame, text="Resultados", padding=10)
        self.resultados_frame.pack(fill=tk.X, pady=(20, 5))
        
        self.lbl_nodos = ttk.Label(self.resultados_frame, text="Nodos visitados: -")
        self.lbl_nodos.pack(anchor=tk.W, pady=2)
        
        self.lbl_tiempo = ttk.Label(self.resultados_frame, text="Tiempo: -")
        self.lbl_tiempo.pack(anchor=tk.W, pady=2)
        
        self.lbl_camino = ttk.Label(self.resultados_frame, text="Largo camino: -")
        self.lbl_camino.pack(anchor=tk.W, pady=2)
        
        self.lbl_salida = ttk.Label(self.resultados_frame, text="Posición salida: -")
        self.lbl_salida.pack(anchor=tk.W, pady=2)

        self.canvas_frame = ttk.LabelFrame(main_frame, text="Laberinto", padding=10)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
    
    def cargar_laberinto(self):
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de laberinto",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if ruta_archivo:
            try:
                self.laberinto = Laberinto(ruta_archivo)
                self.ruta_archivo_actual = ruta_archivo
                self.dibujar_laberinto()
                self.lbl_salida.config(text=f"Posición salida: {self.laberinto.salida}")
                messagebox.showinfo("Éxito", "Laberinto cargado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el laberinto: {str(e)}")
    
    def generar_aleatorio(self):
        if not self.laberinto:
            messagebox.showwarning("Advertencia", "Primero debe cargar un laberinto base.")
            return
        

        if not self.ruta_archivo_actual:
            messagebox.showwarning("Advertencia", "No hay un laberinto cargado actualmente.")
            return
            
        directorio = os.path.dirname(self.ruta_archivo_actual)
        nombre_base = os.path.basename(self.ruta_archivo_actual)
        nombre_sin_extension = os.path.splitext(nombre_base)[0]

        ruta_aleatorio = os.path.join(directorio, f"{nombre_sin_extension}_aleatorio.txt")
        

        nueva_salida = generar_laberinto_aleatorio(self.laberinto, ruta_aleatorio)

        try:
            self.laberinto = Laberinto(ruta_aleatorio)
            self.ruta_archivo_actual = ruta_aleatorio
            self.dibujar_laberinto()
            self.lbl_salida.config(text=f"Posición salida: {self.laberinto.salida}")
            messagebox.showinfo("Éxito", f"Laberinto aleatorio generado y guardado en:\n{ruta_aleatorio}\nNueva posición de salida: {nueva_salida}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el laberinto aleatorio: {str(e)}")
    
    def dibujar_laberinto(self):
        if not self.laberinto:
            return
        
        self.canvas.delete("all")
        
        filas = len(self.laberinto.matriz)
        columnas = len(self.laberinto.matriz[0])

        ancho_canvas = self.canvas.winfo_width()
        alto_canvas = self.canvas.winfo_height()
        
        if ancho_canvas <= 1 or alto_canvas <= 1: 
            ancho_canvas = 800
            alto_canvas = 600
        
        ancho_celda = min(ancho_canvas // columnas, alto_canvas // filas)
        

        colores = {
            '0': "white",  
            '1': "black",  
            '2': "green",  
            '3': "red"     
        }
        
        for i in range(filas):
            for j in range(columnas):
                x1 = j * ancho_celda
                y1 = i * ancho_celda
                x2 = x1 + ancho_celda
                y2 = y1 + ancho_celda
                
                color = colores.get(self.laberinto.matriz[i][j], "gray")
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        
        if self.camino_solucion:
            for i, (accion, estado) in enumerate(self.camino_solucion):
                if i == 0 or i == len(self.camino_solucion) - 1:
                    continue  
                
                fila, col = estado
                x1 = col * ancho_celda
                y1 = fila * ancho_celda
                x2 = x1 + ancho_celda
                y2 = y1 + ancho_celda
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="")
    
    def resolver_laberinto(self):
        if not self.laberinto:
            messagebox.showwarning("Advertencia", "Primero debe cargar un laberinto.")
            return
        
        algoritmo = self.algoritmo_seleccionado.get()
        heuristica = self.heuristica_seleccionada.get()
        
        threading.Thread(target=self.ejecutar_algoritmo, args=(algoritmo, heuristica), daemon=True).start()
    
    def ejecutar_algoritmo(self, algoritmo, heuristica_nombre):
        heuristica_func = distancia_euclidiana if heuristica_nombre == "Euclidiana" else distancia_manhattan
        
        inicio = time.time()
        if algoritmo == "BFS":
            resultado = busqueda_amplitud(self.laberinto)
        elif algoritmo == "DFS":
            resultado = busqueda_profundidad(self.laberinto)
        elif algoritmo == "Greedy":
            resultado = busqueda_voraz(self.laberinto, heuristica_func)
        elif algoritmo == "A*":
            resultado = busqueda_a_estrella(self.laberinto, heuristica_func)
        
        self.root.after(0, lambda: self.actualizar_resultados(resultado))
    
    def actualizar_resultados(self, resultado):
        self.lbl_nodos.config(text=f"Nodos visitados: {resultado['nodos_visitados']}")
        self.lbl_tiempo.config(text=f"Tiempo: {resultado['tiempo']:.6f} segundos")
        
        if resultado['camino']:
            self.lbl_camino.config(text=f"Largo camino: {resultado['largo_camino']}")
            self.camino_solucion = resultado['camino']
        else:
            self.lbl_camino.config(text="Largo camino: No se encontró solución")
            self.camino_solucion = None

        self.dibujar_laberinto()

def main():
    root = tk.Tk()
    app = AplicacionLaberinto(root)
    root.mainloop()

if __name__ == "__main__":
    main()