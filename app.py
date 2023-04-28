from tkinter import *
from tkinter import filedialog

#Definamos la ruta del archivo para poder ser vista por otras funciones
ruta_archivo = ''

# Creamos la content principal
ventana = Tk()
#titulo de la content
ventana.title('ADA II')
# Modificamos en tamaño de la content 
ventana.geometry('600x400')
# Crear un marco dentro de la content principal
frame = Frame(ventana)
frame.pack(fill=BOTH, expand=True)

# Agregar un widget de barra de desplazamiento al marco
scrollbar = Scrollbar(frame, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

# Agregar el widget de contenido a la content principal
canvas = Canvas(frame, yscrollcommand=scrollbar.set)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

# Conectar el widget de contenido al widget de la barra de desplazamiento
scrollbar.config(command=canvas.yview)
# Añadir contenido al canvas
content = Frame(canvas)
canvas.create_window((300, 70), window=content, anchor=CENTER)


# Función para abrir un archivo de texto (.sub o .psub)
def abrir_archivo():
    
    global trio, imprimir_oferentes, oferentes_gob
    global ruta_archivo
    # Definimos los tipos de archivo permitidos
    tipos_archivo = [('Archivos de psubasta', '*.sub'),('Archivos de subasta', '*.sub') ]
    # Abrimos el diálogo para seleccionar el archivo
    ruta_archivo = filedialog.askopenfilename(defaultextension='.sub', filetypes=tipos_archivo )
    
    # Verificamos si se seleccionó un archivo
    if ruta_archivo != '':
        
        # Abrimos el archivo y lo imprimimos en la consola
        with open(ruta_archivo, 'r') as archivo:
                   
            #Obtenemos la informacion de: A - Acciones B - Precio C - numero de oferentes
             contador_oferentes=1
             #indice para cargar los datos de los oferentes en una lista
             indice_oferentes=0
             A = archivo.readline()
             B = archivo.readline()
             n = archivo.readline()
            #Imprimimos en la interfaz el trio de datos
            
             trio = Label(content, text="Acciones:"+ A +"Precio: "+ B + "Oferentes: " + n )
             trio.pack()

             

            #Imprimiendo los oferentes
            #Imprimir lineas en pantalla 
             lineas = archivo.read().split('\n')
             oferentes_aux = []
             for linea in lineas[:-1]:
                 if(contador_oferentes != len(lineas)-1):
                    oferentes_aux.append("\n Oferente("+ str(contador_oferentes)+")" +"-->" + "Oferta" +"("+''.join(linea)+") ")
                    oferentes = ''.join(oferentes_aux)
                    contador_oferentes+=1
                    indice_oferentes+=1
                 else:
                     oferentes_gob = Label(content, text="Gobierno: "+"-->" + "Oferta" +"("+''.join(linea)+")")
                     oferentes_gob.pack()

             imprimir_oferentes = Label(content, text=oferentes)
             imprimir_oferentes.pack()

# Función para limpiar pantalla
def limpiar_pantalla():
    trio.destroy()
    imprimir_oferentes.destroy()
    oferentes_gob.destroy()
    if "venta_acciones" in globals():
        venta_acciones.destroy()
        venta_acciones_gob.destroy()
        ganancia_gob.destroy()
    else:(print("No existe aún"))

    if "venta_acciones_gob_pv" in globals():
    #venta_acciones_pv.destroy()
        venta_acciones_gob_pv.destroy()
        ganancia_gob_pv.destroy()
    else:(print("No existe aún pv"))

# Funcion de fuerza bruta
def accionesFB():
    global venta_acciones, venta_acciones_gob, ganancia_gob
    
    oferente = []
    contador_oferentes=0
    ganancia_gobierno_fb=0
    # Verificamos si se seleccionó un archivo
    if ruta_archivo != '':
        # Abrimos el archivo y lo imprimimos en la consola
        with open(ruta_archivo, 'r') as archivo:
             lineas = archivo.readlines()
             #Obtenemos la informacion de: A - Acciones B - Precio C - numero de oferentes
             A = int(lineas[0])
             B = int(lineas[1])
             n = int(lineas[2])
             #print(lineas)
             #Iniciamos la lista en el tamaño de oferentes 
             oferentes = [None] * len(lineas[3:-1])
             for linea in lineas[3:-1]:
                #valores contiene cada oferentes p,r,c - NO INCLUYE GOBIERNO
                valores = linea.split(',')
                #Valores de los oferentes
                #p=oferta del oferente
                #r=maximo de acciones que compra
                #c=minimo de acciones que compra
                #respectivamente
                oferente.append(int(valores[0]))
                oferente.append(int(valores[1]))
                oferente.append(int(valores[2]))
                #print(len(lineas[3:]))
                #cargamos la lista oferentes con todos los oferentes
                #ecordando que por ultimo esta el gobierno y las acciones 
                #no vendiadaas seran vendidas al gobierno
                if(contador_oferentes != len(lineas[3:])-1):
                    oferentes[contador_oferentes] = oferente
                    oferente = []
                    contador_oferentes+=1

             #Ordenamos la lista de oferentes lexicograficamente
             oferentes_lexicografico = sorted(oferentes,key=lambda x: x) 
             
             #contdor de cantidad de oferentes para poder saber a que oferentes se le vendio
             contador_venta_of=0
             #contamos las acciones disponibles durante la ejecucion
             acciones_disponibles=A
             #guardamos la ganancia del gobierno por cada venta
             ventas_aux=[]
             for mejor_oferente in reversed(oferentes_lexicografico):
                contador_venta_of+=1

                #Vendemos al primero de la lista y reducimos las accion que se vendieron 
                if(acciones_disponibles != 0 and mejor_oferente[1] <= acciones_disponibles and mejor_oferente[1] != 0):
                    #print(acciones_disponibles)
                    acciones_disponibles = acciones_disponibles - mejor_oferente[1]
                    ganancia_gobierno_fb += mejor_oferente[0] * mejor_oferente[1]
                    ventas_aux.append("\nSe vendieron: "+ str(mejor_oferente[1]) + " acciones" + " al oferente: (" + str(contador_venta_of) +") a un precio de: "+ str(mejor_oferente[0]))
                    #venta_acciones = Label(content, text="Se vendieron: "+ str(mejor_oferente[1]) + " acciones" + " al oferente: (" + str(contador_venta_of) +") a un precio de: "+ str(mejor_oferente[0]))
                    #venta_acciones.pack()

             ventas = ''.join(ventas_aux)
             venta_acciones = Label(content, text=ventas)
             venta_acciones.pack()   

             if(acciones_disponibles != 0):
                 ganancia_gobierno_fb+=acciones_disponibles*B
                 venta_acciones_gob = Label(content, text="Se vendieron: "+ str(acciones_disponibles) + " acciones" + " al GOBIERNO a un precio de: "+ str(B))
                 venta_acciones_gob.pack()
    
    
    ganancia_gob = Label(content, text="Las ganancias del gobierno fueron: "+ str(ganancia_gobierno_fb))
    ganancia_gob.pack()              

# Función Programación Voráz
def accionesV():
    global venta_acciones_pv, venta_acciones_gob_pv, ganancia_gob_pv
    oferente = []
    contador_oferentes=0
    ganancia_gobierno_fb=0
    # Verificamos si se seleccionó un archivo
    if ruta_archivo != '':
        # Abrimos el archivo y lo imprimimos en la consola
        with open(ruta_archivo, 'r') as archivo:
             lineas = archivo.readlines()
             #Obtenemos la informacion de: A - Acciones B - Precio C - numero de oferentes
             A = int(lineas[0])
             B = int(lineas[1])
             n = int(lineas[2])
             #print(lineas)
             #Iniciamos la lista en el tamaño de oferentes 
             oferentes = [None] * len(lineas[3:-1])
             for linea in lineas[3:-1]:
                #valores contiene cada oferentes p,r,c - NO INCLUYE GOBIERNO
                valores = linea.split(',')
                #Valores de los oferentes
                #p=oferta del oferente
                #r=maximo de acciones que compra
                #c=minimo de acciones que compra
                #respectivamente
                oferente.append(int(valores[0]))
                oferente.append(int(valores[1]))
                oferente.append(int(valores[2]))
                #print(len(lineas[3:]))
                #cargamos la lista oferentes con todos los oferentes
                #ecordando que por ultimo esta el gobierno y las acciones 
                #no vendiadaas seran vendidas al gobierno
                if(contador_oferentes != len(lineas[3:])-1):
                    oferentes[contador_oferentes] = oferente
                    oferente = []
                    contador_oferentes+=1

             #Ordenamos la lista de oferentes lexicograficamente
             oferentes_lexicografico = sorted(oferentes,key=lambda x: x)
             #contador de cantidad de oferentes para poder saber a que oferentes se le vendió
             contador_venta_of=0
             #contamos las acciones disponibles durante la ejecucion
             acciones_disponibles=A
             #guardamos la ganancia del gobierno por cada venta
             ventas_aux=[]
    
             for mejor_oferente in reversed(oferentes_lexicografico):
                contador_venta_of+=1
                print(str(mejor_oferente[0])+" "+ str(mejor_oferente[1])+ " "+ str(mejor_oferente[2]))
                #print('Precio al que compra: ' + str(mejor_oferente[0]))
                #print('max: ' + str(mejor_oferente[1])) 
                #print('min: ' + str(mejor_oferente[2]))
                #Vendemos al primero de la lista y reducimos las accion que se vendieron 
                if(acciones_disponibles != 0 
                   and mejor_oferente[2] <= acciones_disponibles
                   and mejor_oferente [1] < acciones_disponibles
                   and mejor_oferente[1] != 0):
                    #print(acciones_disponibles)
                    acciones_disponibles = acciones_disponibles - mejor_oferente[1]
                    print(acciones_disponibles)
                    ganancia_gobierno_fb += mejor_oferente[0] * mejor_oferente[1]
                    ventas_aux.append("\nSe vendieron: "+ str(mejor_oferente[1]) + " acciones" + " al oferente: (" + str(contador_venta_of) +") a un precio de: "+ str(mejor_oferente[0]))
                    #venta_acciones_pv = Label(content, text="Se vendieron: "+ str(mejor_oferente[1]) + " acciones" + " al oferente: (" + str(contador_venta_of) +") a un precio de: "+ str(mejor_oferente[0]))
                    #venta_acciones_pv.pack()
                elif(acciones_disponibles != 0 
                   and mejor_oferente[2] <= acciones_disponibles
                   and mejor_oferente [1] >= acciones_disponibles
                   and mejor_oferente[1] != 0):
                    print(str(acciones_disponibles)+" uno")
                    acciones_vendidas = acciones_disponibles
                    acciones_disponibles = acciones_disponibles - acciones_disponibles
                    ganancia_gobierno_fb += mejor_oferente[0] * acciones_vendidas
                    print(str(acciones_disponibles)+" dos")
                    ventas_aux.append("\nSe vendieron: "+ str(acciones_vendidas) + " acciones" + " al oferente: (" + str(contador_venta_of) +") a un precio de: "+ str(mejor_oferente[0]))
                    #venta_acciones_pv = Label(content, text="Se vendieron: "+ str(acciones_vendidas) + " acciones" + " al oferente: (" + str(contador_venta_of) +") a un precio de: "+ str(mejor_oferente[0]))
                    #venta_acciones_pv.pack()
                elif(acciones_disponibles != 0
                    and mejor_oferente[2] > acciones_disponibles):
                    print("Las acciones disponibles son menores a las minimas por comprar del oferente: "+str(contador_venta_of))
            
    if(acciones_disponibles != 0):
                 print(str(acciones_disponibles)+" tres")
                 ganancia_gobierno_fb+=acciones_disponibles*B
                 ventas_aux.append("\nSe vendieron: "+ str(acciones_disponibles) + " acciones" + " al GOBIERNO a un precio de: "+ str(B))
                 #venta_acciones_gob_pv = Label(content, text="Se vendieron: "+ str(acciones_disponibles) + " acciones" + " al GOBIERNO a un precio de: "+ str(B))
                 #venta_acciones_gob_pv.pack()

    ventas = ''.join(ventas_aux)
    venta_acciones_gob_pv = Label(content, text=ventas)
    venta_acciones_gob_pv.pack()

    ganancia_gob_pv = Label(content, text="Las ganancias del gobierno fueron: "+ str(ganancia_gobierno_fb))
    ganancia_gob_pv.pack()

# Botones
# Creamos el botón para abrir el archivo
boton_abrir = Button(
    content, 
    text='Abrir archivo', 
    command=(abrir_archivo),
    cursor='X_cursor'
    )
boton_abrir.pack()
# Creamos boton para ejecutar fuerza bruta
boton_fuerzabruta = Button(
    content, 
    text='Fuerza Bruta', 
    command=accionesFB,
    cursor='X_cursor'
    )
boton_fuerzabruta.pack()

# Creamos boton para ejecutar Programación Voráz
boton_voraz = Button(
    content, 
    text='Programación Voraz', 
    command=accionesV,
    cursor='X_cursor'
    )
boton_voraz.pack()
# Creamos el botón para limpiar el label
boton_limpiar = Button(
    content, 
    text='Limpiar', 
    command=limpiar_pantalla,
    cursor='X_cursor'
    )
boton_limpiar.pack()


# Ejecutamos el bucle principal de la content
content.mainloop()
