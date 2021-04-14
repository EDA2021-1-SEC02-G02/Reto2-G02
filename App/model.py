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
from DISClib.Algorithms.Sorting import mergesort as marg
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
    
    catalog['tags'] = mp.newMap(10,
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
    tags(catalog, pais.strip(), video)

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
    mappaises = catalog['paises']
    existcountry = mp.contains(mappaises, countryname)
    if existcountry:
        pareja = mp.get(mappaises, countryname)
        country = me.getValue(pareja)
    else:
        country = newmap()
        mp.put(mappaises, countryname, country)
    country = tendencias(country, videoid, video)
    
def tags(catalog, countryname, video):
    maptags = catalog['tags']
    existcountry = mp.contains(maptags, countryname)
    if existcountry:
        pareja = mp.get(maptags, countryname)
        country = me.getValue(pareja)
        lt.addLast(country, video)
    else:
        country = lt.newList('ARRAY_LIST')
        lt.addLast(country, video)
        mp.put(maptags, countryname, country)
    
        
        

# Funciones para creacion de datos

def addnewcategorycat(dic, categorynumber, video):
    dic[str(categorynumber)]= lt.newList('ARRAY_LIST')
    lt.addLast(dic[str(categorynumber)], video)
    return dic

def tendencias(mapp, videoid, video):
    existvideo = mp.contains(mapp, str(videoid))
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


# Funciones de consulta
def requerimiento1(catalog, countryname, categorynumber, cantidad):
    pais = mp.get(catalog['paisescat'], countryname)
    if pais:
        dicccat = me.getValue(pais)
        lista = dicccat[categorynumber]
        result = sortVideos(lista, cmpVideosByViews)
        lista_retornar= None
        lista_retornar= lt.newList('ARRAY_LIST')
        iterador = it.newIterator(result)
        i=0
        while (it.hasNext(iterador)) and i<cantidad:
            elemento= it.next(iterador)
            lt.addLast(lista_retornar, elemento)
            i+=1
        return lista_retornar
    else:
        return None

def requerimiento2(catalog, country):
    pais = mp.get(catalog['paises'], country)
    if pais:
        mapcountry = me.getValue(pais)
        values = mp.valueSet(mapcountry)
        sol_requ2 = mayor_trending(values)
        return sol_requ2
    else:
        return None
       
def requerimiento3(catalog, categoria):
    categorias = mp.get(catalog['categorias'], categoria)
    if categorias:
        mapcategorias = me.getValue(categorias)
        values = mp.valueSet(mapcategorias)
        sol_requ3 = mayor_trending(values)
        return sol_requ3
    else:
        return None
       
def requerimiento4(catalog, pais, tag, cantidad):
    tags = mp.get(catalog['tags'], pais)
    if tags:
        lista = me.getValue(tags)
        result = sortVideos(lista, cmpvideosbylikes)
        lista_retornar = findvideos(result, tag, cantidad)
        return lista_retornar
    else:
        return None


# funciones auxiliares para consultar datos.     
def findvideos(listavid, tag, cantidad):
    lista_retornar = lt.newList('ARRAY_LIST')
    iterador = it.newIterator(listavid)
    cant_videos = 0
    
    while (it.hasNext(iterador)) and cant_videos<cantidad:
        elemento = it.next(iterador)
        elemento['tags'] = str(elemento['tags'].lower())
        if ( str(tag.lower()) in (str(elemento['tags'].lower())) ) == True:
            lt.addLast(lista_retornar, elemento)
        else: 
            None
        cant_videos  = lt.size(lista_retornar)
    return lista_retornar
          
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
def cmpVideosByViews(video1, video2):
    if float(video1['views']) > float(video2['views']):
        return True
    else:
        return False

def cmpvideosbylikes(video1, video2):
    if float(video1['likes']) > float(video2['likes']):
        return True
    else:
        return False 



# Funciones de ordenamiento
    
def sortVideos(lst,cmp):
    size= lt.size(lst)
    copia_lista = lst.copy()
    list_orden = marg.sort(copia_lista, cmp)
    return list_orden

    