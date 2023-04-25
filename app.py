from tkinter import *
from tkinter import filedialog

#Definamos la ruta del archivo para poder ser vista por otras funciones
ruta_archivo = ''

# Creamos la ventana principal
ventana = Tk()
#titulo de la ventana
ventana.title('ADA II')
# Modificamos en tamaño de la ventana 
ventana.geometry('600x400')

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
            
             trio = Label(ventana, text="Acciones:"+ A +"Precio: "+ B + "Oferentes: " + n )
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
                     oferentes_gob = Label(ventana, text="Gobierno: "+"-->" + "Oferta" +"("+''.join(linea)+")")
                     oferentes_gob.pack()

             imprimir_oferentes = Label(ventana, text=oferentes)
             imprimir_oferentes.pack()

#Función para limpiar pantalla
def limpiar_pantalla():
    trio.destroy()
    imprimir_oferentes.destroy()
    oferentes_gob.destroy()
   # venta_acciones.pack_forget()
   # venta_acciones_gob.pack_forget()
   # ganancia_gob.pack_forget()

#funcion de fuerza bruta
def mejor_oferente_fb():
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
    
             for mejor_oferente in reversed(oferentes_lexicografico):
                contador_venta_of+=1
                #print('Precio al que cmpra: ' + str(mejor_oferente[0]))
                #print('max: ' + str(mejor_oferente[1])) 
                #print('min: ' + str(mejor_oferente[2]))
                #Vendemos al primero de la lista y reducimos las accion que se vendieron 
                if(acciones_disponibles != 0 and mejor_oferente[1] <= acciones_disponibles and mejor_oferente[1] != 0):
                    #print(acciones_disponibles)
                    acciones_disponibles = acciones_disponibles - mejor_oferente[1]
                    ganancia_gobierno_fb += mejor_oferente[0] * mejor_oferente[1]
                    venta_acciones = Label(ventana, text="Se vendieron: "+ str(mejor_oferente[1]) + " acciones" + " al oferente: (" + str(contador_venta_of) +") a un precio de: "+ str(mejor_oferente[0]))
                    venta_acciones.pack()

             if(acciones_disponibles != 0):
                 ganancia_gobierno_fb+=acciones_disponibles*B
                 venta_acciones_gob = Label(ventana, text="Se vendieron: "+ str(acciones_disponibles) + " acciones" + " al GOBIERNO a un precio de: "+ str(B))
                 venta_acciones_gob.pack()
    
    ganancia_gob = Label(ventana, text="Las ganancias del gobierno fueron: "+ str(ganancia_gobierno_fb))
    ganancia_gob.pack()              

# Función Programación Voráz
def mejor_oferente_pv():
    #global venta_acciones, venta_acciones_gob, ganancia_gob
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
    
             for mejor_oferente in reversed(oferentes_lexicografico):
                contador_venta_of+=1
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
                    venta_acciones = Label(ventana, text="Se vendieron: "+ str(mejor_oferente[1]) + " acciones" + " al oferente: (" + str(contador_venta_of) +") a un precio de: "+ str(mejor_oferente[0]))
                    venta_acciones.pack()
                elif(acciones_disponibles != 0 
                   and mejor_oferente[2] <= acciones_disponibles
                   and mejor_oferente [1] >= acciones_disponibles
                   and mejor_oferente[1] != 0):
                    print(str(acciones_disponibles)+" uno")
                    acciones_vendidas = acciones_disponibles
                    acciones_disponibles = acciones_disponibles - acciones_disponibles
                    ganancia_gobierno_fb += mejor_oferente[0] * acciones_vendidas
                    print(str(acciones_disponibles)+" dos")
                    venta_acciones = Label(ventana, text="Se vendieron: "+ str(acciones_vendidas) + " acciones" + " al oferente: (" + str(contador_venta_of) +") a un precio de: "+ str(mejor_oferente[0]))
                    venta_acciones.pack()
                elif(acciones_disponibles != 0):
                 print(str(acciones_disponibles)+" tres")
                 ganancia_gobierno_fb+=acciones_disponibles*B
                 venta_acciones_gob = Label(ventana, text="Se vendieron: "+ str(acciones_disponibles) + " acciones" + " al GOBIERNO a un precio de: "+ str(B))
                 venta_acciones_gob.pack()
    
    ganancia_gob = Label(ventana, text="Las ganancias del gobierno fueron: "+ str(ganancia_gobierno_fb))
    ganancia_gob.pack()

# Creamos el botón para abrir el archivo
boton_abrir = Button(
    ventana, 
    text='Abrir archivo', 
    command=(abrir_archivo),
    cursor='X_cursor'
    )
boton_abrir.pack()
#Creamos boton para ejecutar fuerza bruta
boton_mejor_fuerzabruta = Button(
    ventana, 
    text='Fuerza Bruta', 
    command=mejor_oferente_fb,
    cursor='X_cursor'
    )
boton_mejor_fuerzabruta.pack()
#Creamos boton para ejecutar Programación Voráz
boton_voraz = Button(
    ventana, 
    text='Programación Voráz', 
    command=mejor_oferente_pv,
    cursor='X_cursor'
    )
boton_voraz.pack()

# Creamos el botón para limpiar el label
boton_limpiar = Button(
    ventana, 
    text='Limpiar', 
    command=limpiar_pantalla,
    cursor='X_cursor'
    )
boton_limpiar.pack()



# Ejecutamos el bucle principal de la ventana
ventana.mainloop()
