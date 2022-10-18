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
	*Para que este bot corra correctamente, habra que instalar SQLPostgres. Se encuentra el instalador adjunto a la carpeta del bot. A su vez, se debera crear la 	base de datos en la cual se generara la informacion de las tablas. Para esto, una vez iniciada la sesion, se debera ejecutar el siguiente comando:
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
	-url_BNA=url del BNA. Ej: https://www.bna.com.ar/Personas
	-driver_path=Path en el cual se encuentra el driver mencionado anteriormente. Ej: E:\Python RPA\chromedriver.exe
	-file_Cotizaciones=Path y Nombre del archivo de output. Ej: E:\Python RPA\Calix\Bonus Track\Output\Cotizaciones.xlsx