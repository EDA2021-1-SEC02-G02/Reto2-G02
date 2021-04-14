"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1 - Cargar información en el catálogo")
    print("2 - Req1: N videos tendencia en un pais por categoria.")
    print("3 - Req2: Video que mas dias ha sido trending para un pais.")
    print("4 - Req3: Video que mas dias ha sido trending para una categoria.")
    print("5 - Req4: N videos con mas liikes de un pais con un tag especifico.")
    print('0 - Salir.')

def initcatalog():
    return controller.initcatalog()

def loaddata(catalog):
    controller.loaddata(catalog)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        cont = controller.initcatalog()
        catalog = controller.loaddata(cont)
        print('Videos cargados: ', lt.size(cont['videos']))
        print("Tiempo [ms]: ", f"{catalog[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{catalog[2]:.3f}")

    # Requerimiento 1.
    elif int(inputs[0]) == 2:
        pais = input("Ingrese el pais: ")
        categoria = input("Ingrese la categoria: ")
        cantidad = input("Ingrese la cantidad de videos que desea ver: ") 
        sol = controller.requerimiento1(cont, str(pais), str(categoria), int(cantidad))

        if sol:
            for video in lt.iterator(sol):
                print( '--> '+ 
                    'trending_date: '  + video['trending_date']            + ' ||' +
                    ' Title: '         + video['title']                    + ' ||' +
                    ' Channel_title: ' + video['channel_title']            + ' ||' +
                    ' Publish_time: '  + video['publish_time']             + ' ||' +
                    ' Views: '         + video['views']                    + ' ||' + 
                    ' Likes: '         + video['likes']                    + ' ||' +
                    ' Dislikes: '      + video['dislikes'])
            print("\n")
        else:
            print('Es posible que el pais o categoria que busque no existe.\n')   
    
    # Requerimiento 2.
    elif int(inputs[0]) == 3:
        pais = input('Ingrese el nombre del pais a buscar: ')
        sol = controller.requerimiento2(cont, str(pais))
        video  = sol[0]
        print('--> '+
              ' Title: '         + video['title']          + ' ||' +
              ' Channel_title: ' + video['channel_title']  + ' ||' +
              ' Country: '       + video['country']        + ' ||' + 
              ' Dias: '          + str(sol[1])             + '.'   )   
    
    # Requerimiento 3.
    elif int(inputs[0]) == 4:
        categoria = input('Ingrese el nombre de la categoria a buscar: ')
        sol = controller.requerimiento3(cont, str(categoria))
        video  = sol[0]
        print('--> '+
              ' Title: '          + video['title']           + ' ||' +
              ' Channel_title: '  + video['channel_title']   + ' ||' +
              ' Country: '        + video['country']         + ' ||' + 
              ' Dias: '           + str(sol[1])              + '.'   )
    
    # Requerimiento 4.
    elif int(inputs[0]) == 5:
        pais = input('Ingrese el nombre del pais a buscar: ')
        tag = input('Ingrese el Tag en el que sea buscar: ')
        cantidad = input('ingrese la cantidad de videos a listar con el tag: ')
        sol =  controller.requerimiento4(cont, str(pais), str(tag), int(cantidad))
        
        if sol:
            for video in lt.iterator(sol):
                print( '--> '+ 
                    ' Title: '          + video['title']          + ' ||' +
                    ' Channel_title: '  + video['channel_title']  + ' ||' +
                    ' Publish_time: '   + video['publish_time']   + ' ||' +
                    ' Views: '          + video['views']          + ' ||' + 
                    ' Likes: '          + video['likes']          + ' ||' +
                    ' Dislikes: '       + video['dislikes']       + ' ||' + 
                    'Tags : '           + video['tags']           + '.'   )
            print("\n")
        else:
            print('Es posible que el pais o categoria que busque no existe.\n')
        
    else:
        sys.exit(0)
sys.exit(0)
