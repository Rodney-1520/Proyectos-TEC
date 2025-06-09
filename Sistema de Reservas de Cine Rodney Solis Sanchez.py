import tkinter as tk
from tkinter import messagebox
import random

#Salas por defecto 
matriz1 = [["L" for _ in range(10)] for _ in range(10)]
matriz2 = [["L" for _ in range(15)] for _ in range(10)]
matriz3 = [["L" for _ in range(20)] for _ in range(20)]
matriz4 = [["L" for _ in range(8)] for _ in range(12)]
 
salas = [
]

#Salir del programa
def salir():
    ventana.destroy()

#Crear nueva sala
def crear_sala():
    def confirmar():
        try:
            filas = int(entrada_filas.get())
            columnas = int(entrada_columnas.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese números válidos.")
            return
        if filas <= 0 or columnas <= 0 or filas > 100 or columnas > 100:
            messagebox.showerror("Error", "Las dimensiones deben estar entre 1 y 100.")
            return

        matriz = []
        f = 0
        while f < filas:
            fila = []
            c = 0
            while c < columnas:
                fila.append("L")
                c += 1
            matriz.append(fila)
            f += 1

        nueva_sala = ["", 0, matriz, 0]
        salas.append(nueva_sala)
        num_sala = len(salas)

        mostrar_matriz_asientos(matriz, f"¡Sala {num_sala} creada exitosamente!")

        ventana_crear.destroy()

    ventana_crear = tk.Toplevel()
    ventana_crear.title("Crear nueva sala")

    tk.Label(ventana_crear, text="Número de filas:").grid(row=0, column=0)
    entrada_filas = tk.Entry(ventana_crear)
    entrada_filas.grid(row=0, column=1)

    tk.Label(ventana_crear, text="Número de columnas:").grid(row=1, column=0)
    entrada_columnas = tk.Entry(ventana_crear)
    entrada_columnas.grid(row=1, column=1)

    tk.Button(ventana_crear, text="Crear sala", command=confirmar).grid(row=2, column=0, columnspan=2, pady=10)

def mostrar_matriz_asientos(matriz, mensaje):
    ventana_matriz = tk.Toplevel()
    ventana_matriz.title("Vista de la sala")

    contenedor = tk.Frame(ventana_matriz)
    contenedor.pack(fill="both", expand=True)

    canvas = tk.Canvas(contenedor, bg="white")
    canvas.pack(side="left", fill="both", expand=True)

    scroll_y = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    scroll_y.pack(side="right", fill="y")

    scroll_x = tk.Scrollbar(ventana_matriz, orient="horizontal", command=canvas.xview)
    scroll_x.pack(side="bottom", fill="x")

    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    frame_sala = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=frame_sala, anchor="nw")

    alto = len(matriz)
    ancho = len(matriz[0])

    pantalla = tk.Label(frame_sala, text="PANTALLA", bg="black", fg="white", font=("Arial", 12, "bold"), width=ancho * 3)
    pantalla.grid(row=0, column=0, columnspan=ancho, pady=(10, 20))

    fila = 0
    while fila < alto:
        letra = chr(fila + 65)  
        columna = 0
        while columna < ancho:
            numero = columna + 1
            asiento = letra + str(numero)

            asiento_frame = tk.Frame(frame_sala, width=35, height=35, bg="gray", highlightbackground="black", highlightthickness=1)
            asiento_frame.grid(row=fila+1, column=columna, padx=2, pady=2)
            asiento_label = tk.Label(asiento_frame, text=asiento, bg="gray", fg="white", font=("Arial", 9))
            asiento_label.place(relx=0.5, rely=0.5, anchor="center")

            columna += 1
        fila += 1

    frame_sala.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    messagebox.showinfo("Éxito", mensaje)

#Asignar los datos a cada sala de cine
def asignar_pelicula_precio():
    if len(salas) == 0:
        messagebox.showwarning("Aviso", "No hay salas creadas aún.")
        return

    ventana_selector = tk.Toplevel()
    ventana_selector.title("Seleccionar sala para asignar datos")

    tk.Label(ventana_selector, text="Seleccione una sala", font=("Arial", 12)).pack(pady=10)
    frame_salitas = tk.Frame(ventana_selector)
    frame_salitas.pack(padx=10, pady=10)

    def agregar_datos(index):
        ventana_selector.destroy()

        ventana_asignar = tk.Toplevel()
        ventana_asignar.title(f"Asigna datos a Sala {index + 1}")

        tk.Label(ventana_asignar, text=f"Sala {index + 1}", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(ventana_asignar, text="Película:").grid(row=1, column=0, sticky="e")
        entrada_pelicula = tk.Entry(ventana_asignar)
        entrada_pelicula.grid(row=1, column=1)

        tk.Label(ventana_asignar, text="Precio entrada:").grid(row=2, column=0, sticky="e")
        entrada_precio = tk.Entry(ventana_asignar)
        entrada_precio.grid(row=2, column=1)

        def confirmar():
            nombre = entrada_pelicula.get().strip()
            try:
                precio = int(entrada_precio.get())
            except ValueError:
                messagebox.showerror("Error", "Precio inválido.")
                return

            if nombre == "" or precio <= 0:
                messagebox.showerror("Error", "Debe ingresar un nombre y un precio válido.")
                return

            salas[index][0] = nombre
            salas[index][1] = precio
            messagebox.showinfo("Éxito", f"Película y precio asignados a la Sala {index + 1}")
            ventana_asignar.destroy()

        tk.Button(ventana_asignar, text="Guardar", command=confirmar).grid(row=3, column=0, columnspan=2, pady=10)

    i = 0
    while i < len(salas):
        nombre = salas[i][0]
        precio = salas[i][1]
        texto_boton = f"Sala {i + 1} - {nombre}" if nombre != "" and precio > 0 else f"Sala {i + 1} (Sin asignar)"

        boton_sala = tk.Button(frame_salitas, text=texto_boton, width=18, height=3,
                               bg="gray", fg="white", font=("Arial", 10),
                               command=lambda i=i: agregar_datos(i))
        boton_sala.grid(row=i // 4, column=i % 4, padx=5, pady=5)
        i += 1

    i = 0
    while i < len(salas):
        nombre = salas[i][0]
        precio = salas[i][1]
        texto_boton = f"Sala {i + 1} - {nombre}" if nombre != "" and precio > 0 else f"Sala {i + 1} (Sin asignar)"

        boton_sala = tk.Button(frame_salitas, text=texto_boton, width=18, height=3,
                               bg="gray", fg="white", font=("Arial", 10),
                               command=lambda i=i: agregar_datos(i))
        boton_sala.grid(row=i // 4, column=i % 4, padx=5, pady=5)
        i += 1
    
#Poder ver el estado actual de cada sala
def ver_estado_sala():
    if len(salas) == 0:
        messagebox.showwarning("Aviso", "No hay salas creadas aún.")
        return

    ventana_selector = tk.Toplevel()
    ventana_selector.title("Seleccionar sala para ver estado")

    tk.Label(ventana_selector, text="Seleccione una sala", font=("Arial", 12)).pack(pady=10)

    frame_salitas = tk.Frame(ventana_selector)
    frame_salitas.pack(padx=10, pady=10)

    def mostrar_estado(index):
        ventana_selector.destroy()
        sala = salas[index]
        matriz = sala[2]
        pelicula = sala[0] if sala[0] != "" else "(sin asignar)"
        precio = sala[1]
        vendidos = sala[3]

        ventana_estado = tk.Toplevel()
        ventana_estado.title(f"Estado de Sala {index + 1}")

        contenedor = tk.Frame(ventana_estado)
        contenedor.pack(fill="both", expand=True)

        canvas = tk.Canvas(contenedor, bg="white")
        canvas.pack(side="left", fill="both", expand=True)

        scroll_y = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        scroll_y.pack(side="right", fill="y")

        scroll_x = tk.Scrollbar(ventana_estado, orient="horizontal", command=canvas.xview)
        scroll_x.pack(side="bottom", fill="x")

        canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        frame_sala = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=frame_sala, anchor="nw")

        alto = len(matriz)
        ancho = len(matriz[0])
        total = alto * ancho
        ocupados = 0

        pantalla = tk.Label(frame_sala, text="PANTALLA", bg="black", fg="white", font=("Arial", 12, "bold"), width=ancho * 3)
        pantalla.grid(row=0, column=0, columnspan=ancho, pady=(10, 20))

        fila = 0
        while fila < alto:
            letra = chr(fila + 65)
            columna = 0
            while columna < ancho:
                numero = columna + 1
                asiento = letra + str(numero)

                estado = matriz[fila][columna]
                color = "gray" if estado == "L" else "red"
                if estado == "X":
                    ocupados += 1

                frame_asiento = tk.Frame(frame_sala, width=35, height=35, bg=color, highlightbackground="black", highlightthickness=1)
                frame_asiento.grid(row=fila + 1, column=columna, padx=2, pady=2)

                etiqueta = tk.Label(frame_asiento, text=asiento, bg=color, fg="white", font=("Arial", 9))
                etiqueta.place(relx=0.5, rely=0.5, anchor="center")

                columna += 1
            fila += 1

        frame_sala.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        porcentaje = (ocupados / total) * 100

        resumen = f"Película: {pelicula}\nPrecio: {precio}\nAsientos totales: {total}\nReservados: {ocupados}\nOcupación: {porcentaje:.2f}%"
        tk.Label(ventana_estado, text=resumen, font=("Arial", 11), justify="left").pack(pady=10)

    i = 0
    while i < len(salas):
        nombre = salas[i][0]
        precio = salas[i][1]
        texto_boton = f"Sala {i + 1} - {nombre}" if nombre != "" and precio > 0 else f"Sala {i + 1} (Sin asignar)"

        boton_sala = tk.Button(frame_salitas, text=texto_boton, width=18, height=3,
                               bg="gray", fg="white", font=("Arial", 10),
                               command=lambda i=i: mostrar_estado(i))
        boton_sala.grid(row=i // 4, column=i % 4, padx=5, pady=5)
        i += 1
        
#Para poder reservar un solo asiento a la vez
def reservar_asiento():
    if len(salas) == 0:
        messagebox.showwarning("Aviso", "No hay salas disponibles.")
        return

    ventana_selector = tk.Toplevel()
    ventana_selector.title("Seleccionar sala para reservar")

    tk.Label(ventana_selector, text="Seleccione una sala", font=("Arial", 12)).pack(pady=10)
    frame_salitas = tk.Frame(ventana_selector)
    frame_salitas.pack(padx=10, pady=10)

    salas_validas = []
    for i in range(len(salas)):
        if salas[i][0] != "" and salas[i][1] > 0:
            salas_validas.append(i)

    if len(salas_validas) == 0:
        tk.Label(frame_salitas, text="No hay salas asignadas disponibles", font=("Arial", 11), fg="red").pack(pady=10)
        return

    def abrir_sala(index):
        ventana_selector.destroy()
        sala = salas[index]
        matriz = sala[2]
        precio = sala[1]

        seleccionados = []

        ventana_reserva = tk.Toplevel()
        ventana_reserva.title(f"Reservar en Sala {index + 1}")

        frame_superior = tk.Frame(ventana_reserva)
        frame_superior.pack(pady=10)

        texto_info = tk.StringVar()
        texto_info.set(f"Precio por entrada: {precio}  |  Asientos seleccionados: 0  |  Total: 0")
        tk.Label(frame_superior, textvariable=texto_info, font=("Arial", 11)).pack()

        def confirmar():
            for fila, col in seleccionados:
                if matriz[fila][col] == "L":
                    matriz[fila][col] = "X"
                    sala[3] += 1
            messagebox.showinfo("Reserva confirmada", "¡Reserva realizada con éxito!")
            ventana_reserva.destroy()

        boton_confirmar = tk.Button(frame_superior, text="Confirmar reserva", bg="skyblue", font=("Arial", 10), command=confirmar)
        boton_confirmar.pack(pady=5)

        contenedor = tk.Frame(ventana_reserva)
        contenedor.pack(fill="both", expand=True)

        canvas = tk.Canvas(contenedor, bg="white")
        canvas.pack(side="left", fill="both", expand=True)

        scroll_y = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        scroll_y.pack(side="right", fill="y")

        scroll_x = tk.Scrollbar(ventana_reserva, orient="horizontal", command=canvas.xview)
        scroll_x.pack(side="bottom", fill="x")

        canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        frame_sala = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=frame_sala, anchor="nw")

        alto = len(matriz)
        ancho = len(matriz[0])

        nombre_pelicula = sala[0]
        etiqueta_pelicula = tk.Label(frame_sala, text=f"Película: {nombre_pelicula}", font=("Arial", 11, "bold"), bg="white")
        etiqueta_pelicula.grid(row=0, column=0, columnspan=ancho, pady=(10, 0))

        pantalla = tk.Label(frame_sala, text="PANTALLA", bg="black", fg="white", font=("Arial", 12, "bold"), width=ancho * 3)
        pantalla.grid(row=1, column=0, columnspan=ancho, pady=(5, 20))

        def actualizar_info():
            cantidad = len(seleccionados)
            total = cantidad * precio
            texto_info.set(f"Precio por entrada: {precio}  |  Asientos seleccionados: {cantidad}  |  Total: {total}")

        def alternar_asiento(fila, col, boton):
            if matriz[fila][col] == "X":
                return
            if (fila, col) in seleccionados:
                seleccionados.remove((fila, col))
                boton.configure(bg="gray")
            else:
                if len(seleccionados) < 1:
                    seleccionados.append((fila, col))
                    boton.configure(bg="green")
            actualizar_info()

        btn_refs = [[None for _ in range(ancho)] for _ in range(alto)]

        f = 0
        while f < alto:
            letra = chr(f + 65)
            c = 0
            while c < ancho:
                numero = c + 1
                estado = matriz[f][c]
                color = "red" if estado == "X" else "gray"
                asiento = f"{letra}{numero}"

                btn = tk.Button(frame_sala, text=asiento, bg=color, fg="white", width=4, height=2)
                btn.configure(command=lambda f=f, c=c, b=btn: alternar_asiento(f, c, b))
                btn_refs[f][c] = btn
                btn.grid(row=f + 2, column=c, padx=2, pady=2)
                c += 1
            f += 1

        frame_sala.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    fila = 0
    col = 0
    for i in salas_validas:
        texto_boton = f"Sala {i + 1} - {salas[i][0]}"
        boton = tk.Button(frame_salitas, text=texto_boton, width=25, height=3,
                          bg="gray", fg="white", font=("Arial", 10),
                          command=lambda i=i: abrir_sala(i))
        boton.grid(row=fila, column=col, padx=5, pady=5)
        col += 1
        if col == 2:
            col = 0
            fila += 1

#Funcion para cancelar la reserva del o los asientos
def cancelar_reserva():
    if len(salas) == 0:
        messagebox.showwarning("Aviso", "No hay salas disponibles.")
        return

    ventana_selector = tk.Toplevel()
    ventana_selector.title("Seleccionar sala para cancelar reservas")

    tk.Label(ventana_selector, text="Seleccione una sala", font=("Arial", 12)).pack(pady=10)
    frame_salitas = tk.Frame(ventana_selector)
    frame_salitas.pack(padx=10, pady=10)

    salas_asignadas = []
    for i in range(len(salas)):
        if salas[i][0] != "" and salas[i][1] > 0:
            salas_asignadas.append(i)

    if len(salas_asignadas) == 0:
        tk.Label(frame_salitas, text="No hay salas asignadas disponibles", font=("Arial", 11), fg="red").pack(pady=10)
        return

    def abrir_sala(index):
        ventana_selector.destroy()
        sala = salas[index]
        matriz = sala[2]
        seleccionados = []

        ventana_cancelar = tk.Toplevel()
        ventana_cancelar.title(f"Cancelar reservas en Sala {index + 1}")

        frame_superior = tk.Frame(ventana_cancelar)
        frame_superior.pack(pady=10)

        texto_info = tk.StringVar()
        texto_info.set(f"Asientos seleccionados para cancelar: 0")
        tk.Label(frame_superior, textvariable=texto_info, font=("Arial", 11)).pack()

        def confirmar_cancelacion():
            cantidad = 0
            for fila, col in seleccionados:
                if matriz[fila][col] == "X":
                    matriz[fila][col] = "L"
                    sala[3] -= 1
                    cantidad += 1
            messagebox.showinfo("Reservas canceladas", f"Se cancelaron {cantidad} reservas.")
            ventana_cancelar.destroy()

        boton_confirmar = tk.Button(frame_superior, text="Confirmar cancelación", bg="orange", font=("Arial", 10),
                                    command=confirmar_cancelacion)
        boton_confirmar.pack(pady=5)

        contenedor = tk.Frame(ventana_cancelar)
        contenedor.pack(fill="both", expand=True)

        canvas = tk.Canvas(contenedor, bg="white")
        canvas.pack(side="left", fill="both", expand=True)

        scroll_y = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        scroll_y.pack(side="right", fill="y")

        scroll_x = tk.Scrollbar(ventana_cancelar, orient="horizontal", command=canvas.xview)
        scroll_x.pack(side="bottom", fill="x")

        canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        frame_sala = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=frame_sala, anchor="nw")

        alto = len(matriz)
        ancho = len(matriz[0])

        nombre_pelicula = sala[0]
        etiqueta_pelicula = tk.Label(frame_sala, text=f"Película: {nombre_pelicula}", font=("Arial", 11, "bold"), bg="white")
        etiqueta_pelicula.grid(row=0, column=0, columnspan=ancho, pady=(10, 0))

        pantalla = tk.Label(frame_sala, text="PANTALLA", bg="black", fg="white", font=("Arial", 12, "bold"), width=ancho * 3)
        pantalla.grid(row=1, column=0, columnspan=ancho, pady=(5, 20))

        def actualizar_info():
            texto_info.set(f"Asientos seleccionados para cancelar: {len(seleccionados)}")

        def alternar_cancelacion(fila, col, boton):
            if matriz[fila][col] != "X":
                return
            if (fila, col) in seleccionados:
                seleccionados.remove((fila, col))
                boton.configure(bg="red")
            else:
                seleccionados.append((fila, col))
                boton.configure(bg="orange")
            actualizar_info()

        f = 0
        while f < alto:
            letra = chr(f + 65)
            c = 0
            while c < ancho:
                numero = c + 1
                estado = matriz[f][c]
                asiento = f"{letra}{numero}"
                color = "red" if estado == "X" else "gray"

                btn = tk.Button(frame_sala, text=asiento, bg=color, fg="white", width=4, height=2)
                if estado == "X":
                    btn.configure(command=lambda f=f, c=c, b=btn: alternar_cancelacion(f, c, b))
                btn.grid(row=f + 2, column=c, padx=2, pady=2)
                c += 1
            f += 1

        frame_sala.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    fila = 0
    col = 0
    for i in salas_asignadas:
        nombre = salas[i][0]
        texto_boton = f"Sala {i + 1} - {nombre}"
        boton = tk.Button(frame_salitas, text=texto_boton, width=25, height=3,
                          bg="gray", fg="white", font=("Arial", 10),
                          command=lambda i=i: abrir_sala(i))
        boton.grid(row=fila, column=col, padx=5, pady=5)
        col += 1
        if col == 2:
            col = 0
            fila += 1

#Para poder ver las estadisticas de ocupacion de las salas
def ver_estadisticas_ocupacion():
    if len(salas) == 0:
        messagebox.showwarning("Aviso", "No hay salas disponibles.")
        return

    ventana_selector = tk.Toplevel()
    ventana_selector.title("Seleccionar sala para ver estadísticas de ocupación")

    tk.Label(ventana_selector, text="Seleccione una sala", font=("Arial", 12)).pack(pady=10)
    frame_salitas = tk.Frame(ventana_selector)
    frame_salitas.pack(padx=10, pady=10)

    salas_validas = []
    for i in range(len(salas)):
        if salas[i][0] != "" and salas[i][1] > 0:
            salas_validas.append(i)

    if len(salas_validas) == 0:
        tk.Label(frame_salitas, text="No hay salas asignadas disponibles", font=("Arial", 11), fg="red").pack(pady=10)
        return

    def mostrar_estadisticas(index):
        ventana_selector.destroy()
        sala = salas[index]
        matriz = sala[2]
        pelicula = sala[0]

        total = 0
        ocupados = 0
        filas = len(matriz)
        columnas = len(matriz[0])

        f = 0
        while f < filas:
            c = 0
            while c < columnas:
                total += 1
                if matriz[f][c] == "X":
                    ocupados += 1
                c += 1
            f += 1

        porcentaje = (ocupados / total) * 100

        ventana_datos = tk.Toplevel()
        ventana_datos.title(f"Estadísticas de Sala {index + 1}")

        mensaje = f"""Sala {index + 1} - {pelicula}
Asientos totales: {total}
Reservados: {ocupados}
Porcentaje de ocupación: {porcentaje:.2f}%"""

        tk.Label(ventana_datos, text=mensaje, font=("Arial", 12), justify="left").pack(padx=15, pady=15)

    fila = 0
    col = 0
    for i in salas_validas:
        texto_boton = f"Sala {i + 1} - {salas[i][0]}"
        boton = tk.Button(frame_salitas, text=texto_boton, width=25, height=3,
                          bg="gray", fg="white", font=("Arial", 10),
                          command=lambda i=i: mostrar_estadisticas(i))
        boton.grid(row=fila, column=col, padx=5, pady=5)
        col += 1
        if col == 2:
            col = 0
            fila += 1

#Para poder las estadisticas de recaudacion de las distintas salas
def ver_estadisticas_recaudacion():
    if len(salas) == 0:
        messagebox.showwarning("Aviso", "No hay salas creadas aún.")
        return

    ventana_selector = tk.Toplevel()
    ventana_selector.title("Seleccionar sala para ver recaudación")

    tk.Label(ventana_selector, text="Seleccione una sala", font=("Arial", 12)).pack(pady=10)
    frame_salitas = tk.Frame(ventana_selector)
    frame_salitas.pack(padx=10, pady=10)

    salas_validas = []
    for i in range(len(salas)):
        if salas[i][0] != "" and salas[i][1] > 0:
            salas_validas.append(i)

    if len(salas_validas) == 0:
        tk.Label(frame_salitas, text="No hay salas asignadas disponibles", font=("Arial", 11), fg="red").pack(pady=10)
        return

    def mostrar_recaudacion(index):
        ventana_selector.destroy()
        sala = salas[index]
        nombre = sala[0]
        precio = sala[1]
        vendidos = sala[3]
        total = precio * vendidos

        ventana_datos = tk.Toplevel()
        ventana_datos.title(f"Recaudación - Sala {index + 1}")

        mensaje = f"""Sala {index + 1} - {nombre}
Entradas vendidas: {vendidos}
Precio por entrada: {precio}
Total recaudado: {total}"""

        tk.Label(ventana_datos, text=mensaje, font=("Arial", 12), justify="left").pack(padx=15, pady=15)

    fila = 0
    col = 0
    for i in salas_validas:
        texto_boton = f"Sala {i + 1} - {salas[i][0]}"
        boton = tk.Button(frame_salitas, text=texto_boton, width=25, height=3,
                          bg="gray", fg="white", font=("Arial", 10),
                          command=lambda i=i: mostrar_recaudacion(i))
        boton.grid(row=fila, column=col, padx=5, pady=5)
        col += 1
        if col == 2:
            col = 0
            fila += 1
            
#Buscador de sala por pelicula
def buscar_sala_por_pelicula():
    if len(salas) == 0:
        messagebox.showwarning("Aviso", "No hay salas disponibles.")
        return

    ventana_busqueda = tk.Toplevel()
    ventana_busqueda.title("Buscar sala por nombre de película")

    tk.Label(ventana_busqueda, text="Ingrese el nombre de la película:", font=("Arial", 11)).pack(pady=10)
    entrada = tk.Entry(ventana_busqueda, width=30)
    entrada.pack(pady=5)

    resultado = tk.Text(ventana_busqueda, height=10, width=50, state="disabled")
    resultado.pack(padx=10, pady=10)

    def realizar_busqueda():
        nombre = entrada.get().strip().lower()
        resultado.configure(state="normal")
        resultado.delete(1.0, "end")

        if nombre == "":
            resultado.insert("end", "Por favor, escriba el nombre de la película.\n")
        else:
            encontrado = False
            i = 0
            while i < len(salas):
                sala_nombre = salas[i][0].lower()
                if sala_nombre == nombre and salas[i][1] > 0:
                    matriz = salas[i][2]
                    libres = 0
                    f = 0
                    while f < len(matriz):
                        c = 0
                        while c < len(matriz[0]):
                            if matriz[f][c] == "L":
                                libres += 1
                            c += 1
                        f += 1
                    resultado.insert("end", f"- Sala {i + 1} (asientos disponibles: {libres})\n")
                    encontrado = True
                i += 1

            if not encontrado:
                resultado.insert("end", f"No se encontraron salas proyectando: \"{nombre}\"\n")

        resultado.configure(state="disabled")

    tk.Button(ventana_busqueda, text="Buscar", command=realizar_busqueda).pack(pady=5)

#Para visualizar las funciones disponibles
def ver_funciones_disponibles():
    if len(salas) == 0:
        messagebox.showwarning("Aviso", "No hay salas disponibles.")
        return

    ventana_funciones = tk.Toplevel()
    ventana_funciones.title("Funciones disponibles")

    tk.Label(ventana_funciones, text="--- Funciones disponibles ---", font=("Arial", 13, "bold")).pack(pady=10)

    resultado = tk.Text(ventana_funciones, height=15, width=50, state="normal")
    resultado.pack(padx=15, pady=10)

    funciones_encontradas = False
    i = 0
    while i < len(salas):
        sala = salas[i]
        nombre = sala[0]
        precio = sala[1]
        matriz = sala[2]

        if nombre != "" and precio > 0:
            libres = 0
            f = 0
            while f < len(matriz):
                c = 0
                while c < len(matriz[0]):
                    if matriz[f][c] == "L":
                        libres += 1
                    c += 1
                f += 1

            resultado.insert("end", f"Sala {i + 1} - {nombre}\n")
            resultado.insert("end", f"Precio: {precio}\n")
            resultado.insert("end", f"Asientos disponibles: {libres}\n\n")
            funciones_encontradas = True
        i += 1

    if not funciones_encontradas:
        resultado.insert("end", "No hay funciones disponibles.")

    resultado.config(state="disabled")

def reservar_asientos_consecutivos():
    if len(salas) == 0:
        messagebox.showwarning("Aviso", "No hay salas disponibles.")
        return

    ventana_selector = tk.Toplevel()
    ventana_selector.title("Seleccionar sala para reservar varios asientos")

    tk.Label(ventana_selector, text="Seleccione una sala", font=("Arial", 12)).pack(pady=10)
    frame_salitas = tk.Frame(ventana_selector)
    frame_salitas.pack(padx=10, pady=10)

    salas_validas = []
    for i in range(len(salas)):
        if salas[i][0] != "" and salas[i][1] > 0:
            salas_validas.append(i)

    if len(salas_validas) == 0:
        tk.Label(frame_salitas, text="No hay salas asignadas disponibles", font=("Arial", 11), fg="red").pack(pady=10)
        return

    def abrir_sala(index):
        ventana_selector.destroy()
        sala = salas[index]
        matriz = sala[2]
        precio = sala[1]

        seleccionados = []

        ventana_reserva = tk.Toplevel()
        ventana_reserva.title(f"Reserva múltiple en Sala {index + 1}")

        frame_superior = tk.Frame(ventana_reserva)
        frame_superior.pack(pady=10)

        texto_info = tk.StringVar()
        texto_info.set(f"Precio por entrada: {precio}  |  Asientos seleccionados: 0  |  Total: 0")
        tk.Label(frame_superior, textvariable=texto_info, font=("Arial", 11)).pack()

        def confirmar():
            for fila, col in seleccionados:
                if matriz[fila][col] == "L":
                    matriz[fila][col] = "X"
                    sala[3] += 1
            messagebox.showinfo("Reserva confirmada", f"¡Se reservaron {len(seleccionados)} asientos exitosamente!")
            ventana_reserva.destroy()

        boton_confirmar = tk.Button(frame_superior, text="Confirmar reserva", bg="skyblue", font=("Arial", 10), command=confirmar)
        boton_confirmar.pack(pady=5)

        contenedor = tk.Frame(ventana_reserva)
        contenedor.pack(fill="both", expand=True)

        canvas = tk.Canvas(contenedor, bg="white")
        canvas.pack(side="left", fill="both", expand=True)

        scroll_y = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        scroll_y.pack(side="right", fill="y")

        scroll_x = tk.Scrollbar(ventana_reserva, orient="horizontal", command=canvas.xview)
        scroll_x.pack(side="bottom", fill="x")

        canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        frame_sala = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=frame_sala, anchor="nw")

        alto = len(matriz)
        ancho = len(matriz[0])

        nombre_pelicula = sala[0]
        etiqueta_pelicula = tk.Label(frame_sala, text=f"Película: {nombre_pelicula}", font=("Arial", 11, "bold"), bg="white")
        etiqueta_pelicula.grid(row=0, column=0, columnspan=ancho, pady=(10, 0))

        pantalla = tk.Label(frame_sala, text="PANTALLA", bg="black", fg="white", font=("Arial", 12, "bold"), width=ancho * 3)
        pantalla.grid(row=1, column=0, columnspan=ancho, pady=(5, 20))

        def actualizar_info():
            cantidad = len(seleccionados)
            total = cantidad * precio
            texto_info.set(f"Precio por entrada: {precio}  |  Asientos seleccionados: {cantidad}  |  Total: {total}")

        def alternar_asiento(fila, col, boton):
            if matriz[fila][col] == "X":
                return
            elif (fila, col) in seleccionados:
                seleccionados.remove((fila, col))
                boton.configure(bg="gray")
            else:
                seleccionados.append((fila, col))
                boton.configure(bg="green")
            actualizar_info()

        btn_refs = [[None for _ in range(ancho)] for _ in range(alto)]

        f = 0
        while f < alto:
            letra = chr(f + 65)
            c = 0
            while c < ancho:
                numero = c + 1
                estado = matriz[f][c]
                color = "red" if estado == "X" else "gray"
                asiento = f"{letra}{numero}"

                btn = tk.Button(frame_sala, text=asiento, bg=color, fg="white", width=4, height=2)
                btn.configure(command=lambda f=f, c=c, b=btn: alternar_asiento(f, c, b))
                btn_refs[f][c] = btn
                btn.grid(row=f + 2, column=c, padx=2, pady=2)
                c += 1
            f += 1

        frame_sala.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    fila = 0
    col = 0
    for i in salas_validas:
        texto_boton = f"Sala {i + 1} - {salas[i][0]}"
        boton = tk.Button(frame_salitas, text=texto_boton, width=25, height=3,
                          bg="gray", fg="white", font=("Arial", 10),
                          command=lambda i=i: abrir_sala(i))
        boton.grid(row=fila, column=col, padx=5, pady=5)
        col += 1
        if col == 2:
            col = 0
            fila += 1

#Simulador de ventas masivas
def simular_venta_masiva():
    if len(salas) == 0:
        messagebox.showwarning("Aviso", "No hay salas disponibles.")
        return

    ventana_simular = tk.Toplevel()
    ventana_simular.title("Simular venta masiva")

    tk.Label(ventana_simular, text="Ingrese el porcentaje de venta (1 a 100):", font=("Arial", 11)).pack(pady=10)
    entrada = tk.Entry(ventana_simular)
    entrada.pack(pady=5)

    def procesar():
        try:
            porcentaje = int(entrada.get())
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número entero.")
            return

        if porcentaje < 1 or porcentaje > 100:
            messagebox.showerror("Error", "El porcentaje debe estar entre 1 y 100.")
            return

        for sala in salas:
            nombre = sala[0]
            precio = sala[1]
            matriz = sala[2]

            if nombre != "" and precio > 0:
                total = len(matriz) * len(matriz[0])
                meta = int((porcentaje / 100) * total)

                actuales = 0
                disponibles = []
                for f in range(len(matriz)):
                    for c in range(len(matriz[0])):
                        if matriz[f][c] == "X":
                            actuales += 1
                        elif matriz[f][c] == "L":
                            disponibles.append((f, c))

                if actuales >= meta:
                    continue

                a_reservar = meta - actuales
                if a_reservar > len(disponibles):
                    a_reservar = len(disponibles)

                seleccionados = random.sample(disponibles, a_reservar)
                for f, c in seleccionados:
                    matriz[f][c] = "X"
                    sala[3] += 1

        messagebox.showinfo("Simulación completada", "Se realizó la venta masiva según el porcentaje dado.")
        ventana_simular.destroy()

    tk.Button(ventana_simular, text="Confirmar", bg="skyblue", command=procesar).pack(pady=10)
    
#Para reiniciar las salas de cine
def reiniciar_sala():
    if len(salas) == 0:
        messagebox.showwarning("Aviso", "No hay salas creadas.")
        return

    ventana_selector = tk.Toplevel()
    ventana_selector.title("Reiniciar una sala")

    tk.Label(ventana_selector, text="Seleccione una sala para reiniciar", font=("Arial", 12)).pack(pady=10)
    frame_salitas = tk.Frame(ventana_selector)
    frame_salitas.pack(padx=10, pady=10)

    salas_validas = []
    for i in range(len(salas)):
        if salas[i][0] != "" and salas[i][1] > 0:
            salas_validas.append(i)

    if len(salas_validas) == 0:
        tk.Label(frame_salitas, text="No hay salas asignadas disponibles", font=("Arial", 11), fg="red").pack(pady=10)
        return

    def reiniciar(index):
        sala = salas[index]
        matriz = sala[2]
        for f in range(len(matriz)):
            for c in range(len(matriz[0])):
                matriz[f][c] = "L"
        sala[3] = 0
        messagebox.showinfo("Éxito", f"Todos los asientos de la Sala {index + 1} fueron liberados.")
        ventana_selector.destroy()

    fila = 0
    col = 0
    for i in salas_validas:
        texto_boton = f"Sala {i + 1} - {salas[i][0]}"
        boton = tk.Button(frame_salitas, text=texto_boton, width=25, height=3,
                          bg="gray", fg="white", font=("Arial", 10),
                          command=lambda i=i: reiniciar(i))
        boton.grid(row=fila, column=col, padx=5, pady=5)
        col += 1
        if col == 2:
            col = 0
            fila += 1

ventana = tk.Tk()
ventana.title("Sistema de Reservas de Cine")
ventana.geometry("400x700")

tk.Label(ventana, text="Menú Principal", font=("Arial", 16, "bold")).pack(pady=10)

opciones = [
    "1. Crear nueva sala",
    "2. Asignar película y precio a sala",
    "3. Ver estado de una sala",
    "4. Reservar asiento",
    "5. Cancelar reserva",
    "6. Ver estadísticas de ocupación",
    "7. Ver estadísticas de recaudación",
    "8. Buscar sala por nombre de película",
    "9. Ver funciones disponibles",
    "10. Reservar varios asientos consecutivos",
    "11. Simular venta masiva",
    "12. Reiniciar sala",
    "13. Salir"
]

i = 1
for texto in opciones:
    if i == 1:
        boton = tk.Button(ventana, text=texto, width=40, height=2, command=crear_sala)
    elif i == 2:
        boton = tk.Button(ventana, text=texto, width=40, height=2, command=asignar_pelicula_precio)
    elif i == 3:
        boton = tk.Button(ventana, text=texto, width=40, height=2, command=ver_estado_sala)
    elif i == 4:
        boton = tk.Button(ventana, text=texto, width=40, height=2, command=reservar_asiento)
    elif i == 5:
        boton = tk.Button(ventana, text=texto, width=40, height=2, command=cancelar_reserva)
    elif i == 6:
        boton = tk.Button(ventana, text=texto, width=40, height=2, command=ver_estadisticas_ocupacion)
    elif i == 7:
        boton = tk.Button(ventana, text=texto, width=40, height=2, command=ver_estadisticas_recaudacion)
    elif i == 8:
        boton = tk.Button(ventana, text=texto, width=40, height=2, command=buscar_sala_por_pelicula)
    elif i == 9:
        boton = tk.Button(ventana, text=texto, width=40, height=2, command=ver_funciones_disponibles)
    elif i == 10:
        boton = tk.Button(ventana, text=texto, width=40, height=2, command=reservar_asientos_consecutivos)
    elif i == 11:
        boton = tk.Button(ventana, text=texto, width=40, height=2, command=simular_venta_masiva)
    elif i == 12:
        boton = tk.Button(ventana, text=texto, width=40, height=2, command=reiniciar_sala)
    elif i == 13:
        boton = tk.Button(ventana, text=texto, width=40, height=2, command=salir)

    boton.pack(pady=3) 
    i += 1

ventana.mainloop()
