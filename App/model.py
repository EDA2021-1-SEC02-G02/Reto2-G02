"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import quicksort as qck
assert cf
from DISClib.DataStructures import listiterator as it

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = {'videos': None,
               'categorias': None}
    
    catalog['videos'] =  lt.newList('ARRAY_LIST', cmpfunction = None)
    catalog['categorias'] = mp.newMap(800,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction= None)
    return catalog

# Funciones para agregar informacion al catalogo
def addvideo(catalog, video):
    lt.addLast(catalog['videos'], video)
    category = video['category_id'] 
    addcategory(catalog, category.strip(), video)

def addcategory(catalog, categoryname, video):
    mapcategorias = catalog['categorias']
    existcategory = mp.contains(mapcategorias, categoryname)
    if existcategory:
        pareja = mp.get(mapcategorias, categoryname)
        category= me.getValue(pareja)
    else:
        category = newcategory(categoryname)
        mp.put(mapcategorias, categoryname, category)
    lt.addLast(category['videos'], video)
        
    

# Funciones para creacion de datos
def newcategory(categorynumber):
    category = {'number_category': "", "videos": None}
    category['number_category'] = categorynumber
    category['videos'] = lt.newList('ARRAY_LIST')
    return category

# Funciones de consulta

def getvideosbycategory(catalog, categorynumber, cantidad):
    category= mp.get(catalog['categorias'], categorynumber)
    if category:
        lista = me.getValue(category)
        
        lista= lista['videos']
        result = sortVideos(lista, cantidad, cmpVideosByViews)
        return result
    return None

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def cmpVideosByViews(video1, video2):
    if video1['views'] < video2['views']:
        return True
    else:
        return False
    
def sortVideos(lst,size,cmp):
    copia_lista = lst.copy()
    list_orden = qck.sort(copia_lista, cmp)
    resul = lt.subList(list_orden, 1, size)
    return resul