# Facebook Group AutoPoster & AutoResponder Bot

Este proyecto demuestra cómo publicar de forma automática en grupos de Facebook
utilizando el **Graph API** oficial. Además incluye un ejemplo para responder
comentarios de las publicaciones que genera.

## Características principales

- Publicaciones en varios grupos usando diferentes tokens en rotación.
- Descarga el contenido a publicar de una URL que devuelve un JSON con los
  campos `message` y `link`.
- Respuesta automática a los comentarios de cada publicación.

> **Nota:** todo el código se proporciona únicamente con fines educativos. El uso
de bots automatizados está sujeto a las políticas de Facebook y puede requerir
permisos especiales. Asegúrate de disponer de las autorizaciones necesarias
antes de usarlo.

## Requisitos

- Python 3.8 o superior.
- Dependencias listadas en `requirements.txt`.
- Tokens de acceso válidos para cada cuenta que vaya a publicar.
- Identificadores (ID) de los grupos donde se publicará.

## Funcionamiento

1. El script descarga desde `JSON_URL` un objeto como:
   ```json
   {"message": "Hola a todos", "link": "https://ejemplo.com"}
   ```
2. Con cada token definido en `TOKENS` se publica el mensaje en los grupos
   indicados por `GROUP_IDS`.
3. Tras publicar, el primer token se utiliza para revisar los comentarios en cada
   publicación y responder con el texto de `REPLY_MESSAGE`.

## Uso paso a paso

1. Instala las dependencias:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Crea un archivo `.env` (o define variables de entorno) con las claves:
   ```bash
   TOKENS=token1,token2,token3
   GROUP_IDS=123456789,987654321
   JSON_URL=https://tu-servidor.com/post.json
   REPLY_MESSAGE=Gracias por tu comentario!
   ```
3. Ejecuta el bot:
   ```bash
   python facebook_group_bot/bot.py
   ```

El programa mostrará en consola el identificador de cada publicación y las
respuestas que envía en los comentarios.
