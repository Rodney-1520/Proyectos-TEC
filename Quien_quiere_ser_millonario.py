import os
from datetime import datetime
import random

#Largo texto
#E:Recibe un texto
#S:Retorna el largo de ese texto
#R:Si el texto ese vacio retorna error
def largoTexto(txt):
    resultado = 0
    if txt == "":
        return("Error: el texto no puede estar vacío.")
    while txt != "":
        resultado += 1
        txt = txt[1:]

    return resultado
#Crear indice
#E:Recibe un documento txt
#S:Retornar el documento pero con un  indice
#R:
def crearIndice():
    try:
        archivo = open("IndiceJuegos.txt", "r", encoding="utf-8")
        lineas = archivo.readlines()
        archivo.close()
        return largoLista(lineas) + 1
    except FileNotFoundError:
        archivo = open("IndiceJuegos.txt", "w", encoding="utf-8")
        archivo.close()
        return 
    
#Crear nuevo juego
#E:
#S:se va a crear un archivo txt que contiene 15 preguntas dela rchivo Preguntas.txt y en el va a contor los montos a ganar si se responde correctamente
#R:El programa solo sirve si se activa manualmente
def crearNuevoJuego():
    archivo = open("Preguntas.txt", "r", encoding="utf-8")
    todas_preguntas = archivo.readlines()
    archivo.close()

    preguntas_seleccionadas = random.sample(todas_preguntas, 15)
    premios=[100, 200, 300, 400, 500, 1000, 2000, 2500, 4000, 5000, 7000, 8500, 9500, 12000, 15000]

    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d")
    hora = ahora.strftime("%H:%M:%S")
    
    numero_juego = crearIndice()
    nombre_archivo = f"ListaPreguntas{numero_juego}.txt"

    archivo= open(nombre_archivo, "w", encoding="utf-8")
    archivo.write(f"{numero_juego},{fecha},{hora}\n")
    i=0
    for pregunta in preguntas_seleccionadas:
        premio=premios[i]
        archivo.write(f"{premio},{pregunta.strip()}\n")
        i=i+1
    archivo.close()

    archivo = open("IndiceJuegos.txt", "a", encoding="utf-8")
    archivo.write(nombre_archivo + "\n")
    archivo.close()

    print(f"Juego creado: {nombre_archivo}")

#Crear juego menu
#E:En esta funcion se va almacenar la funcion de crear juego 
#S:Se va a imprimir un menu para que sea mas bonito de ver
#R:Si no se ingresa un valor valido retornara un error
def crearJuegoMenu():
    while True:
        print("Menu Principal")
        print("\n")
        print("1. Crear nuevo juego")
        print("\n")
        print("2. Salir")
        print("\n")

        opcion = int(input("Seleccione una opcion:"))
        if opcion == 1:
            crearNuevoJuego()
        elif opcion == 2:
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
            
#Buscar en texto
#E:Un texto y un texto a buscar y utilizara la funcion auxiliar de buscarEntexto_Aux
#S:Retorna el texto buscado
#R:Si el texto es vacio retornar un error
def buscarEnTexto(texto, textoABuscar):
    if isinstance(texto, str) and isinstance(textoABuscar, str):
        if (texto != "") and (textoABuscar != ""):
            return buscarEnTexto_Aux(texto, textoABuscar)
        else:
            return "Error: La variable de texto y textoABuscar no deben de estar vacios"
    else:
        return "Error: El tipo de parametro no es texto"

#Buscar en texto Aux
#E:Un texto ingresado en la funcion principal de buscar en texto
#S:Retornara el texto solicitado
#R:Si el texto es vacio retornara u error
def buscarEnTexto_Aux(texto, textoABuscar):
    resultado = False
    largo = largoTexto(textoABuscar)

    if textoABuscar == "":
        return "Error: el texto no puede estar vacío."

    while texto != "":
        textoCorte = texto[0:largo]

        if textoABuscar == textoCorte:
            resultado = True
            break
        else:
            texto = texto[1:]

    return resultado

#Buscar en arhivo 
#E:Un archivo de texto
#S:Retornara True usuario y la clave son correctos y False si son incorrectos 
#R:
def buscarEnTexto_AuxV2(linea, textoABuscar):
    largo_linea = largoTexto(linea)
    largo_buscar = largoTexto(textoABuscar)

    if largo_buscar == "Error: el texto no puede estar vacío.":
        return False

    for i in range(largo_linea - largo_buscar + 1):
        coincidencia = True
        for j in range(largo_buscar):
            if linea[i + j] != textoABuscar[j]:
                coincidencia = False
        if coincidencia:
            return True
    return False

def buscarEnArchivo(nombreArchivo, textoABuscar):
    if not isinstance(nombreArchivo, str) or nombreArchivo.strip() == "":
        return "Error: El nombre del archivo no debe estar vacío"
    if not isinstance(textoABuscar, str) or textoABuscar.strip() == "":
        return "Error: El texto a buscar no debe estar vacío"

    try:
        archivo = open(nombreArchivo, "r")
        for linea in archivo:
            if buscarEnTexto_AuxV2(linea, textoABuscar):
                archivo.close()
                return linea.strip()
        archivo.close()
        return "No se encontró el texto en el archivo"
    except:
        return "Error: El archivo no existe"
    
#Inciar sesion
#E:Usuario y clave
#S:Abre el menu administrativo si el usuario y clave son correctos
#R:Si el usuario o la clave son incoorrectos retornar "Usuario o contraseña incorrectos"
def iniciarSesion():
    print("\n")
    usuario = input("Ingrese su nombre de usuario: ")
    print("\n")
    clave = input("Ingrese su clave: ")
    datosIngresados = usuario + ";" + clave

    resultado = buscarEnArchivo("Acceso.txt", datosIngresados)

    if resultado == datosIngresados:
        print("\n")
        print("Inicio de sesión exitoso")
        print("\n")
        print("Bienvenido al Menu Administrativo")
        print("\n")
        menuAdministrativo()
        return True
    else:
        print("Usuario o contraseña incorrectos")
        return False

#Ver historial 
#E:En esta funcion se alamcena todo lo relacionado con el almacenamiento de los datos de los juegos y posee la capacidad de mostrarla y buscar informacion relacionada a las estadisticas del juego
#S:Retornara la informaciopn seleccionada por el usuario
#R:Si no se ingresa una opcion valida o el archivo necesario retornara un error
def verHistorial():
    if os.path.exists("historial.txt"):
        with open("historial.txt", "r", encoding="utf-8") as archivo_historial:
            contenido = archivo_historial.readlines()

            if contenido:
                while True:
                    print("\n--- Historial de Juegos ---\n")
                    print("\n")
                    print("0. Salir")
                    print("\n")
                    print("1. Ver todo el historial")
                    print("\n")
                    print("2. Buscar por nombre de jugador")
                    print("\n")
                    print("3. Buscar por premio ganado")
                    print("\n")
                    print("4. Buscar por fecha")
                    print("\n")
                    
                    opcion = int(input("Seleccione una opcion:"))

                    if opcion == 0:
                        break

                    elif opcion == 1:
                        contador = 1
                        for linea in contenido:
                            print(f"Juego #{contador}: {linea.strip()}")
                            contador += 1
                            

                    elif opcion == 2:
                        nombre_buscar = input("\nIngrese el nombre del jugador que desea buscar: ").strip().lower()
                        encontrados = False
                        contador = 1
                        for linea in contenido:
                            if nombre_buscar in linea.lower():
                                print(f"Juego #{contador}: {linea.strip()}")
                                encontrados = True
                            contador += 1
                        if not encontrados:
                            print("\nNo se encontraron juegos para ese nombre.\n")
                        

                    elif opcion == 3:
                        premio_buscar = input("\nIngrese el monto de premio que desea buscar (solo el número, sin 'colones'): ").strip()
                        encontrados = False
                        contador = 1
                        for linea in contenido:
                            if premio_buscar in linea:
                                print(f"Juego #{contador}: {linea.strip()}")
                                encontrados = True
                            contador += 1
                        if not encontrados:
                            print("\nNo se encontraron juegos con ese monto de premio.\n")
                        

                    elif opcion == 4:
                        fecha_buscar = input("\nIngrese la fecha que desea buscar (formato AAAA-MM-DD): ").strip()
                        encontrados = False
                        contador = 1
                        for linea in contenido:
                            if fecha_buscar in linea:
                                print(f"Juego #{contador}: {linea.strip()}")
                                encontrados = True
                            contador += 1
                        
                        if not encontrados:
                            print("\nNo se encontraron juegos con esa fecha.\n")

                    else:
                        print("\nOpción no válida. Por favor selecciona 0, 1, 2, 3 o 4.\n")
            else:
                print("\nNo hay juegos registrados en el historial aún.\n")
    else:
        print("\nEl archivo historial.txt no existe.\n")

#Encontrar maximo
#E:Una lista de numeros
#S:retornara el numero mayor
#R:
def encontrarMaximo(lista):
    if not lista:
        return None
    maximo = lista[0]
    for elemento in lista:
        if elemento > maximo:
            maximo = elemento
    return maximo

#Encontrar minimo diferente de cero
#E:Una lista
#S:retornara el numero minimo diferente de cero
#R:
def encontrarMinimoDifCero(lista):
    minimo = None
    for elemento in lista:
        if elemento > 0:
            if minimo is None or elemento < minimo:
                minimo = elemento
    return 

#Estadisticas de juegos
#E:Esta funcion va alamacenar estadisticas mas concretas sobre los juegos realizados por el jugador 
#S:retornara el numero de cosas que indique el nombre de la estadistica
#R:retornara un error si no se ingresa un valor valido o el archuvo no existe
def estadisticasJuegos():
    if os.path.exists("historial.txt"):
        with open("historial.txt", "r", encoding="utf-8") as archivo_historial:
            contenido = archivo_historial.readlines()

            if contenido:
                while True:
                    print("\n--- Estadísticas de Juegos ---\n")
                    print("\n")
                    print("(1) Total de juegos")
                    print("\n")
                    print("(2) Total de juegos ganados")
                    print("\n")
                    print("(3) Total de juegos perdidos")
                    print("\n")
                    print("(4) Suma de premios entregados")
                    print("\n")
                    print("(5) Monto máximo obtenido como premio")
                    print("\n")
                    print("(6) Monto mínimo obtenido como premio diferente a CERO")
                    print("\n")
                    print("(7) Retornar")
                    print("\n")
                    
                    opcion = int(input("Seleccione una opcion:"))

                    if opcion == "7":
                        break

                    premios = []
                    for linea in contenido:
                        partes = linea.strip().split(",")
                        for parte in partes:
                            if "colones" in parte:
                                monto = int(parte.strip().split()[0])
                                premios += [monto]  

                    if opcion == 1:
                        print(f"\nTotal de juegos: {largoLista(contenido)}\n")
                        

                    elif opcion == 2:
                        ganados = 0
                        for premio in premios:
                            if premio > 0:
                                ganados += 1
                        print(f"\nTotal de juegos ganados: {ganados}\n")
                        

                    elif opcion == 3:
                        perdidos = 0
                        for premio in premios:
                            if premio == 0:
                                perdidos += 1
                        print(f"\nTotal de juegos perdidos: {perdidos}\n")
                        

                    elif opcion == 4:
                        suma_premios = 0
                        for premio in premios:
                            suma_premios += premio
                        print(f"\nSuma de premios entregados: {suma_premios} colones\n")
                        

                    elif opcion == 5:
                        if premios:
                            max_premio = encontrarMaximo(premios)
                            print(f"\nMonto máximo obtenido como premio: {max_premio} colones\n")
                            
                        else:
                            print("\nNo hay premios registrados.\n")

                    elif opcion == 6:
                        min_premio = encontrarMinimoDifDeCero(premios)
                        if min_premio is not None:
                            print(f"\nMonto mínimo obtenido como premio diferente a CERO: {min_premio} colones\n")
                            
                        else:
                            print("\nNo hay premios diferentes a cero registrados.\n")

                    else:
                        print("\nOpción no válida. Por favor selecciona un número entre 1 y 7.\n")

            else:
                print("\nNo hay juegos registrados en el historial aún.\n")
    else:
        print("\nEl archivo historial.txt no existe.\n")
        
#Menu Administrativo
#E:La funcion va almacenar las funciones administrativas
#S:Retornara la opcion de escojer una de las funciones administrativas 
#R:Si no se ingresa algunas de las opciones del menu retornara un error
def menuAdministrativo():
    while True:
        print("--Menu Administrativo--")
        print("\n")
        print("(1).Gestion de Preguntas y Respuestas")
        print("\n")
        print("(2).Gestion de Juegos")
        print("\n")
        print("(3).Historial de Juegos")
        print("\n")
        print("(4).Estadisticas de Juegos")
        print("\n")
        print("(5).Retornar")
        print("\n")
        try:
            opcion = int(input("Seleccione una opcion:"))
            
            if opcion == 1:
                GestionDePreguntasyRespuestasMenu()
                print("\n")
                
            elif opcion == 2:
                  crearJuegoMenu()   
                  print("\n")
                  
            elif opcion == 3:
                  verHistorial()
                  print("\n")
                  
            elif opcion == 4:
                  estadisticasJuegos()
                  print("\n")
                  
            elif opcion == 5:
                  print("\n")
                  print("Saliendo del programa...")
                  break
            else:
                  print("Opcion invalida")
        except:
              print("Error")
              
#Ver preguntas y respuestas
#E:El archivo de texto que contine las preguntas y repsuestas
#S:Mostrara las preguntas y respuestas que contiene el archivo
#R:Solo se mostrara las preguntas y respuestas que contiene el archivo
def verPreguntasyRespuestas(nombreArchivo):
    if(isinstance(nombreArchivo, str)):
        if(nombreArchivo != ""):
            archivo = open('Preguntas.txt', 'r', encoding='utf-8')
            contenido = archivo.read()
            print(contenido)
            archivo.close()
        else:
            return "Error: El nombre del archivo no debe de estar vacio"
    else:
        return "Error: El tipo de parametro no es texto"
   
# Pregunta Existe
#E:Numero de pregunta
#S:Retorna True si la pregunta existe o False o existe
#R:
def preguntaExiste(num):
        archivo = open("Preguntas.txt",  "r",encoding="utf-8")
        preguntas = archivo.readlines()
        archivo.close()
        for pregunta in preguntas:
            pregunta = pregunta.strip().split(",")
            if int(pregunta[0]) == num:
                return pregunta
            
#Largo Lista version 2
#E:un archivo txt
#S:va retornar un contador de cuantas preguntas existen
#R:
def largoListaV2():
    archivo = open("Preguntas.txt",  "r",encoding="utf-8")
    preguntas = archivo.readlines()
    archivo.close()
    cantidad = 0
    for pregunta in preguntas:
        cantidad += 1
    return cantidad

#Modificar pregunta menu
#E:esta funcion va a ser el menu de la modificacion de preguntas
#S:Va imprimir un menu para la modificacion de preguntas
#R:
def modificarPreguntaMenu():  
     print("\n")
     print("(1).Nueva pregunta")
     print("\n")
     print("(2).Nueva respuesta1")
     print("\n")
     print("(3).Nueva respuesta2")
     print("\n")
     print("(4).Nueva respuesta3")
     print("\n")
     print("(5).Nueva respuesta correcta")
     print("\n")   
     print("(6).Salir")
     print("\n")
    
# Modificar pregunta
# E:El contenido de a cambiar en la pregunta indicada
# S:Mostrar si la pregunta modifico correctamente
# R:
def modificarPregunta():
    archivo = open("Preguntas.txt",  "r",encoding="utf-8")
    preguntas = archivo.readlines()
    archivo.close()
    
    while True:
        try:
            num = int(input("Ingrese el numero de pregunta que desa modificar: "))
        except ValueError:
            print("Error: Valor no valido")
            return
        
        if num <= 0 or num > largoListaV2():
            print("Error: Numero de pregunta invalido")
            return
        pregunta = preguntaExiste(num)
        print(f"Pregunta encontrada: {pregunta}")
        
        modificarPreguntaMenu()
        
        try:
            opcion = int(input("Escoja la opcion a modificar: "))
        except ValueError:
            print("Error: Valor no valido")
            return
        if opcion == 1:
            nuevaPregunta = str(input("Ingrese la nueva pregunta: "))
            pregunta [1] = nuevaPregunta
        elif opcion == 2:
            nuevaRespuesta1 = str(input("Ingrese la nueva respuesta1: "))
            pregunta[2] = nuevaRespuesta1
        elif opcion == 3:
            nuevaRespuesta2 =  str(input("Ingrese la nueva respuesta2: "))
            pregunta[3] = nuevaRespuesta2
        elif opcion == 4:
            nuevaRespuesta3 =  str(input("Ingrese la nueva respuesta3: "))
            pregunta[4] = nuevaRespuesta3
        elif opcion == 5:
            nuevaCorrecta = str(input("Ingrse la nueva respuesta correcta: "))
            pregunta[5] = nuevaCorrecta
        elif opcion == 6:
            return
        else:
            print("Opcion no valida")
            return
        
        pregunta_modificada = f"{pregunta[0]},{pregunta[1]},{pregunta[2]},{pregunta[3]},{pregunta[4]},{pregunta[5]}\n"
        preguntas[num - 1] = pregunta_modificada
        archivo = open("Preguntas.txt",  "w",encoding="utf-8")
        for pregunta in preguntas:
            archivo.write(pregunta)
        archivo.close()
        print("Pregunta modificada con exito")
        
        continuar = input("¿Desea modificar otra pregunta? (s/n): ").lower()
        if continuar != 's':
            print("Saliendo del menú de modificación.")
            break
        
#Pregunta ya existe
#E:una nueva pregunta que se quiere agregar
#S:verificar si es pregunta ya existe 
#R:
def preguntaYaExiste(pregunta_nueva):
    archivo = open("Preguntas.txt", "r", encoding="utf-8")
    for linea in archivo:
        partes = linea.strip().split(",")
        indice = 0
        for elemento in partes:
            if indice == 1:
                if elemento.strip().lower() == pregunta_nueva.strip().lower():
                    archivo.close()
                    return True
            indice += 1
    archivo.close()
    return False

#Agregar pregunta
#E:Nueva pregunta y respuestas
#S:La nueva pregunta agregada correctamente
#R:No puede haber 2 preguntas iguales
def agregarPregunta():
    numero = input("Número de la pregunta: ")
    pregunta = input("Escribe la pregunta: ")
    if preguntaYaExiste(pregunta):
        print("Esa pregunta ya existe en el archivo.")
        return
    opcion1 = input("Opción 1: ")
    opcion2 = input("Opción 2: ")
    opcion3 = input("Opción 3: ")
    respuesta_correcta = input("Respuesta correcta: ")
    linea = f"{numero},{pregunta},{opcion1},{opcion2},{opcion3},{respuesta_correcta}\n"
    archivo = open("Preguntas.txt", "a", encoding="utf-8")
    archivo.write(linea)
    archivo.close()

#Largo lista
#E:Una lista
#S:Cuenta cuantos x cosas hay en una lista
#R:
def largoLista(lista):
    cantidad = 0
    for x in lista:
        cantidad += 1
    return cantidad

#Pregunta ya existe v2
#E:una pregunta
#S:Va a verificar si la pregunta esta en el archivo
#R:
def preguntaYaExisteV2(valorBuscado, modo):
    archivo = open("Preguntas.txt", "r", encoding="utf-8")
    for linea in archivo:
        partes = linea.strip().split(",", 1)

        if largoLista(partes) < 2:
            continue

        numero = partes[0].strip()
        texto = partes[1].strip()

        if modo == "texto" and texto.lower() == valorBuscado.strip().lower():
            archivo.close()
            return True
        elif modo == "numero" and numero == valorBuscado.strip():
            archivo.close()
            return True
    archivo.close()
    return False

#Eliminar Pregunta
#E:se va ingresar el numero de pregunta que se quiere eliminar
#S:se va a retornar un mensaje de que se elimino la pregunta correctamente
#R:la pregunta debe de existir
def eliminarPregunta():
    numeroAEliminar = input("Escribe el número de la pregunta que deseas eliminar: ").strip()

    if not preguntaYaExisteV2(numeroAEliminar, "numero"):
        print("Ese número de pregunta no existe.")
        return

    archivo = open("Preguntas.txt", "r", encoding="utf-8")
    nuevas_preguntas = []

    for linea in archivo:
        partes = linea.strip().split(",", 1)

        if largoLista(partes) < 2:
            continue

        numero = partes[0].strip()
        pregunta = partes[1].strip()

        if numero != numeroAEliminar:
            nuevas_preguntas += [pregunta]
    archivo.close()

    archivo = open("Preguntas.txt", "w", encoding="utf-8")
    contador = 1
    for pregunta in nuevas_preguntas:
        archivo.write(str(contador) + "," + pregunta + "\n")
        contador += 1
    archivo.close()

    print("Pregunta eliminada y archivo reenumerado correctamente.")

#Gestion de Preguntas y Respuestas
#E:La funcion va almacenar distintas opciones como ver las preguntas ,modificarlas eliminarlas,ect
#S:Se abrira el menu de la opcion seleccionada
#R:sin no se ingresa algunas de las opciones del menu retornara un error
def GestionDePreguntasyRespuestasMenu():
    while True:
        print("\n")
        print("(1).Ver preguntas y respuestas")
        print("\n")
        print("(2).Modificar preguntas y respuestas")
        print("\n")
        print("(3).Añadir preguntas y respuestas")
        print("\n")
        print("(4).Eliminar preguntas")
        print("\n")
        print("(5).Salir")
        print("\n")
        try:
            opcion = int(input("Seleccione una opcion:"))
            
            if opcion == 1:
                verPreguntasyRespuestas("Preguntas.txt")
                print("\n")
                
            elif opcion == 2:
                modificarPregunta()
                print("\n")
            elif opcion == 3:
                agregarPregunta()
                print("\n")
                  
            elif opcion == 4:
                eliminarPregunta()
                print("\n")
                  
            elif opcion == 5:
                print("\n")
                print("Saliendo del programa...")
                break
            else:
                print("Opcion invalida")
        except:
            print("Error")
            
#Es digito
#E:Una cadena de digitos
#S:retornara true si los digitos de la cadena esta entre 0 y 9
#R:
def esDigito(cadena):
    for digito in cadena:
        if digito < '0' or digito > '9':
            return False
    return True

#Validar cedula
#E:una cadena de numeros de 9 digitos
#S:retornara true si la cantidad total de digitos es = 9
#R:
def validarCedula(cedula):
    if largoLista(cedula) != 9:  
        return False
    if cedula[0] == '0':  
        return False
    if not esDigito(cedula):
        return False
    return True

#Datos de jugador
#E:Los datos personales del jugador como el nombre numero de cedula y sexo
#S:si los datos estan son bien ingresados se guardaran en el archivo .txt de historial y se empezara a ejeuctar la funcion de juego
#R:Si no se ingresa bien los datos retornara un error
def datosJugador():
    archivos = ["historial.txt", "Juegos.txt"]

    for archivo_nombre in archivos:
        if os.path.exists(archivo_nombre):
            continue  
        with open(archivo_nombre, "w", encoding="utf-8") as archivo:
            print(f"Archivo {archivo_nombre} creado.")

    while True:
        print("\n ---- Iniciar sesion ----\n")

        while True:
            jugadorCedula = str(input("Ingrese su número de cédula: "))
            if validarCedula(jugadorCedula):
                break
            else:
                print("\n--- Error: Cédula inválida, debe tener 9 dígitos y no comenzar con cero ---\n")

        while True:
            jugador_Nombre = input("Ingrese su nombre completo: ").strip()
            if jugador_Nombre == "":
                print("\nError: El nombre no puede estar vacío\n")
            elif esDigito(jugador_Nombre):
                print("\nError: El nombre no puede ser solo números\n")
            else:
                break

        while True:
            jugador_Sexo = str(input("Ingrese su sexo (Hombre o Mujer): "))
            if jugador_Sexo == "Hombre" or jugador_Sexo == "Mujer":
                break
            else:
                print("\n-- Error: Sexo inválido --\n")

        while True:
            pregunta = input("¿Desea Iniciar el Juego? (s/n): ").strip().lower()  
            if pregunta == "s":
                fechaI = datetime.now()
                formatoFechaI = fechaI.strftime("%Y-%m-%d")
                formatoHoraI = fechaI.strftime("%H:%M:%S")

                with open("historial.txt", "a", encoding="utf-8") as archivo_historial:
                    archivo_historial.write(f"{jugadorCedula},{jugador_Nombre},{jugador_Sexo},{formatoFechaI} {formatoHoraI},,," + "\n")
                
                print("\nDatos guardados en el historial. ¡Vamos a empezar el juego!\n")
                
                juego_continuar = jugar()
                if not juego_continuar:
                    return  

            elif pregunta == "n":
                print("\nJuego finalizado. No se guardaron los datos ingresados\n")
                return
            else:
                print("\n--- Error: Opción inválida, intente de nuevo ---\n")

#Jugar
#E:En esta funcion se empezara a ejuctar despues de que los datos del jugador se hayan ingresado correctamente y imprimira el juego propiamente el juego como tal de quien quiere ser millonario
#S:retornara los resultados del jugador durante la partida y las estadisticas y datos se guardaran correspondientemente en el archivo indicado
#R:Si no se ingresa las opciones indicadas retornara un error
def jugar():
    preguntas_correctas = 0 
    while True:
        print("\n--- Iniciando  juego ---\n")
        
        zonas_seguras = [500, 5000, 15000]
        zona_segura = 0
        premio_ganado = 0

        archivos_preguntas = [f for f in os.listdir() if f.startswith("ListaPreguntas") and f.endswith(".txt")]

        if not archivos_preguntas:
            print("\nNo hay archivos de preguntas disponibles. Crea primero archivos como 'ListaPreguntas01.txt'.\n")
            return

        archivo_seleccionado = random.choice(archivos_preguntas)
        print(f"\nArchivo seleccionado: {archivo_seleccionado}\n")

        with open(archivo_seleccionado, "r", encoding="utf-8") as archivo:
            preguntas = archivo.readlines()

        preguntas = preguntas[1:]  # Ignorar encabezado

        for linea in preguntas:
            partes = linea.strip().split(',')
            
            if largoLista(partes) < 7:
                print("\nError en el formato de la pregunta.\n")
                continue
            
            premio, _, pregunta, opA, opB, opC, opD = partes[:7]

            opciones = [opA, opB, opC, opD]
            respuesta_correcta = opD
            random.shuffle(opciones)

            if zona_segura == 0:
                premio_ganado = 0

            print(f"\nPregunta: {pregunta}")
            print(f"Premio: {premio} colones")
            print(f"A) {opciones[0]}")
            print(f"B) {opciones[1]}")
            print(f"C) {opciones[2]}")
            print(f"D) {opciones[3]}")

            respuesta = input("\nSelecciona una opción (A, B, C o D): ").strip().lower()

            if respuesta == "a":
                if opciones[0] == respuesta_correcta:
                    print("\n✅ ¡Respuesta correcta!\n")
                    preguntas_correctas += 1
                    if zona_segura == 2:
                        print(f"\n🎉 ¡Has completado el juego y has ganado {premio} colones.")
                        premio_ganado = int(premio)
                        break
                    premio_ganado += int(premio)
                else:
                    if zona_segura > 0:
                        premio_ganado = zonas_seguras[zona_segura - 1]
                    print(f"\n❌ Respuesta incorrecta. Premio ganado: {premio_ganado} colones.\n")
                    break
            elif respuesta == "b":
                if opciones[1] == respuesta_correcta:
                    print("\n✅ ¡Respuesta correcta!\n")
                    preguntas_correctas += 1
                    if zona_segura == 2:
                        print(f"\n🎉 ¡Has completado el juego y has ganado {premio} colones.")
                        premio_ganado = int(premio)
                        break
                    premio_ganado += int(premio)
                else:
                    if zona_segura > 0:
                        premio_ganado = zonas_seguras[zona_segura - 1]
                    print(f"\n❌ Respuesta incorrecta. Premio ganado: {premio_ganado} colones.\n")
                    break
            elif respuesta == "c":
                if opciones[2] == respuesta_correcta:
                    print("\n✅ ¡Respuesta correcta!\n")
                    preguntas_correctas += 1
                    if zona_segura == 2:
                        print(f"\n🎉 ¡Has completado el juego y has ganado {premio} colones.")
                        premio_ganado = int(premio)
                        break
                    premio_ganado += int(premio)
                else:
                    if zona_segura > 0:
                        premio_ganado = zonas_seguras[zona_segura - 1]
                    print(f"\n❌ Respuesta incorrecta. Premio ganado: {premio_ganado} colones.\n")
                    break
            elif respuesta == "d":
                if opciones[3] == respuesta_correcta:
                    print("\n✅ ¡Respuesta correcta!\n")
                    preguntas_correctas += 1
                    if zona_segura == 2:
                        print(f"\n🎉 ¡Has completado el juego y has ganado {premio} colones.")
                        premio_ganado = int(premio)
                        break
                    premio_ganado += int(premio)
                else:
                    if zona_segura > 0:
                        premio_ganado = zonas_seguras[zona_segura - 1]
                    print(f"\n❌ Respuesta incorrecta. Premio ganado: {premio_ganado} colones.\n")
                    break
            else:
                print("\n❌ Opción inválida.\n")
                continue

            print("\n--- Siguiente pregunta ---\n")

            if int(premio) == zonas_seguras[zona_segura]:
                print(f"\n🎉 ¡Zona segura alcanzada! {zonas_seguras[zona_segura]} colones asegurados.")
                if zona_segura < 2:
                    respuesta_retirarse = input(f"\n¿Quieres retirarte con {zonas_seguras[zona_segura]} colones? (s/n): ").strip().lower()
                    if respuesta_retirarse == "s":
                        print(f"\n¡Has decidido retirarte! Premio ganado: {zonas_seguras[zona_segura]} colones.")
                        premio_ganado = zonas_seguras[zona_segura]
                        break
                zona_segura += 1

            if zona_segura > 0:
                jugar_nuevamente = input("\n¿Quieres continuar con el juego? (s/n): ").strip().lower()
                if jugar_nuevamente != "s":
                    print(f"\n¡Has decidido retirarte! Premio ganado: {premio_ganado} colones.")
                    break

        print(f"\n--- Fin del juego. Premio ganado: {premio_ganado} colones ---\n")
        print(f"Total de preguntas correctas: {preguntas_correctas}\n")

        with open("historial.txt", "r", encoding="utf-8") as historial:
            lineas = historial.readlines()

        if lineas:
            ultima_linea = lineas[-1].strip()
            fecha_hora_final = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nueva_linea = f"{ultima_linea},{fecha_hora_final},{premio_ganado} colones,{preguntas_correctas} preguntas correctas,{archivo_seleccionado}\n"
            lineas[-1] = nueva_linea

        with open("historial.txt", "w", encoding="utf-8") as historial:
            historial.writelines(lineas)

        print("\n¡Gracias por jugar! Hasta pronto.\n")
        return False  

#Opciones de jugador menu
#E:La funcion va almacenar otras funciones para que se puedan llevar a cabo las opciones de jugador
#S:Va a retornar lo que realizan las otras funciones
#R:si no se ingresa algunas de las opciones del menu retornara un error
def menuOpcionesJugador():
    while True:
         print ("\n")
         print ("1.Jugar")
         print ("\n")
         print("2.Retornar")
         print ("\n")
         try:
            opcion = int(input("Seleccione una opcion:"))
            
            if opcion == 1:
                datosJugador()
                print("\n")
            elif opcion == 2:
                print("\n")
                print("Saliendo del programa...")
                break
            else:
                print("Opcion invalida")
         except:
            print("Error")
                                   
#Menu Principal
#E: La funcion va a almacenar otras funciones para que funcione el programa
#S: Va a retornar lo que realizan las otras funciones si se seleccion la opcion correspondiente
#R: si no se ingresa algunas de las opciones del menu retornara un error
def menuPrincipal():
     while True:
          print ("\n")
          print ("---Menu Principal---")
          print ("\n")
          print("A. Opciones Administrativas")
          print ("\n")
          print("J. Opciones de Jugador")
          print ("\n")
          print("S. Salir.")
          print ("\n")
          try:
               opcion = str(input("Selecciona una opcion: ")).upper()
          
               if opcion == "A":
                    iniciarSesion()
                    print("\n")
          
               elif opcion == "J":
                    menuOpcionesJugador()
                    print("\n")
               
               elif opcion == "S":
                    print("Saliendo del programa...")
                    break
               
               else:
                    print("Opción inválida.")

          except:
               print("Error")

menuPrincipal()




          

          



          

          


          

          
