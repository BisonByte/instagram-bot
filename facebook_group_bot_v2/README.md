# Facebook Group AutoPoster (Versión 2)

Esta carpeta contiene una versión que no depende del Graph API de Facebook.
En su lugar utiliza **Selenium** para automatizar el navegador y publicar como
si de un usuario real se tratara.

## Características principales

- Publicaciones en múltiples grupos rotando distintas cuentas.
- Obtención del mensaje y enlace a publicar desde una URL que devuelve un JSON.
- Puede ampliarse para responder comentarios de forma automática.

> **Nota:** este ejemplo solo tiene fines educativos. El uso de bots está sujeto
> a las políticas de Facebook y podría requerir permisos adicionales.

## Requisitos

- Python 3.8 o superior.
- Dependencias incluidas en `requirements.txt`.
- Correo y contraseña de las cuentas de Facebook que se usarán.
- Identificadores de los grupos donde se publicará.

## Funcionamiento

1. El script solicita a `JSON_URL` un objeto con las claves `message` y `link`.
2. Con cada par de credenciales definido en `FB_CREDENTIALS` se abre un navegador
   en modo *headless*, se inicia sesión y se realiza la publicación en los grupos
   de `GROUP_IDS`.
3. Una vez enviada la publicación se cierra el navegador y se pasa a la siguiente
   cuenta.

## Uso paso a paso

1. Instala las dependencias necesarias:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Define las variables en un archivo `.env` como en el siguiente ejemplo:
   ```bash
   FB_CREDENTIALS=correo1:clave1,correo2:clave2
   GROUP_IDS=123456789,987654321
   JSON_URL=https://tu-servidor.com/post.json
   ```
3. Ejecuta el bot con:
   ```bash
   python facebook_group_bot_v2/bot.py
   ```

El programa mostrará en la terminal el resultado de cada publicación que se
realiza con las distintas cuentas.
