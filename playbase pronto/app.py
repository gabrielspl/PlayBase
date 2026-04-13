from flask import Flask
from jogos import jogos_bp
from dotenv import load_dotenv
from extensions import mail
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "chave_secreta_para_mensagens")


app.config["MAIL_SERVER"]   = "smtp.gmail.com"
app.config["MAIL_PORT"]     = 587
app.config["MAIL_USE_TLS"]  = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail.init_app(app)
app.register_blueprint(jogos_bp)

if __name__ == "__main__":
    app.run(debug=True)
