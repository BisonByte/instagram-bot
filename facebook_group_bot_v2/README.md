# Facebook Group AutoPoster (Versión 2)

Esta carpeta contiene una variante que automatiza la publicación en
grupos de Facebook **sin** utilizar el API oficial. Se apoya en Selenium
para interactuar con la interfaz de la web directamente.

## Características

- Publica en múltiples grupos rotando varias cuentas.
- Descarga el contenido a publicar desde una URL que devuelve un JSON.
- Puede ampliarse para responder comentarios de forma automática.

> **Nota:** El código es únicamente educativo. El uso de bots está sujeto
> a las políticas de Facebook y puede requerir permisos adicionales.

## Requisitos

- Python 3.8 o superior.
- Paquetes indicados en `requirements.txt`.
- Credenciales (correo y contraseña) de las cuentas de Facebook.
- Los identificadores de los grupos donde se realizarán las publicaciones.

## Uso rápido

1. Instala las dependencias:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Define las variables de entorno o crea un `.env` con:
   - `FB_CREDENTIALS`: lista separada por comas con pares `correo:clave`.
   - `GROUP_IDS`: lista separada por comas con los ID de los grupos.
   - `JSON_URL`: dirección desde donde se obtiene el contenido a publicar.

3. Ejecuta el script:
   ```bash
   python facebook_group_bot_v2/bot.py
   ```
