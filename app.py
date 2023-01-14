from flask import Flask, redirect, request, url_for, session
from spotipy import SpotifyOAuth
from random import choices
from string import ascii_letters, digits
from time import time

key_letters = choices(ascii_letters + digits, k=16)

app = Flask(__name__)
app.secret_key = "".join([str(i) for i in key_letters])
app.config["SESSION_COOKIE_NAME"] = "spotify-login-session"
TOKEN_INFO = "token_info"


def create_oauth_object():
    return SpotifyOAuth(
        client_id="37966fda0d884fcc8d13f2d3d6d6e7e1",
        client_secret="0232febf10974b9091b8e05d013ff547",
        redirect_uri=url_for("redirectPage", _external=True),
        scope="user-library-read",
    )


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception("No token found in session")
    now = int(time())

    is_token_expired = token_info["expires_at"] - now < 60
    if is_token_expired:
        oauth = create_oauth_object()
        token_info = oauth.refresh_access_token(token_info["refresh_token"])

    return token_info


@app.route("/")
def login():
    oauth = create_oauth_object()
    auth_url = oauth.get_authorize_url()
    return redirect(auth_url)


@app.route("/redirect")
def redirectPage():
    oauth = create_oauth_object()
    session.clear()
    code = request.args.get("code")
    token_info = oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for("getTracks", _external=True))


@app.route("/getTracks")
def getTracks():
    return "This is the get tracks page"


if __name__ == "__main__":
    app.run(debug=True)
