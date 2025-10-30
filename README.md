# Prueba1-Backend-2025
Trabajo de desarrollar una pagina weeb para solucionar un problema entregado por el profesor. En mi caso escogi el caso N°1 donde una empresa necesita llevar un control digital de las visitas que recibe diariamente.

Escala de apreciación entregada por el profesor

1- Identifica correctamente variables y operaciones del lenguaje.
2- Utiliza estructuras de decisión y operadores de forma adecuada.
3- Integra paquetes externos en la solución.
4- Implementa una aplicación funcional en Django según requerimientos.
5- Estructura el código de forma clara y ordenada.
6- Comenta el código para facilitar su comprensión.
7- Valida correctamente los datos de entrada.
8- Utiliza correctamente el entorno de desarrollo y herramientas asociadas
9- Cumple con los requerimientos funcionales del caso seleccionado.
10- Presenta el archivo sin errores de ejecución.


Caso:

Una empresa necesita llevar un control digital de las visitas que recibe diariamente.

Requerimientos basicos
entregados por el profesor:

- Registrar nombre, RUT, motivo de visita y hora de entrada/salida.
- Mostrar listado de visitas del día.
- Utilizar estructuras de decisión para validar datos.

Rquerimientos Agregados por mi
para un funcionamiento correcto:

- Validacion en las casillas para ingresar datos correctos
- Mostrar un mensaje de error en la casilla que esta rellena de forma incorrecta
- Usar la validacion matematica para ver si el rut esta bien ingresado y es real
- Filtro de busqueda por fecha para revisar la visitas
- Agregar un filtro opcional de hora en caso de querer buscar tambien en un rango de tiempo determinado
- Agregar filtro por nombre para buscar al visitante
- Agregar filtro para buscar por rut


Herramientas para el desarrollo:

- Django y su base de datos local integrada
- Lenguaje Python 
- Utilizando un entorno virtual (venv)
- Ulilizare tailwindcss para darle un poco de estilo a la pagina


Pasos para ejecutar correctamente el proyecto

1-Crear ambiente virtual

python -m venv venv

2-Instalar Django y paquetes

pip install django
pip install django-widget-tweaks

3-Ingresamos en la carpeta

cd GestorDeVisitas

4-Verificamos y Aplicamos las migraciones

python manage.py makemigrations GestorDeVisitas
python manage.py migrate

5-Levantar la pagina

python manage.py runserver

6-crear admin 

python manage.py createsuperuser

ragnar
ragnar@gmail.cl
Ragnar7m7.,1234



Movimos todo el proyecto a la carpeta raiz

Agregue el archivo "requirements.txt"
se ejecuta  "pip install -r requirements.txt"

Esto es necesario para levantar la pagina mediante Heroku

creamos el archivo "Procfile"

dentro del archivo settings.py se agrega esto

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

ALLOWED_HOSTS = [
    '.herokuapp.com'
]


