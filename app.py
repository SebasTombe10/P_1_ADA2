from tkinter import *
from tkinter import filedialog
import datetime


#Definamos la ruta del archivo para poder ser vista por otras funciones
ruta_archivo = ''

# Creamos la content principal
ventana = Tk()

#titulo de la content
ventana.title('ADA II')

# Modificamos en tamaño de la content 
ventana.geometry('500x400')

# Crear un marco dentro de la content principal
frame = Frame(ventana)
frame.pack(fill=BOTH, expand=True)

# Agregar el widget de contenido a la content principal
canvas = Canvas(frame)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

# Agregar un widget de barra de desplazamiento al marco
scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

# Conectar el widget de contenido al widget de la barra de desplazamiento
canvas.configure(yscrollcommand=scrollbar.set)

# Añadir contenido al canvas
content = Frame(canvas)
canvas.create_window((canvas.winfo_reqwidth()/2, 0), window=content, anchor=NW)
print(canvas.winfo_reqwidth()/2)
canvas.config(scrollregion=(0,0,0,4000))

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
    txt_ventas_aux=[]
    acciones_disponibles = 0
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
             txt_contador_venta_of=0
             #contamos las acciones disponibles durante la ejecucion
             acciones_disponibles=A
             #guardamos la ganancia del gobierno por cada venta
             ventas_aux=[]
             no_ventas_aux=[]
             
             txt_ventas_aux=[0 for i in range(len(oferentes_lexicografico))]
             for mejor_oferente in reversed(oferentes_lexicografico):
                contador_venta_of+=1
                
                #Vendemos al primero de la lista y reducimos las accion que se vendieron 
                if(acciones_disponibles != 0 and mejor_oferente[1] <= acciones_disponibles and mejor_oferente[1] != 0):
                    #print(acciones_disponibles)
                    acciones_disponibles = acciones_disponibles - mejor_oferente[1]
                    ganancia_gobierno_fb += mejor_oferente[0] * mejor_oferente[1]
                    ventas_aux.append("\nSe vendieron: "+ str(mejor_oferente[1]) + " acciones" + " al oferente: (" + str(contador_venta_of) +") a un precio de: "+ str(mejor_oferente[0]))

                    #venta_acciones = Label(content, text="Se vendieron: "+ str(mejor_oferente[1]) + " acciones" + " al oferente: (" + str(contador_venta_of) +") a un precio de: "+ str(mejor_oferente[0]))
                    txt_ventas_aux[txt_contador_venta_of] = str(mejor_oferente[1])

                    #venta_acciones.pack()
                else:
                    no_ventas_aux.append("\nNo se vendieron acciones" + " al oferente: " + str(contador_venta_of))
                
                txt_contador_venta_of+=1

             ventas = ''.join(ventas_aux)

             venta_acciones = Label(content, text=ventas)
             venta_acciones.pack()   


             if(acciones_disponibles != 0):
                 ganancia_gobierno_fb+=acciones_disponibles*B
                 venta_acciones_gob = Label(content, text="Se vendieron: "+ str(acciones_disponibles) + " acciones" + " al GOBIERNO a un precio de: "+ str(B))
                 venta_acciones_gob.pack()
    

    ganancia_gob = Label(content, text="Las ganancias del gobierno fueron: "+ str(ganancia_gobierno_fb))
    ganancia_gob.pack()              

    # Concatenar los elementos de la lista en una variable
    lista_vertical = "\n".join(str(elemento) for elemento in txt_ventas_aux)
    
    #Imprimiend el archivo de salida
    # Obtener la fecha y hora actual
    fecha_actual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Concatenar la fecha y hora al nombre del archivo
    nombre_archivo = f"Fuerza_bruta_{fecha_actual}.txt"

    # Obtener la ruta y el nombre del archivo de salida
    archivo_salida = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Archivos de texto", "*.txt"),
                                                             ("Todos los archivos", "*.*")],
                                                   initialfile=nombre_archivo )
    # Escribir los datos en el archivo
    with open(archivo_salida, "w") as archivo:
        archivo.write("costo \n" + str(ganancia_gobierno_fb) + "\n" + lista_vertical + "\n" +"resto \n" + str(acciones_disponibles))              


# Función Programación Voráz
def accionesV():
    global venta_acciones_pv, venta_acciones_gob_pv, ganancia_gob_pv
    oferente = []
    contador_oferentes=0
    ganancia_gobierno_fb=0
    txt_ventas_aux=[]
    acciones_disponibles = 0
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
             txt_contador_venta_of=0
             #contamos las acciones disponibles durante la ejecucion
             acciones_disponibles=A
             #guardamos la ganancia del gobierno por cada venta
             ventas_aux=[]

             txt_ventas_aux=[0 for i in range(len(oferentes_lexicografico))]
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
                    txt_ventas_aux[txt_contador_venta_of] = str(mejor_oferente[1])
 
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
                    txt_ventas_aux[txt_contador_venta_of] = str(acciones_vendidas)

                    #venta_acciones_pv.pack()
                elif(acciones_disponibles != 0
                    and mejor_oferente[2] > acciones_disponibles):
                    print("Las acciones disponibles son menores a las minimas por comprar del oferente: "+str(contador_venta_of))
                
                txt_contador_venta_of+=1

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

    # Concatenar los elementos de la lista en una variable
    lista_vertical = "\n".join(str(elemento) for elemento in txt_ventas_aux)

    #Imprimiend el archivo de salida
    # Obtener la fecha y hora actual
    fecha_actual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Concatenar la fecha y hora al nombre del archivo
    nombre_archivo = f"Programacion voraz_{fecha_actual}.txt"

    # Obtener la ruta y el nombre del archivo de salida
    archivo_salida = filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Archivos de texto", "*.txt"),
                                                             ("Todos los archivos", "*.*")],
                                                   initialfile=nombre_archivo )
    # Escribir los datos en el archivo
    with open(archivo_salida, "w") as archivo:
        archivo.write("costo \n" + str(ganancia_gobierno_fb) + "\n" + lista_vertical + "\n" +"resto \n" + str(acciones_disponibles))

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
