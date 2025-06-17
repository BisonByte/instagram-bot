# Facebook Group AutoPoster & AutoResponder Bot

Esta carpeta contiene un proyecto de ejemplo para publicar
automáticamente en grupos de Facebook y responder mensajes o
comentarios utilizando el API de Facebook.

## Características

- Publica en múltiples grupos de Facebook utilizando varias cuentas en rotación.
- Descarga el contenido a publicar desde una URL que devuelve un JSON.
- Responde de forma automática a comentarios en las publicaciones y mensajes de Messenger.

> **Nota:** El código se ofrece únicamente con fines educativos. El uso de bots automatizados está sujeto a las políticas de Facebook y puede requerir permisos adicionales. Asegúrate de contar con la autorización correspondiente antes de utilizarlo.

## Requisitos

- Python 3.8 o superior.
- Paquetes indicados en `requirements.txt`.
- Tokens de acceso válidos para cada cuenta de Facebook que vaya a publicar.
- Los identificadores (ID) de los grupos donde se realizarán las publicaciones.

## Uso rápido

1. Instala las dependencias:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Crea un archivo `.env` o define las variables de entorno con las claves:
   - `TOKENS`: lista separada por comas con los tokens de Facebook.
   - `GROUP_IDS`: lista separada por comas con los ID de los grupos.
   - `JSON_URL`: dirección desde donde se descargará el contenido a publicar.

3. Ejecuta el script de ejemplo:
   ```bash
   python facebook_group_bot/bot.py
   ```
