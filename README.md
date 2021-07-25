# flask-postgres-0109

El proyecto utiliza las siguientes tecnologias

- Flask
- Python
- PostgreSQL
- Virtualenv
- SqlAlchemy

## Instalación de Virtualenv

En el caso que no lo tuvieramos instalado en el equipo usamos lo siguiente

```sh
$ pip install virtualenv
```

## Configuración del Virtualenv

Abrimos el terminal en la ubicación de la carpeta del proyecto

```sh
$ python -m venv venv
$ source venv/bin/activate
```

Si queremos salir de la venv usamos lo siguiente

```sh
$ deactivate
```

## Dependencias

Es necesario instalar estas dependencias para el proyecto

```sh
$ pip flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy 
```

Podemos instalar las dependencias directamente del archivo txt

```sh
$ pip freeze > requirements.txt
````

## Despliegue

Lo hacemos de manera local

```sh
$ python app.py
```
## Heroku Deploy

Lo primero que tenemos que hacer es logearnos con nuestra cuenta heroku. Antes de ello debemos instalar heroku cli en nuestra mac.

```sh
$ heroku login
```

Como estamos usando una bd de postgres. Nos dirigimos en Resources y agregamos Heroku Postgres.

Debemos crear los siguientes archivos en nuestro proyecto Procfile con el siguiente contenido:

> web: gunicorn app:app

Ademas, agregar la siguiente dependencia:

> gunicorn

Cuando subimos unos cambios ejecutamos lo siguiente en la consola en la ubicacion de la carpeta de nuestro proyecto.

```sh
$ git add .
$ git commit -am "make it better"
$ git push heroku main
```
