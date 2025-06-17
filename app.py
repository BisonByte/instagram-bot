from flask import Flask, render_template, request, redirect, url_for, flash
from main import SeguidorInstagram
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "changeme")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_bot():
    usuario = request.form.get("usuario")
    clave = request.form.get("clave")
    proxy = request.form.get("proxy")
    target = request.form.get("target")
    do_like = request.form.get("like_post")
    do_follow = request.form.get("seguir_followers")

    if not all([usuario, clave, target]):
        flash("Usuario, contraseña y cuenta objetivo son obligatorios")
        return redirect(url_for("index"))

    if proxy:
        os.environ["PROXY"] = proxy

    bot = SeguidorInstagram(usuario, clave)
    try:
        bot.iniciar_sesion()
        if do_like:
            bot.dar_like_publicacion()
        if do_follow:
            bot.encontrar_seguidores(target)
            bot.seguir()
        flash("Bot ejecutado correctamente")
    except Exception as exc:
        flash(f"Ocurrió un error: {exc}")
    finally:
        bot.cerrar_navegador()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
