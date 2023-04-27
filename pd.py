from tkinter import *
from tkinter import filedialog

#Definamos la ruta del archivo para poder ser vista por otras funciones
ruta_archivo = ''

# Creamos la ventana principal
ventana = Tk()
#titulo de la ventana
ventana.title('ADA II-2')
# Modificamos en tamaño de la ventana 
ventana.geometry('600x400')

# Función para abrir un archivo de texto (.sub o .psub)
def abrir_archivo():
    
    global trio, imprimir_oferentes, oferentes_gob
    global ruta_archivo
    # Definimos los tipos de archivo permitidos
    tipos_archivo = [('Archivos de psubasta', '*.psub'),('Archivos de subasta', '*.sub') ]
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

# Función para limpiar pantalla
def limpiar_pantalla():
    trio.destroy()
    imprimir_oferentes.destroy()
    oferentes_gob.destroy()
    

def subasta_publica():

    oferente = []
    contador_oferentes=0

    if ruta_archivo != '':
        # Abrimos el archivo y lo imprimimos en la consola
        with open(ruta_archivo, 'r') as archivo:
             lineas = archivo.readlines()
             #Obtenemos la informacion de: A - Acciones B - Precio C - numero de oferentes
             acciones = int(lineas[0])
             precio_minimo = int(lineas[1])
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

    n = len(oferentes)
    # Matriz de memoria para la programación dinámica
    memo = [[None for j in range(acciones + 1)] for i in range(n + 1)]
    
    # Función recursiva auxiliar que implementa la programación dinámica
    def dp(i, j):
        # print("abrir")
        # Si ya se ha calculado este valor, devolverlo
        if memo[i][j] is not None:
            return memo[i][j]
        
        # Casos base
        if i == n:
            # Se acabaron las ofertas, solo se pueden comprar acciones al precio mínimo
            memo[i][j] = j * precio_minimo
            return memo[i][j]
        if j == 0:
            # No se quieren comprar acciones, el precio es 0
            memo[i][j] = 0
            return memo[i][j]
        
        # Comprobar si se puede aceptar la oferta actual
        oferta = oferentes[i]
        precio = oferta[0]
        maximo = oferta[1]
        minimo = oferta[2]
        
        max_acciones = min(j, maximo) # No se pueden comprar más acciones de las que ofrece la oferta o de las que quedan por vender
        min_acciones = min(j, minimo) # Se deben comprar al menos las acciones mínimas o las que quedan por vender
        
        # Si no se pueden comprar las acciones mínimas, se descarta la oferta
        if min_acciones > max_acciones:
            memo[i][j] = dp(i+1, j)
            return memo[i][j]
        
        # Calcular la ganancia si se acepta la oferta
        ganancia = precio * min_acciones + dp(i+1, j-min_acciones)
        
        
        # Probar a aceptar la oferta y otras ofertas
        for k in range(min_acciones+1, max_acciones+1):
            #print(precio*min_acciones)
            ganancia_k = precio * k + dp(i+1, j-k)
            if ganancia_k > ganancia:
                ganancia = ganancia_k
                
        
        # No aceptar la oferta y seguir probando otras ofertas
        ganancia_no = dp(i+1, j)
        if ganancia_no > ganancia:
            ganancia = ganancia_no
        
        memo[i][j] = ganancia
        
        return memo[i][j]
    
    # Llamada inicial a la función recursiva
    print(dp(0, acciones))
    

# Botones
# Creamos el botón para abrir el archivo
boton_abrir = Button(
    ventana, 
    text='Abrir archivo', 
    command=(abrir_archivo),
    cursor='X_cursor'
    )
boton_abrir.pack()
# Creamos boton para ejecutar fuerza bruta
boton_mejor_fuerzabruta = Button(
    ventana, 
    text='pd', 
    command=subasta_publica,
    cursor='X_cursor'
    )
boton_mejor_fuerzabruta.pack()

# Ejecutamos el bucle principal de la ventana
ventana.mainloop()