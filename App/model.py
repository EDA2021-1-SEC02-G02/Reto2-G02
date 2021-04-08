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
               'paisescat': None,
               'categorias': None,
               'paises': None,
               'tendencias': None}
    
    catalog['videos'] =  lt.newList('ARRAY_LIST', cmpfunction = None)
    
    catalog['paisescat']= mp.newMap(10,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=None)
    
    catalog['categorias'] = mp.newMap(18,
                                      maptype='PROBING',
                                      loadfactor=0.5,
                                      comparefunction= None)
    
    catalog['paises'] = mp.newMap(10,
                                   maptype='PROBING',
                                   loadfactor=0.5,
                                   comparefunction= None)
    return catalog


# Funciones para agregar informacion al catalogo

def addvideo(catalog, video):
    lt.addLast(catalog['videos'], video)
    pais= video['country']
    videoid = video["video_id"]
    category = video['category_id']
    
    addcountry(catalog, pais.strip(), videoid.strip(), video)
    addcategory(catalog, category.strip(), videoid.strip(), video)
    addpaisescat(catalog, pais.strip(), category.strip(), video)

def addpaisescat(catalog, pais, categoria, video):
    mappaiscat = catalog['paisescat']
    existcountry = mp.contains(mappaiscat, pais)
    if existcountry:
        country = mp.get(mappaiscat, pais)
        category = me.getValue(country)
        if categoria in category:
            lt.addLast(category[categoria], video)
        else:
            category= addnewcategorycat(category, categoria, video)
    else:
        dic = {}
        dic = addnewcategorycat(dic, categoria, video)
        mp.put(mappaiscat, pais, dic)

def addcategory(catalog, categoryname, videoid, video):
    mapcategorias = catalog['categorias']
    existcategory = mp.contains(mapcategorias, categoryname)
    if existcategory:
        pareja = mp.get(mapcategorias, categoryname)
        category= me.getValue(pareja) # category seria el nuevo map
    else:
        category = newmap()
        mp.put(mapcategorias, categoryname, category)
    category = tendencias(category, videoid, video)   
    
def addcountry(catalog, countryname, videoid, video):
    pass
    mappaises = catalog['paises']
    existcountry = mp.contains(mappaises, countryname)
    if existcountry:
        pareja = mp.get(mappaises, countryname)
        country = me.getValue(pareja)
    else:
        country = newmap()
        mp.put(mappaises, countryname, country)
    countryi = tendencias(country, videoid, video)
        
def tendencias(mapp, videoid, video):
    existvideo = mp.contains(mapp, videoid)
    if existvideo:
        pareja = mp.get(mapp, videoid)
        trending= me.getValue(pareja)
        trending["tendencias"]+=1
    else:
        trending= {'videoid': videoid , 'tendencias': 1 , 'video' : video}
        mp.put(mapp, videoid, trending)

def newmap():
    country= mp.newMap(120000, #poner 120000
                       maptype='PROBING',
                       loadfactor=0.9,
                       comparefunction=None)

    return country
       

# Funciones para creacion de datos
def newcategory(categorynumber):
    category = {'number_category': "", "videos": None}
    category['number_category'] = categorynumber
    category['videos'] = lt.newList('ARRAY_LIST')
    return category

def addnewcategorycat(dic, categorynumber, video):
    dic[str(categorynumber)]= lt.newList('ARRAY_LIST')
    lt.addLast(dic[str(categorynumber)], video)
    return dic

def addnewcountry(countryname):
    country = {'name_country': "", "videos": None}
    country['name_country'] = countryname
    country['videos'] = lt.newList('ARRAY_LIST')
    return country



# Funciones de consulta
def requerimiento1(catalog, countryname, categorynumber, cantidad):
    pais = mp.get(catalog['paisescat'], countryname)
    if pais:
        dicccat = me.getValue(pais)
        lista = dicccat[categorynumber]
        result = sortVideos(lista, cmpVideosByViews)
        lista_retornar = None
        lista_retornar= lt.newList('ARRAY_LIST')
        iterador = it.newIterator(result)
        i=0
        while (it.hasNext(iterador)) and i<cantidad:
            elemento= it.next(iterador)
            lt.addLast(lista_retornar, elemento)
            i+=1
        return lista_retornar 
    return None

def requerimiento2(catalog, pais):
    pais = mp.get(catalog['paises'], pais)
    if pais:
        mapcountry = me.getValue(pais)
        values = mp.valueSet(mapcountry)
        sol_requ2 = mayor_trending(values)
        return sol_requ2
    else:
        return None
        
def mayor_trending(arraylist):
    if arraylist:
        mayor_trending = 0
        infovideo  = None
        for video in lt.iterator(arraylist):
            if video['tendencias'] > mayor_trending:
                mayor_trending =video['tendencias']
                infovideo = video['video']
        
        return infovideo, mayor_trending
    else:
        return None
    
    

# Funciones utilizadas para comparar elementos dentro de una lista


# Funciones de ordenamiento
def cmpVideosByViews(video1, video2):
    if float(video1['views']) > float(video2['views']):
        return True
    else:
        return False
    
def sortVideos(lst,cmp):
    size= lt.size(lst)
    copia_lista = lst.copy()
    list_orden = qck.sort(copia_lista, cmp)
    resul = lt.subList(list_orden, 1, size)
    return resul


def funordenamientos(catalog):
    paisescat = catalog['paisescat']
    keylist = mp.keySet(paisescat)
    iterador = it.newIterator(keylist)
    while it.hasNext(iterador):
        dicc = it.next(iterador)
        for f in dicc.values():
            pass
    