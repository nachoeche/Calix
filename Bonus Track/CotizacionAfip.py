"""Importar librerias
    -> Selenium: Automatizar portales web.
    ->Selenium.webdriver: Traerse el webdriver de una carpeta en especifico.
    ->Pandas: Automatizar tablas e ingreso a csv, xls,xlsx entre otros. ->openpyxl
    ->Time: Funciones relacionadas a tiempo.
    ->Decouple: Extraer data Input File(.env).
    
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import os
from decouple import config
from datetime import datetime
import logging
import sys
"""Realizar un programa que tome las cotizaciones de la pagina de bna y las introduzca en un excel como output
    ->Estrategia:
    1) Abrir portal
    2) Extraer tabla
    3) Ingresarla tabla al Excel final
"""
#Variables:
driver_path=config('driver_path')
url_BNA=config('url_BNA')
file_Cotizaciones=config('file_Cotizaciones')
folder_output=config('folder_output')
try:
    if not os.path.isdir(config('log_folder')):
        os.mkdir(config('log_folder'))
except Exception as e:
    raise
logging.basicConfig(filename=config('log_folder') + 'log-' + datetime.today().strftime('%y-%m-%d') + '.csv',level=logging.INFO)

#   1) Abrir portal - Opciones de Navegacion
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
logger=options.add_experimental_option("excludeSwitches", ["enable-logging"])
logger=logging.getLogger()
logger.info(",Accion,Fecha")
logger.info(',Inicializando el Bot,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))


logger.info(',Extrayendo tabla del portal web,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))

try:
    #Iniciando drivers
    driver_service= Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=driver_service, options=options)
except OSError as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logger.info(',El archivo de Chrome Driver no se existe o se ingreso un path incorrecto.  Linea:' + str(exc_tb.tb_lineno) +","+ datetime.today().strftime('%y-%m-%d %H:%M:%S'))
    logger.info(',Bot finalizado con errores. Verificar la linea informada en la linea superior.,'+ datetime.today().strftime('%y-%m-%d %H:%M:%S'))
    #Sin el driver, el bot frena
    raise
try:
    #   1) Abrir portal - Inicializar Browser
    driver.get(url_BNA)
    time.sleep(5)

    #   2) Extraer tabla - Extraer informacion de la tabla

    fecha=driver.find_elements(By.XPATH,'//*[@id="billetes"]/table/thead/tr/th[1]')
    monedas=driver.find_elements(By.XPATH,'//*[@id="billetes"]/table/tbody/tr/td[1]')
    cotizacionCompra=driver.find_elements(By.XPATH,'//*[@id="billetes"]/table/tbody/tr/td[2]')
    cotizacionVenta=driver.find_elements(By.XPATH,'//*[@id="billetes"]/table/tbody/tr/td[3]')
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logger.info(',No se pudo obtener la cotizacion del dia de la fecha. Error en linea: ' + str(exc_tb.tb_lineno) +"," + datetime.today().strftime('%y-%m-%d %H:%M:%S'))
    logger.info(',Bot finalizado con errores. Verificar la linea informada en la linea superior.,'+ datetime.today().strftime('%y-%m-%d %H:%M:%S'))
    #No se pudo traer la cotizacion del dia de la fecha, el bot frena.
    raise

#   2) Extraer tabla - Generar tabla
logger.info(',Generando tablas,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))
table_Cotizaciones=[]


for i in range(len(monedas)):
    #Verificar el sistema de puntuacion en su maquina
    promedioActual=(float(cotizacionCompra[i].text.replace(',','.'))+float(cotizacionVenta[i].text.replace(',','.')))/2
    data_temp={
        'Moneda':monedas[i].text,
        'Compra':float(cotizacionCompra[i].text.replace(',','.')),
        'Venta':float(cotizacionVenta[i].text.replace(',','.')),
        'Promedio':promedioActual
        }
    table_Cotizaciones.append(data_temp)

#   3) Ingresarla tabla al Excel final - Ingresar Tabla
try:
    if not os.path.isdir(folder_output):
        os.mkdir('output_folder')
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logger.info(',El path especificado para la carpeta de output es erroneo. Verificar Linea: ' + str(exc_tb.tb_lineno) +"," + datetime.today().strftime('%y-%m-%d %H:%M:%S'))
    logger.info(',Bot finalizado con errores. Verificar la linea informada en la linea superior.,'+ datetime.today().strftime('%y-%m-%d %H:%M:%S'))
    #La carpeta de output fue mal especificada
    raise
df_TablaCotizaciones=pd.DataFrame(table_Cotizaciones)

df_TablaCotizaciones.to_excel(file_Cotizaciones, index=False)
logger.info(',Fin de la ejecucion,' + datetime.today().strftime('%y-%m-%d %H:%M:%S'))