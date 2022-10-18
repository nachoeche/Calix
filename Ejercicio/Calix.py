def generarCarpetas(carpeta:str,folder_Main:str):
    """Funcion encargada de verificar que existan las carpetas necesarias y de eliminar archivos de la fecha
        para no duplicar.
        Solamente se realiza el error handling sobre el path original ya que si este existe, las demas carpetas se pueden crear.
    Args:
        Carpeta(str):Carpeta a analizar
        folder_Main(str):Main Path
    Returns:
        Void: La funcion no retorna ningun valor al programa principal
    """
    #   1) Generar carpetas
    try:
        if not os.path.isdir(folder_Main +carpeta+ "\\" ):
            os.mkdir(folder_Main + carpeta + "\\")
            os.mkdir(folder_Main + carpeta + "\\" +  datetime.today().strftime('%Y-%B'))
    except OSError as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.info(',La carpeta ' + folder_Main +carpeta+ "\\ " + "no existe. Linea:" + str(exc_tb.tb_lineno) + "," + + datetime.today().strftime('%y-%m-%d %H:%M:%S'))
        logger.info(',Bot finalizado con errores. Verificar la linea informada en la linea superior.,'+ datetime.today().strftime('%y-%m-%d %H:%M:%S'))
        #Si el path inicial no es correcto, el bot frena
        raise
    
    if not os.path.isdir(folder_Main + carpeta + "\\" +  datetime.today().strftime('%Y-%B')):
        os.mkdir(folder_Main + carpeta + "\\" +  datetime.today().strftime('%Y-%B'))
    # 2) Eliminar archivo basura
    if os.path.exists(folder_Main +carpeta +"\\" +  datetime.today().strftime('%Y-%B') +"\\" + carpeta +"-" + datetime.today().strftime('%d-%m-%y') + ".csv"):
        os.remove(folder_Main +carpeta +"\\" +  datetime.today().strftime('%Y-%B') +"\\" + carpeta +"-" + datetime.today().strftime('%d-%m-%y') + ".csv")
        
def descargarArchivos(url:str,carpeta:str,folder_Main:str):
    """Funcion encargada de realizar la descarga de un archivo dado el URL inicial de la pagina.\
        Esta extrae el href del boton Descargar.
        Se abre el driver dentro de la funcion ya que, en caso de que el url no sea correcto,\
            las paginas son similares y puede llegar a descargar dos veces el mismo archivo.
            De esta manera, si el url es inexistente, se notifica el error.
    Args:
        url(str): Url de la pagina a visitar para descargar el archivo
        carpeta(str): Carpeta en la cual se depositara el archivo
        folder_Main(str):Main Path
    Returns:
        void: La funcion no retorna ningun valor al programa principal

    """    
    #   1) Descargar archivos
    logger.info(',Descargando archivo ' + carpeta + ',' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))
    try:
        try:
            #Iniciando drivers
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            options.add_argument('--disable-extensions')
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            driver_service= Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=driver_service, options=options)
        except OSError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.info(',El archivo de Chrome Driver no se existe o se ingreso un path incorrecto.  Linea:' + str(exc_tb.tb_lineno) +","+ datetime.today().strftime('%y-%m-%d %H:%M:%S'))
            logger.info(',Bot finalizado con errores. Verificar la linea informada en la linea superior.,'+ datetime.today().strftime('%y-%m-%d %H:%M:%S'))
            #Sin el driver, el bot frena
            raise
        #Realizando descarga
        driver.get(url)
        time.sleep(5)
        url_Archivo=driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div/div[3]/a[1]')
        myFile = requests.get(url_Archivo.get_property("href"))
        fileName=folder_Main +carpeta +"\\" +  datetime.today().strftime('%Y-%B') +"\\" + carpeta +"-" + datetime.today().strftime('%d-%m-%y') + ".csv"
        open(fileName,'wb').write(myFile.content)
        driver.close()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.info(',No se pudo realizar la descarga para el archivo archivo ' + carpeta + '.Error en linea: ' + str(exc_tb.tb_lineno) +"," + datetime.today().strftime('%y-%m-%d %H:%M:%S'))
        logger.info(',Bot finalizado con errores. Verificar la linea informada en la linea superior.,'+ datetime.today().strftime('%y-%m-%d %H:%M:%S'))
        #En caso de que no se genere alguno de los 3 archivos, el bot frena.
        raise
    else:
        logger.info(',Descarga exitosa para el archivo archivo ' + carpeta + ',' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))

from asyncio.windows_events import NULL
from datetime import datetime
from multiprocessing.resource_sharer import stop
from sqlite3 import DatabaseError
import sqlite3
from venv import create
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import locale
import os
import sys
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy import text
import logging
import pandas as pd


#Crear archivo y carpeta de log
if not os.path.isdir(config('log_folder')):
    os.mkdir(config('log_folder'))
logging.basicConfig(filename=config('log_folder') + 'log-' + datetime.today().strftime('%y-%m-%d') + '.csv',level=logging.INFO)
logger=logging.getLogger()
logger.info(",Accion,Fecha")
logger.info(',Inicializando el Bot,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))

# 0) Inicializar variables y configurar locale a ES
logger.info(',Inicializando variables,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))
url_categoria=[config('url_museo'),config('url_bilioteca'),config('url_cine')]
folders_categoria=[config('folder_museo'),config('folder_bilioteca'),config('folder_cine')]
folder_Main=config('folder_Main')
folder_Postgre=config('folder_Postgre')
driver_path=config('driver_path')
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')



logger.info(',Inicializando descarga de archivos,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))
# 1) Descarga de archivos

for element in range(len(url_categoria)):
    generarCarpetas(folders_categoria[element],folder_Main)
    descargarArchivos(url_categoria[element],folders_categoria[element],folder_Main)

# 2) Subida a SQL
"""Para esta parte es necesario crear un dataframe con los 3 archivos,\
    renombrar las columnas necesarias y eliminar las que no se van a utilizar para la carga.
    Luego eliminar columnas inecesarias y subir el data frame a la base de datos.
"""
    #   Generar tabla Maestra

logger.info(',Extrayendo informacion de archivos,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))
logger.info(',Creando tablas,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))
df_DataUnificada=[]
#Museos
header_names=['cod_localidad','id_provincia','id_departamento','Observaciones','categoria','subcategoria','provincia','localidad','nombre','domicilio','piso','codigo postal','cod_area','numero de telefono','mail','web','Latitud','Longitud','TipoLatitudLongitud','Info_adicional','fuente','jurisdiccion','año_inauguracion','actualizacion']
df_DataUnificada.append(pd.read_csv(folder_Main+ folders_categoria[0] + '\\' + datetime.today().strftime('%Y-%B') + '\\' + folders_categoria[0]+'-' + datetime.today().strftime('%d-%m-%y') + '.csv',skiprows=1, header=None,names=header_names))
#Bibliotecas
header_names=['cod_localidad','id_provincia','id_departamento','Observaciones','categoria','subcategoria','provincia','departamento','localidad','nombre','domicilio','piso','codigo postal','cod_area','numero de telefono','mail','web','Info_adicional','Latitud','Longitud','TipoLatitudLongitud','fuente','jurisdiccion','año_inauguracion','actualizacion']
df_DataUnificada.append(pd.read_csv(folder_Main+ folders_categoria[1] + '\\' + datetime.today().strftime('%Y-%B') + '\\' + folders_categoria[1] +'-' +datetime.today().strftime('%d-%m-%y') + '.csv',skiprows=1, header=None,names=header_names))
#Cines
header_names=['cod_localidad','id_provincia','id_departamento','categoria','provincia','departamento','localidad','nombre','domicilio','piso','codigo postal','web','Latitud','Longitud','TipoLatitudLongitud','fuente','jurisdiccion','pantallas','butacas','tipo_gestion','espacio_incaa','actualizacion']
df_DataUnificada.append(pd.read_csv(folder_Main+ folders_categoria[2] + '\\' + datetime.today().strftime('%Y-%B') + '\\' + folders_categoria[2] +'-' +datetime.today().strftime('%d-%m-%y') + '.csv',skiprows=1, header=None,names=header_names))


df_Master=pd.concat(df_DataUnificada)
    #   Generar tabla unificada con las columnas necesarias
df_DataUnificada = pd.concat(df_DataUnificada)[['cod_localidad','id_provincia','id_departamento','categoria','provincia','localidad','nombre','domicilio','codigo postal','numero de telefono','mail','web']]

"""Procesar los datos conjuntos para poder generar una tabla con la siguiente información
        o Cantidad de registros totales por categoría
        o Cantidad de registros totales por fuente
        o Cantidad de registros por provincia y categoría
"""
    #Sub tablas con los valorees de fuente, categoria y provincia/Categoria
df_fuente=[]
df_fuente=df_Master.value_counts('fuente')
df_fuente=pd.DataFrame(df_fuente)
df_categoria=[]
df_categoria=df_Master.value_counts('categoria')
df_categoria=pd.DataFrame(df_categoria)
df_provCat=[]
df_provCat=df_Master.value_counts(['id_provincia','categoria'])
df_provCat=pd.DataFrame(df_provCat)


"""Procesar la información de cines para poder crear una tabla que contenga:
        o Provincia
        o Cantidad de pantallas
        o Cantidad de butacas
        o Cantidad de espacios INCAA
"""
df_DataCines=[]
header_names=['cod_localidad','id_provincia','id_departamento','categoria','provincia','departamento','localidad','nombre','domicilio','piso','codigo postal','web','Latitud','Longitud','TipoLatitudLongitud','fuente','jurisdiccion','pantallas','butacas','tipo_gestion','espacio_incaa','actualizacion']
df_DataCines.append(pd.read_csv(folder_Main+ folders_categoria[2] + '\\' + datetime.today().strftime('%Y-%B') + '\\' + folders_categoria[2] +'-' +datetime.today().strftime('%d-%m-%y') + '.csv',skiprows=1, header=None,names=header_names))
df_DataCines = pd.concat(df_DataCines)[['id_provincia', 'pantallas','butacas', 'espacio_incaa']].groupby(['id_provincia','espacio_incaa'],as_index=False)[['pantallas','butacas',]].sum()
logger.info(',Informacion extraida correctamente,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))

"""Insertar a SQL

"""
logger.info(',Ingreso a SQL,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))
user=config('user')
password=config('password')
host=config('host')
base=config('base')

logger.info(',Creacion de Tablas,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))

engine = create_engine("postgresql://" + user + ":" + password + "@" + host + "/" + base)


with engine.connect() as con:
    with open(folder_Main+folder_Postgre + "\Tabla_DataUnificada.sql") as file:
        query = text(file.read())
        con.execute(query)
    with open(folder_Main+folder_Postgre + "\Tabla_Cines.sql") as file:
        query = text(file.read())
        con.execute(query)
    with open(folder_Main+folder_Postgre +"\Tabla_FiltroCategoria.sql") as file:
        query = text(file.read())
        con.execute(query)
    with open(folder_Main+folder_Postgre + "\Tabla_FiltroFuente.sql") as file:
        query = text(file.read())
        con.execute(query)
    with open(folder_Main+folder_Postgre+"\Tabla_FiltroProvCat.sql") as file:
        query = text(file.read())
        con.execute(query)

logger.info(',Tablas Creadas Exitosamente,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))
logger.info(',Insertando de informacion en las Tablas,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))
#Insertar Data Unificada
df_DataUnificada.insert(0, 'TimeStamp',pd.Timestamp.now(tz=None).replace(microsecond=0))
pd.DataFrame.to_sql(df_DataUnificada,con=engine, name='DataUnificada', if_exists='replace', index=False)
#Insertar Data Cine
df_DataCines.insert(0, 'TimeStamp',pd.Timestamp.now(tz=None).replace(microsecond=0))
pd.DataFrame.to_sql(df_DataCines,con=engine, name='Cines', if_exists='replace', index=False)
#Insertar Data Filtros
df_categoria.insert(1, 'TimeStamp',pd.Timestamp.now(tz=None).replace(microsecond=0))
pd.DataFrame.to_sql(df_categoria,con=engine, name='FiltroCategoria', if_exists='replace', index=True)
df_fuente.insert(1, 'TimeStamp',pd.Timestamp.now(tz=None).replace(microsecond=0))
pd.DataFrame.to_sql(df_fuente,con=engine, name='FiltroFuente', if_exists='replace', index=True)
df_provCat.insert(1, 'TimeStamp',pd.Timestamp.now(tz=None).replace(microsecond=0))
pd.DataFrame.to_sql(df_provCat,con=engine, name='FiltroProvCat', if_exists='replace', index=True)

logger.info(',Insercion Exitosa,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))

logger.info(',Fin de la ejecucion,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))