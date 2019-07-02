# TINDER

Los scripts de esta carpeta permiten hacer un scaneo de los usuarios de Tinder, almacenando su información. Se obtienen los nombres, fechas de nacimiento, fotografías, información sobre luegares de trabajo, estudios, etc.

### Prerequisites

Es necesario tener Google Chrome e instalar el driver (Chromedriver adecuado en función del SO y versión de navegador).
Para descargar Chromedriver: http://chromedriver.chromium.org/downloads
En esta carpeta viene Chromedriver compativle con la versión de Chrome 72.xx, para otras versiones será necesario descargar el chromedriver correspondiente.

## Getting Started

Lo primero es neceario obtener un access_token de Facebook para poder utilizar los scripts puesto que el Login de Tinder se realiza a través de facebook.
Para obtener el token hay que utilizar el script fb_token.py que utiliza por debajo Selenium.
 
Hay que modificar el archivo fb_token.py y añadir el email y el password de facebook con el que se quiere acceder a Tinder:

```
tk=get_fb_access_token('mail','pass')
```
Se ejecuta de la siguiente manera:

```
python3 fb_token.py
```

Por consola se devuelven dos valores, el token y el userId. 
Hay que abrir el fichero api.py y modificarlo añadiendo en el el token y el userId obtenidos gracias al fichero fb_token.py

```
tk=get_auth_token("token","userId")

```

Ejecutamos el script api.py

```
python3.py
```

