from tkinter import *
from tkinter import filedialog
import numpy as np

#Definamos la ruta del archivo para poder ser vista por otras funciones
ruta_archivo = ''

# Creamos la ventana principal
ventana = Tk()
# Modificamos en tamaño de la ventana 
ventana.geometry('600x400')

# Función para abrir un archivo de texto
def abrir_archivo():
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
             A = archivo.readline()
             B = archivo.readline()
             n = archivo.readline()
            #Imprimimos en la interfaz el trio de datos
             trio = Label(ventana, text="Acciones:"+ A +"Precio: "+ B + "Oferentes: " + n )
             trio.pack()

             lineas = archivo.read().split('\n')
            #Imprimiendo los oferentes
             print(lineas)
             print(''.join(lineas))
             for linea in lineas:
                 if(contador_oferentes != len(lineas)):
                    oferentes = Label(ventana, text="Oferente("+ str(contador_oferentes)+")" +"-->" + "Oferta" +"("+''.join(linea)+")")
                    oferentes.pack()
                    contador_oferentes+=1
                 else:
                     oferentes = Label(ventana, text="Gobierno: "+"-->" + "Oferta" +"("+''.join(linea)+")")
                     oferentes.pack()




# Creamos el botón para abrir el archivo
boton_abrir = Button(
    ventana, 
    text='Abrir archivo', 
    command=abrir_archivo,
    cursor='X_cursor'
    )
boton_abrir.pack()




# Ejecutamos el bucle principal de la ventana
ventana.mainloop()
