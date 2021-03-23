# Flask Postgres SQLAlchemy

### Codigo 8BND-BCRA-WSXA

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

## Despliegue

Lo hacemos de manera local

```sh
$ python app.py
```