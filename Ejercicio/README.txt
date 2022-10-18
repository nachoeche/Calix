Para la ejecucion de este bot, seran necesarios los siguientes puntos:
Instalacion de Python:
Dirigirse a la pagina 'https://www.python.org/downloads/release/python-3108/' e instalar Python 3.10.6. 
Librerias de python:
	-datetime
	-selenium
	-selenium webdriver
	-decouple
	-sqlalchemy
	-pandas
*Para realizar la instalacion de Librerias, dirigirse a la cmd y ejecutar el comando "pip install [libreria]". Ejemplo: pip install pandas	
Instalacion de Postgres:
	*Para que este bot corra correctamente, habra que instalar SQLPostgres. Se debera crear la base de datos en la cual se generara la informacion de las tablas. 	Para esto, una vez iniciada la sesion, se debera ejecutar el siguiente comando:
CREATE DATABASE nombre
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
Instalacion del driver de Chrome:
	*Para que este bot corra correctamente, se tendra que dejar en una carpeta interna al bot el archivo "chromedriver.exe" adjunto a la carpeta del bot y 		definirlo posteriormente en el archivo de input
Archivo de input:
	*El archivo de input se debe llamar ".env" y localizarse en la carpeta en la cual se ejecuta el script. Este tiene que contener las siguientes variables:
	-folder_Main: path inicial del bot. Ej: "E:\Python RPA\Calix\Ejercicio\"
	-url_museo=url que contiene el archivo de Museo. Ej:'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_4207def0-2ff7-41d5-9095-d42ae8207a5d'
	-url_bilioteca=url que contiene el archivo de Biblioteca. Ej:'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_01c6c048-dbeb-44e0-8efa-6944f73715d7'
	-url_cine=url que contiene el archivo de Cine.Ej:'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_f7a8edb8-9208-41b0-8f19-d72811dcea97'
	-folder_museo=nombre de carpeta de museos. Ej:'museos'
	-folder_bilioteca=nombre de carpeta de biblioteca. Ej:'bibliotecas'
	-folder_cine=nombre de carpeta de cines. Ej: 'cines'
	-driver_path=Nombre en el cual se encuentra el driver de chrome(Instalacion explicada anteriormente). Ej:'E:\Python RPA\chromedriver.exe'
	-log_folder=Nombre de la carpeta en la que se ubicaran los archivos de Log. Ej:"E:\Python RPA\Calix\Ejercicio\Logs\"

	-user=Usuario de Postgres. Ej:'postgres'
	-password=Password de Postgres. Ej:'test123'
	-host=Puerto de postgres. Ej:'localhost:5432'
	-base=Nombre de Base de datos de postgres creada previamente. Ej:'Ejercicio_Calix'

	folder_Postgre=Carpeta en la cual se encontraran los scripts de creacion de tablas ".sql". Estos archivos no pueden ser eliminados. Ej:'PostgreSQL'
	script_TablaUnificada=Path completo del archivo ".sql" que genera la tabla Unificada. Ej:'E:\Python RPA\Calix\Ejercicio\PostgreSQL\Tabla_DataUnificada.sql'
	script_TablaCines=Path completo del archivo ".sql" que genera la tabla Cines. Ej:'E:\Python RPA\Calix\Ejercicio\PostgreSQL\Tabla_Cines.sql'
	script_FiltroCategoria=Path completo del archivo ".sql" que genera la tabla Categoria. Ej:'E:\Python RPA\Calix\Ejercicio\PostgreSQL\Tabla_FiltroCategoria.sql'
	script_FiltroFuente=Path completo del archivo ".sql" que genera la tabla Fuente. Ej:'E:\Python RPA\Calix\Ejercicio\PostgreSQL\Tabla_FiltroFuente.sql'
	script_FiltroProvCat=Path completo del archivo ".sql" que genera la tabla Provincia/Categoria. Ej:'E:\Python RPA\Calix\Ejercicio\PostgreSQL\Tabla_FiltroProvCat.sql'
