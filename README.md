# Anime Bot Telegram
El objetivo del bot es buscar títulos de animes en la página web de AnimeFLV (No es un bot oficial), busca las coincidencias del anime y las despliega al usuario a través de una lista con la cual puede interactuar hasta obtener los enlaces de descarga del episodio y capítulo preferido. 

Este bot cuenta con persistencia en FireBase.

Para interactuar con el bot: <a href="https://t.me/AnimesAndMoreBot"> `AnimesAndMoreBot` </a>

# Variables de Entorno (Env Var)
Si deseas ejecutar el bot e incorporarlo con FireBase, es necesario crear las siguientes variables de entorno:

> `FIREBASE_CREDENTIALS` : Credenciales otorgadas por FireBase en RealTime Database

> `FIREBASE_URL` : URL de la Base de Datos en RealTime DataBase

> `TOKEN` :  Token otorgado por el bot de Telegram

> `MODE` :  Modo en que será ejecutado el bot, para modo local es "dev" y para producción es "prod"

# ¿Qué Packages son necesarios?
Todos los recursos usados para el desarrollo del bot se encuentran en: `requirements.txt`
> `pip install -r requirements.txt`

# ¿Cómo ejecutarlo?
Una vez instalados todos los recursos y haber configurado las variables de entorno, se emplea el siguiente comando para iniciarlo:
> `python anime_bot.py`

# Interactuando con el Bot
<img src="img/example.gif">

# Recursos
FireBase: https://firebase.google.com/docs/reference/admin/python 

Telegram: https://core.telegram.org/bots/api

Bot Telegram: https://python-telegram-bot.readthedocs.io/en/stable/index.html

Emojis: https://unicode.org/emoji/charts/full-emoji-list.html






