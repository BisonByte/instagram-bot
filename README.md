# Bot de Instagram con Python

Este proyecto es un bot de Instagram desarrollado en Python que automatiza ciertas acciones en la plataforma.

## Descripción

El bot utiliza la libreria de Selenium para interactuar con la plataforma. Puede realizar diversas tareas, como seguir usuarios, dar "me gusta" a publicaciones ...

## Instalación

1. Clona este repositorio en tu máquina local:
```
git clone https://github.com/usuario/instagram-bot.git
cd instagram-bot
```

2. Instala las dependencias del proyecto:

```
python -m venv venv
source venv/bin/activate  # En Windows usa venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Configuración

Antes de ejecutar el bot puedes configurar las credenciales de dos maneras:

1. Usando un archivo `.env` con un único usuario.
2. Creando un archivo `credentials.txt` con varias cuentas, una por línea.

Ejemplo del archivo `.env`:

```python
# .env

USUARIO = 'tu_nombre_de_usuario'
CONTRASENA = 'tu_contraseña'
```

Formato de `credentials.txt`:

```
usuario1,clave1
usuario2,clave2
```

Si `credentials.txt` existe, el bot utilizará todas las cuentas secuencialmente. De lo contrario, usará las variables del `.env`.

### Uso de proxy

Si necesitas utilizar un proxy para conectarte a Instagram puedes definir la variable `PROXY` en el archivo `.env` con el formato `http://usuario:clave@host:puerto`. El bot configurará automáticamente Chrome para usar este proxy.


## Ejecución

Para iniciar el bot ejecuta:

```
python main.py
```

Se abrirá una ventana del navegador y el bot comenzará a realizar las acciones configuradas.
