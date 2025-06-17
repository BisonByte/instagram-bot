import os
import itertools
import requests
from dotenv import load_dotenv

load_dotenv()

class FacebookAutoPoster:
    """Publica contenido en varios grupos usando diferentes tokens."""

    GRAPH_URL = "https://graph.facebook.com/v18.0"

    def __init__(self, tokens, group_ids, json_url):
        self.tokens = tokens
        self.group_ids = group_ids
        self.json_url = json_url
        self.token_cycle = itertools.cycle(self.tokens)

    def fetch_content(self):
        """Descarga la información desde la URL definida."""
        try:
            response = requests.get(self.json_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            print(f"Error al obtener contenido: {exc}")
            return None

    def post_to_group(self, group_id, message, link=None):
        """Envía una publicación al grupo indicado."""
        token = next(self.token_cycle)
        params = {"access_token": token, "message": message}
        if link:
            params["link"] = link
        url = f"{self.GRAPH_URL}/{group_id}/feed"
        resp = requests.post(url, params=params, timeout=10)
        if resp.ok:
            data = resp.json()
            print(f"Publicado en {group_id}: {data.get('id')}")
            return data.get("id")
        else:
            print(f"Fallo al publicar en {group_id}: {resp.text}")
            return None

    def autopost(self):
        content = self.fetch_content()
        if not content:
            print("No hay contenido para publicar")
            return []
        message = content.get("message")
        link = content.get("link")
        posted_ids = []
        for group_id in self.group_ids:
            post_id = self.post_to_group(group_id, message, link)
            if post_id:
                posted_ids.append(post_id)
        return posted_ids

class FacebookAutoResponder:
    """Responde a comentarios de las publicaciones en los grupos."""

    def __init__(self, token):
        self.token = token
        self.graph_url = FacebookAutoPoster.GRAPH_URL

    def get_comments(self, post_id):
        url = f"{self.graph_url}/{post_id}/comments"
        params = {"access_token": self.token}
        resp = requests.get(url, params=params, timeout=10)
        if resp.ok:
            return resp.json().get("data", [])
        return []

    def reply_to_comment(self, comment_id, message):
        url = f"{self.graph_url}/{comment_id}/comments"
        params = {"access_token": self.token, "message": message}
        resp = requests.post(url, params=params, timeout=10)
        if resp.ok:
            print(f"Respondido en comentario {comment_id}")
        else:
            print(f"Fallo al responder {comment_id}: {resp.text}")

    def auto_reply(self, post_ids, reply_message):
        for post_id in post_ids:
            comments = self.get_comments(post_id)
            for comment in comments:
                self.reply_to_comment(comment["id"], reply_message)

if __name__ == "__main__":
    tokens = os.getenv("TOKENS", "").split(",")
    group_ids = os.getenv("GROUP_IDS", "").split(",")
    json_url = os.getenv("JSON_URL", "")
    reply_message = os.getenv("REPLY_MESSAGE", "Gracias por tu comentario!")

    tokens = [t.strip() for t in tokens if t.strip()]
    group_ids = [g.strip() for g in group_ids if g.strip()]

    if not tokens or not group_ids or not json_url:
        print("Debes definir TOKENS, GROUP_IDS y JSON_URL en las variables de entorno")
        exit(1)

    poster = FacebookAutoPoster(tokens, group_ids, json_url)
    posts = poster.autopost()

    if posts:
        responder = FacebookAutoResponder(tokens[0])
        responder.auto_reply(posts, reply_message)
